"""Validacao offline com HTTP e S3 simulados."""
import hashlib
import json
import os
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gatilhador
from src import aws, extractor
from src.config_loader import carregar_configs
from src.metadata import gerar_manifest



def cliente_memoria():
    from io import BytesIO
    from botocore.exceptions import ClientError
    objetos = {}
    cliente = MagicMock()
    def put(**kw):
        chave = kw["Key"]
        if chave in objetos:
            raise ClientError({"Error": {"Code": "PreconditionFailed"}}, "PutObject")
        objetos[chave] = (kw["Body"], kw.get("Metadata", {}))
    def get(**kw):
        if kw["Key"] not in objetos:
            raise ClientError({"Error": {"Code": "NoSuchKey"}}, "GetObject")
        body, meta = objetos[kw["Key"]]
        return {"Body": BytesIO(body), "Metadata": meta}
    cliente.put_object.side_effect = put
    cliente.get_object.side_effect = get
    return cliente


def payload_formato(formato):
    if formato == "JSON":
        return b'[{"valor":"original"}]'
    if formato == "PDF":
        return b"%PDF-1.7\noriginal\n%%EOF\n"
    import io, zipfile
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as arquivo:
        arquivo.writestr("original.csv", b"data;chuva\n2024-05-27;\n")
    return buffer.getvalue()

class BronzeTests(unittest.TestCase):
    def setUp(self):
        self.configs = carregar_configs()

    def test_oito_fontes_nove_arquivos_bytes_e_manifest(self):
        original = deepcopy(self.configs)
        payload = b"original;\xff;;\r\n"
        cliente = cliente_memoria()
        nomes = set()
        with patch("src.extractor.urlopen") as abrir:
            abrir.return_value.__enter__.return_value.read.return_value = payload
            for config in self.configs:
                payload = payload_formato(config["access"]["format"])
                abrir.return_value.__enter__.return_value.read.return_value = payload
                for arquivo in extractor.extrair(config):
                    chave = aws.definir_destino(config, arquivo)
                    self.assertNotIn(chave, nomes)
                    nomes.add(chave)
                    manifest = gerar_manifest(config, arquivo, "teste", chave)
                    self.assertEqual(manifest["ingestion"]["sha256"], hashlib.sha256(payload).hexdigest())
                    self.assertEqual(manifest["ingestion"]["size_bytes"], len(payload))
                    aws.enviar_aws(cliente, "teste", arquivo, manifest)
                    bruto, meta = cliente.put_object.call_args_list[-2:]
                    self.assertEqual(bruto.kwargs["Body"], payload)
                    self.assertEqual(bruto.kwargs["IfNoneMatch"], "*")
                    self.assertEqual(json.loads(meta.kwargs["Body"]), manifest)
            self.assertEqual(abrir.call_count, 9)
        self.assertEqual(len(self.configs), 8)
        self.assertEqual(len(nomes), 9)
        self.assertEqual(self.configs, original)


    def test_rejeita_erro_html_e_formato_incorreto(self):
        for formato in ("JSON", "ZIP", "PDF"):
            with self.subTest(formato=formato):
                with self.assertRaises(ValueError):
                    extractor.validar_conteudo(b"<html>erro</html>", formato)
                with self.assertRaises(ValueError):
                    extractor.validar_conteudo(b"", formato)
                extractor.validar_conteudo(payload_formato(formato), formato)
        for payload in (b'{"error":"falha"}', b'[]', b'"erro"', b'{'):
            with self.assertRaises(ValueError):
                extractor.validar_conteudo(payload, "JSON")

    def test_retomada_preserva_timestamp_e_nao_sobrescreve(self):
        config = self.configs[0]
        arquivo = dict(content=b"original", filename="a.json", source_url="https://example.org/a", retrieved_at="2026-09-15T00:00:00+00:00")
        manifest = gerar_manifest(config, arquivo, "teste", "fonte/a.json")
        cliente = cliente_memoria()
        put = cliente.put_object.side_effect
        def falhar_manifest(**kw):
            if kw["Key"].endswith(".manifest.json"):
                raise RuntimeError("falha simulada")
            return put(**kw)
        cliente.put_object.side_effect = falhar_manifest
        with self.assertRaises(RuntimeError):
            aws.enviar_aws(cliente, "teste", arquivo, manifest)
        cliente.put_object.side_effect = put
        novo = deepcopy(manifest)
        novo["ingestion"]["retrieved_at"] = "2026-09-16T00:00:00+00:00"
        aws.enviar_aws(cliente, "teste", arquivo, novo)
        salvo = json.loads(aws._ler_objeto(cliente, "teste", "fonte/a.json.manifest.json")[0])
        self.assertEqual(salvo["ingestion"]["retrieved_at"], manifest["ingestion"]["retrieved_at"])
        aws.enviar_aws(cliente, "teste", arquivo, novo)
        diferente = dict(arquivo, content=b"outro")
        with self.assertRaisesRegex(ValueError, "Conflito"):
            aws.enviar_aws(cliente, "teste", diferente, gerar_manifest(config, diferente, "teste", "fonte/a.json"))
        self.assertEqual(aws._ler_objeto(cliente, "teste", "fonte/a.json")[0], b"original")

    def test_dispatch(self):
        for config in self.configs:
            nome = {"JSON": "extrair_api", "ZIP": "extrair_zip", "PDF": "extrair_pdf"}[config["access"]["format"]]
            with patch.object(extractor, nome, return_value=[]) as funcao:
                self.assertEqual(extractor.extrair(config), [])
                funcao.assert_called_once_with(config)
        invalido = deepcopy(self.configs[0])
        invalido["access"]["format"] = "CSV"
        with self.assertRaisesRegex(ValueError, "source.id=.*access.type=API access.format=CSV"):
            extractor.extrair(invalido)

    def test_http_metodo_url_nome_pdf_e_recursos(self):
        config = next(c for c in self.configs if c["source"]["id"] == "rs-coletivas")
        with patch("src.extractor.urlopen") as abrir:
            abrir.return_value.__enter__.return_value.read.return_value = payload_formato("PDF")
            arquivos = extractor.extrair(config)
        self.assertEqual(len(arquivos), 2)
        for recurso, arquivo, chamada in zip(config["access"]["resources"], arquivos, abrir.call_args_list):
            self.assertEqual(arquivo["resource_id"], recurso["id"])
            self.assertEqual(arquivo["filename"], recurso["url"].rsplit("/", 1)[1])
            self.assertEqual(chamada.args[0].full_url, recurso["url"])
            self.assertEqual(chamada.args[0].get_method(), "GET")

    def test_config_vazia_pendente_e_invalida(self):
        import yaml
        with tempfile.TemporaryDirectory() as pasta:
            base = Path(pasta)
            (base / "config.yml").write_text("", encoding="utf-8")
            (base / "pendente.yml").write_text("status: pending", encoding="utf-8")
            (base / "fonte.yml").write_text(yaml.safe_dump(self.configs[0]), encoding="utf-8")
            self.assertEqual(len(carregar_configs(base)), 1)
            (base / "invalido.yml").write_text("status: validated", encoding="utf-8")
            with self.assertRaises(ValueError):
                carregar_configs(base)

    def test_copia_profunda_manifest(self):
        config = self.configs[0]
        arquivo = dict(content=b"123", filename="teste.json", source_url="https://example.org", retrieved_at="2026-09-15T00:00:00+00:00")
        manifest = gerar_manifest(config, arquivo, "teste", "chave")
        manifest["source"]["roles"].append("teste")
        self.assertNotIn("teste", config["source"]["roles"])

    def test_aws_variaveis_existentes(self):
        ambiente = {"AWS_ACESS_KEY_ID": "fake", "AWS_SECRET_ACCESS_KEY": "fake-secret", "BUCKET_BRONZE": "teste", "AWS_REGION": "us-east-1"}
        with patch.dict(os.environ, ambiente, clear=True), patch("src.aws.load_dotenv"), patch("src.aws.boto3.Session") as session:
            _, bucket = aws.configurar_aws()
            self.assertEqual(bucket, "teste")
            self.assertEqual(session.call_args.kwargs["aws_access_key_id"], "fake")
        with patch.dict(os.environ, {}, clear=True), patch("src.aws.load_dotenv"):
            with self.assertRaisesRegex(ValueError, "BUCKET_BRONZE"):
                aws.configurar_aws()

    def test_falhas_http_e_s3_propagadas(self):
        with patch("src.extractor.urlopen", side_effect=TimeoutError):
            with self.assertRaises(TimeoutError):
                extractor.extrair(self.configs[0])
        cliente = cliente_memoria()
        cliente.put_object.side_effect = RuntimeError("falha simulada")
        with self.assertRaises(RuntimeError):
            aws.enviar_aws(cliente, "teste", {"content": b"x"}, {"ingestion": {"s3_key": "x"}})
        self.assertEqual(cliente.put_object.call_count, 1)

    def test_orquestracao_completa(self):
        cliente = cliente_memoria()
        with patch("gatilhador.configurar_aws", return_value=(cliente, "teste")), patch("src.extractor.urlopen") as abrir:
            abrir.return_value.__enter__.return_value.read.side_effect = [payload_formato(c["access"]["format"]) for c in self.configs for _ in c["access"].get("resources", [None])]
            gatilhador.executar()
        self.assertEqual(cliente.put_object.call_count, 18)


if __name__ == "__main__":
    unittest.main()
