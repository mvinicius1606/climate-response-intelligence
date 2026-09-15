"""Obtencao dos arquivos sem transformar seu conteudo."""
import logging
import json
import io
import zipfile
from datetime import datetime, timezone
from pathlib import PurePosixPath
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)



def validar_conteudo(content, formato):
    """Conferir formato sem regravar ou transformar os bytes recebidos."""
    if not content:
        raise ValueError("Resposta vazia")
    if formato == "JSON":
        try:
            dados = json.loads(content)
        except (ValueError, UnicodeError) as erro:
            raise ValueError("Resposta nao contem JSON valido") from erro
        if not isinstance(dados, (list, dict)) or not dados:
            raise ValueError("JSON sem registros")
        if isinstance(dados, dict) and any(str(k).lower() in {"erro", "error", "errors"} for k in dados):
            raise ValueError("API retornou objeto de erro")
    elif formato == "ZIP":
        if not zipfile.is_zipfile(io.BytesIO(content)):
            raise ValueError("Resposta nao contem ZIP valido")
    elif formato == "PDF":
        if not content.startswith(b"%PDF-") or b"%%EOF" not in content[-1024:]:
            raise ValueError("Resposta nao contem PDF com assinatura e terminador")
    else:
        raise ValueError(f"Formato nao suportado: {formato}")

def _baixar(config, url, resource_id=None):
    access = config["access"]
    formato = access["format"]
    nome = PurePosixPath(unquote(urlsplit(url).path)).name
    extensao = "." + formato.lower()
    if not nome.lower().endswith(extensao):
        nome = f"{resource_id or config['source']['id']}{extensao}"
    if "/" in nome or "\\" in nome or nome in {".", ".."}:
        raise ValueError("Nome de arquivo invalido")
    request = Request(url, method=access["method"], headers={"Accept-Encoding": "identity"})
    with urlopen(request, timeout=120) as response:
        content = response.read()
    if not content:
        raise ValueError(f"source.id={config['source']['id']}: resposta vazia")
    validar_conteudo(content, formato)
    logger.info("Arquivo extraido | source=%s file=%s bytes=%s", config["source"]["id"], nome, len(content))
    return {
        "content": content,
        "filename": nome,
        "source_url": url,
        "resource_id": resource_id,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
    }


def extrair_api(config):
    return [_baixar(config, config["access"]["url"])]


def extrair_zip(config):
    return [_baixar(config, config["access"]["url"])]


def extrair_pdf(config):
    access = config["access"]
    recursos = access.get("resources", [{"url": access.get("url")}])
    return [_baixar(config, recurso["url"], recurso.get("id")) for recurso in recursos]


def extrair(config):
    access = config["access"]
    tipo, formato = access.get("type"), access.get("format")
    if tipo == "API" and formato == "JSON":
        return extrair_api(config)
    if tipo == "download direto" and formato == "ZIP":
        return extrair_zip(config)
    if tipo == "download direto" and formato == "PDF":
        return extrair_pdf(config)
    raise ValueError(f"source.id={config['source']['id']} access.type={tipo} access.format={formato}: mecanismo nao suportado")
