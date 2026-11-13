import pathlib
from typing import Any
from models.uteis.ajudante_json import AjudanteJSON


class _AjudanteEstilo:
    """Classe singleton para gerenciar o estilo da aplicação, incluindo cores e fontes."""

    def __init__(self) -> None:
        self.dicionario_estilo = self.obter_dicionario_json()

    def __new__(cls):
        """Padrão Singleton para garantir instância única."""
        if not hasattr(cls, "instance"):
            cls.instance = super(_AjudanteEstilo, cls).__new__(cls)
        return cls.instance

    def obter_dicionario_json(self):
        """Carrega o dicionário a partir do arquivo JSON."""
        caminho_estilo_json = pathlib.Path(__file__).parent / "estilo.json"
        return AjudanteJSON.carregar_de_json(str(caminho_estilo_json))

    def obter_cor(self, nome_cor: str, padrao: str) -> str:
        """Obtém a cor definida no JSON ou o padrão informado."""
        if self.dicionario_estilo and "cores" in self.dicionario_estilo:
            cor = self.dicionario_estilo["cores"].get(nome_cor)
            if isinstance(cor, str) and cor:
                return cor
        return padrao

    def obter_fonte(self, nome_fonte: str, padrao: tuple[str | int, ...]) -> tuple[Any, ...]:
        """Obtém a fonte definida no JSON ou o padrão informado."""
        if self.dicionario_estilo and "fontes" in self.dicionario_estilo:
            fonte = self.dicionario_estilo["fontes"].get(nome_fonte)
            if isinstance(fonte, (list, tuple)):
                return tuple(fonte)
        return padrao

AjudanteEstilo = _AjudanteEstilo()