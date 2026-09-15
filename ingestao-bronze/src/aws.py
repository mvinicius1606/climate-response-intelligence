"""Configuracao AWS existente e persistencia dos originais e manifests."""
import json
import hashlib
from copy import deepcopy
from botocore.exceptions import ClientError
import logging
import os
from pathlib import Path

import boto3
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def configurar_aws():
    etapa = Path(__file__).resolve().parents[1]
    load_dotenv(etapa / ".env", override=False)
    load_dotenv(etapa.parent / ".env", override=False)
    bucket = os.getenv("BUCKET_BRONZE")
    if not bucket or not bucket.strip():
        raise ValueError("Variavel BUCKET_BRONZE ausente")
    # O .env existente usa ACESS (um C); aceitar tambem o nome padrao AWS.
    access_key = os.getenv("AWS_ACCESS_KEY_ID") or os.getenv("AWS_ACESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    if bool(access_key) != bool(secret_key):
        raise ValueError("Configuracao AWS incompleta: access key e secret key devem coexistir")
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )
    return session.client("s3"), bucket.strip()


def definir_destino(config, arquivo):
    return f"{config['source']['id']}/{arquivo['filename']}"



def _ler_objeto(cliente, bucket, chave):
    try:
        resposta = cliente.get_object(Bucket=bucket, Key=chave)
    except ClientError as erro:
        if erro.response["Error"]["Code"] in {"NoSuchKey", "404"}:
            return None
        raise
    try:
        return resposta["Body"].read(), resposta.get("Metadata", {})
    finally:
        resposta["Body"].close()


def enviar_aws(cliente, bucket, arquivo, manifest):
    chave = manifest["ingestion"]["s3_key"]
    esperado = manifest["ingestion"]
    config = {k: v for k, v in manifest.items() if k != "ingestion"}
    config_sha = hashlib.sha256(json.dumps(config, sort_keys=True, ensure_ascii=True).encode("utf-8")).hexdigest()
    try:
        cliente.put_object(
            Bucket=bucket, Key=chave, Body=arquivo["content"], IfNoneMatch="*",
            Metadata={"ingestion": json.dumps(esperado, ensure_ascii=True, separators=(",", ":")), "config_sha256": config_sha},
        )
    except ClientError as erro:
        if erro.response["Error"]["Code"] not in {"PreconditionFailed", "412"}:
            raise
    bruto = _ler_objeto(cliente, bucket, chave)
    if bruto is None:
        raise ValueError("Original ausente apos upload")
    conteudo, metadata = bruto
    if len(conteudo) != esperado["size_bytes"] or hashlib.sha256(conteudo).hexdigest() != esperado["sha256"]:
        raise ValueError(f"Conflito de conteudo no destino: {chave}; original preservado")
    existente = _ler_objeto(cliente, bucket, chave + ".manifest.json")
    if existente is not None:
        anterior = json.loads(existente[0])
        dados = anterior.get("ingestion", {})
        for campo in ("sha256", "size_bytes", "source_url", "resource_id", "filename", "s3_bucket", "s3_key"):
            if dados.get(campo) != esperado.get(campo):
                raise ValueError(f"Manifest incompativel: {chave}")
        if anterior.get("source", {}).get("id") != manifest["source"]["id"]:
            raise ValueError(f"Fonte incompativel: {chave}")
        logger.info("Original e manifest existentes verificados | file=%s", arquivo["filename"])
        return
    # Recuperar o timestamp da primeira aquisicao, nunca inventar uma nova data.
    if "ingestion" not in metadata:
        raise ValueError(f"Original legado sem metadata de recuperacao: {chave}")
    if metadata.get("config_sha256") != config_sha:
        raise ValueError(f"Configuracao mudou durante recuperacao: {chave}")
    recuperado = json.loads(metadata["ingestion"])
    for campo in ("sha256", "size_bytes", "source_url", "resource_id", "filename", "s3_bucket", "s3_key"):
        if recuperado.get(campo) != esperado.get(campo):
            raise ValueError(f"Metadata de recuperacao incompativel: {chave}")
    final = deepcopy(manifest)
    final["ingestion"] = recuperado
    corpo = json.dumps(final, ensure_ascii=False, indent=2).encode("utf-8")
    try:
        cliente.put_object(
            Bucket=bucket, Key=chave + ".manifest.json", Body=corpo,
            ContentType="application/json; charset=utf-8", IfNoneMatch="*",
        )
    except ClientError as erro:
        if erro.response["Error"]["Code"] not in {"PreconditionFailed", "412"}:
            raise
    salvo = _ler_objeto(cliente, bucket, chave + ".manifest.json")
    if salvo is None or json.loads(salvo[0]) != final:
        raise ValueError(f"Manifest armazenado diverge do esperado: {chave}")
    logger.info("Original e manifest verificados no S3 | file=%s", arquivo["filename"])
