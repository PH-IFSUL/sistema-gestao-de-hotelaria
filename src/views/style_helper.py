import pathlib
from typing import Any
from models.utils.json_helpers import JSONHelper

class Estilo:
    def __init__(self):
        self.style_dict = self.get_dict_from_json()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Estilo, cls).__new__(cls)
        return cls.instance

    def get_dict_from_json(self):
        json_helper = JSONHelper()
        style_json_path = pathlib.Path(__file__).parent / "style.json"
        return json_helper.load_from_json(str(style_json_path))

    def get_color(self, color_name: str, default: str) -> str:
        '''pegar a cor do dicionario, se não funcionar usar a default '''
        if self.style_dict and "cores" in self.style_dict:
            cor = self.style_dict["cores"].get(color_name)
            if isinstance(cor, str) and cor:
                return cor
        return default

    def get_font(self, font_name: str, default: tuple[str | int, ...]) -> tuple[Any, ...]:
        if self.style_dict and "fontes" in self.style_dict:
            fonte = self.style_dict["fontes"].get(font_name)
            if isinstance(fonte, (list, tuple)):
                return tuple(fonte)
        return default



