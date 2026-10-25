from dataclasses import dataclass
from .ajudante_estilo import AjudanteEstilo


@dataclass(frozen=True)
class _CoresTema:
    """Cores do tema da aplicação."""
    COR_FUNDO: str       = AjudanteEstilo.obter_cor("COR_FUNDO", "#F5F4F0")
    COR_SURFACE: str     = AjudanteEstilo.obter_cor("COR_SURFACE", "#FFFFFF")
    COR_ACCENT: str      = AjudanteEstilo.obter_cor("COR_ACCENT", "#2C5F8A")
    COR_ACCENT_DARK: str = AjudanteEstilo.obter_cor("COR_ACCENT_DARK", "#1E4266")
    COR_TEXTO: str       = AjudanteEstilo.obter_cor("COR_TEXTO", "#1A1714")
    COR_TEXTO_SOFT: str  = AjudanteEstilo.obter_cor("COR_TEXTO_SOFT", "#6A6460")
    COR_BORDA: str       = AjudanteEstilo.obter_cor("COR_BORDA", "#DDDAD4")
    COR_ERRO: str        = AjudanteEstilo.obter_cor("COR_ERRO", "#8A2020")
    COR_SUCESSO: str     = AjudanteEstilo.obter_cor("COR_SUCESSO", "#2A6644")


CoresTema = _CoresTema()


@dataclass(frozen=True)
class _FontesTema:
    """Fontes do tema da aplicação."""
    FONTE_LABEL: tuple[str, int] = AjudanteEstilo.obter_fonte("FONTE_LABEL", ("Segoe UI", 10))
    FONTE_LABEL_SM: tuple[str, int] = AjudanteEstilo.obter_fonte("FONTE_LABEL_SM", ("Segoe UI", 9))
    FONTE_BOTAO: tuple[str, int, str] = AjudanteEstilo.obter_fonte("FONTE_BOTAO", ("Segoe UI", 10, "bold"))


FontesTema = _FontesTema()
