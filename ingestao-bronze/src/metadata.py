"""Manifest a partir da configuracao e dos bytes adquiridos."""
import hashlib
from copy import deepcopy


def gerar_manifest(config, arquivo, bucket, s3_key):
    manifest = deepcopy(config)
    manifest["ingestion"] = {
        "retrieved_at": arquivo["retrieved_at"],
        "filename": arquivo["filename"],
        "source_url": arquivo["source_url"],
        "resource_id": arquivo.get("resource_id"),
        "size_bytes": len(arquivo["content"]),
        "sha256": hashlib.sha256(arquivo["content"]).hexdigest(),
        "s3_bucket": bucket,
        "s3_key": s3_key,
    }
    return manifest
