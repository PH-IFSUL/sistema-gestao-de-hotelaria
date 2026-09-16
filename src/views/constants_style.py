from dataclasses import dataclass
from .style_helper import Estilo

style_helper = Estilo()

@dataclass(frozen=True)
class _ThemeColors:
    COR_FUNDO: str       = style_helper.get_color("COR_FUNDO", "#F5F4F0")
    COR_SURFACE: str     = style_helper.get_color("COR_SURFACE", "#FFFFFF")
    COR_ACCENT: str      = style_helper.get_color("COR_ACCENT", "#2C5F8A")
    COR_ACCENT_DARK: str = style_helper.get_color("COR_ACCENT_DARK", "#1E4266")
    COR_TEXTO: str       = style_helper.get_color("COR_TEXTO", "#1A1714")
    COR_TEXTO_SOFT: str  = style_helper.get_color("COR_TEXTO_SOFT", "#6A6460")
    COR_BORDA: str       = style_helper.get_color("COR_BORDA", "#DDDAD4")
    COR_ERRO: str        = style_helper.get_color("COR_ERRO", "#8A2020")
    COR_SUCESSO: str     = style_helper.get_color("COR_SUCESSO", "#2A6644")
ThemeColors = _ThemeColors()

@dataclass(frozen=True)
class _ThemeFonts:
    FONTE_LABEL: tuple = style_helper.get_font("FONTE_LABEL", ("Segoe UI", 10))
    FONTE_LABEL_SM: tuple[str, int] = style_helper.get_font("FONTE_LABEL_SM", ("Segoe UI", 9))
    FONTE_BOTAO: tuple[str, int, str] = style_helper.get_font("FONTE_BOTAO", ("Segoe UI", 10, "bold"))
theme_fonts = _ThemeFonts()
