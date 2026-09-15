"""Ponto de entrada da ingestao Bronze."""
import logging

from src.aws import configurar_aws, definir_destino, enviar_aws
from src.config_loader import carregar_configs
from src.extractor import extrair
from src.metadata import gerar_manifest

logger = logging.getLogger(__name__)


def executar():
    configs = carregar_configs()
    cliente, bucket = configurar_aws()
    for config in configs:
        source_id = config["source"]["id"]
        logger.info("Fonte iniciada | source=%s", source_id)
        try:
            arquivos = extrair(config)
            for arquivo in arquivos:
                destino = definir_destino(config, arquivo)
                manifest = gerar_manifest(config, arquivo, bucket, destino)
                enviar_aws(cliente, bucket, arquivo, manifest)
        except Exception:
            logger.exception("Erro da fonte | source=%s", source_id)
            raise
    logger.info("Ingestao finalizada | fontes=%s", len(configs))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    executar()
