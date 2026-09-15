"""Leitura e validacao minima das fontes YAML."""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

import yaml

CONFIG_DIR = Path(__file__).resolve().parents[1] / "config"


def carregar_configs(diretorio=CONFIG_DIR):
    configs = []
    ids = set()
    for caminho in sorted(Path(diretorio).glob("*.yml")):
        with caminho.open(encoding="utf-8") as arquivo:
            config = yaml.safe_load(arquivo)
        if config is None and caminho.name == "config.yml":
            continue
        if not isinstance(config, dict):
            raise ValueError(f"{caminho.name}: YAML deve conter um objeto")
        if config.get("status") != "validated":
            continue
        source = config.get("source", {})
        access = config.get("access", {})
        if not isinstance(source, dict) or not isinstance(access, dict):
            raise ValueError(f"{caminho.name}: source e access devem ser objetos")
        source_id = source.get("id")
        contexto = f"source.id={source_id} access.type={access.get('type')} access.format={access.get('format')}"
        if not isinstance(source_id, str) or not re.fullmatch(r"[a-zA-Z0-9_-]+", source_id):
            raise ValueError(f"{contexto}: identificador invalido")
        if source_id in ids:
            raise ValueError(f"{contexto}: identificador duplicado")
        if (access.get("type"), access.get("format")) not in {
            ("API", "JSON"), ("download direto", "ZIP"), ("download direto", "PDF")
        }:
            raise ValueError(f"{contexto}: mecanismo nao suportado")
        if access.get("method") != "GET":
            raise ValueError(f"{contexto}: somente GET suportado")
        recursos = access.get("resources")
        if recursos is not None:
            if access["format"] != "PDF" or "url" in access or not isinstance(recursos, list) or not recursos:
                raise ValueError(f"{contexto}: resources invalidos")
        else:
            recursos = [{"url": access.get("url")}]
        resource_ids = set()
        for recurso in recursos:
            if not isinstance(recurso, dict):
                raise ValueError(f"{contexto}: recurso invalido")
            url = recurso.get("url")
            if not isinstance(url, str) or urlsplit(url).scheme != "https" or not urlsplit(url).netloc:
                raise ValueError(f"{contexto}: URL HTTPS obrigatoria")
            if "resources" in access:
                rid = recurso.get("id")
                if not isinstance(rid, str) or not rid or rid in resource_ids:
                    raise ValueError(f"{contexto}: resource.id ausente ou duplicado")
                resource_ids.add(rid)
        json.dumps(config, ensure_ascii=False)
        ids.add(source_id)
        configs.append(config)
    if not configs:
        raise ValueError("Nenhuma fonte validated encontrada")
    return configs
