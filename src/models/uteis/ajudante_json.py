import json
import os
from typing import Any


class AjudanteJSON:
    """Classe utilitária para manipulação de arquivos JSON."""

    @staticmethod
    def carregar_de_json(caminho_arquivo: str) -> Any:
        """
        Carrega dados a partir de um arquivo JSON.

        :param caminho_arquivo: Caminho para o arquivo JSON.
        :return: Dados carregados do arquivo JSON (dict ou list), ou None se vazio/inexistente.
        """
        if os.path.exists(caminho_arquivo) and os.path.getsize(caminho_arquivo) != 0:
            with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        return None

    # Compatibilidade
    load_from_json = carregar_de_json


# Alias para compatibilidade
JSONHelper = AjudanteJSON
