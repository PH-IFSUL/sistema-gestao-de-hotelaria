import tkinter as tk
from tkinter import ttk
from typing import Callable
from models.quarto import Quarto
from ..estilo.constantes import CoresTema, FontesTema
from .seletor_base import ColunaSeletor, JanelaSeletorBase


class JanelaSelecionarQuarto(JanelaSeletorBase[Quarto]):
    """Janela modal para pesquisar e selecionar um quarto cadastrado."""

    _COLUNAS = (
        ColunaSeletor("numero", "Número", 90),
        ColunaSeletor("tipo", "Tipo", 130),
        ColunaSeletor("valor", "Diária (R$)", 120),
        ColunaSeletor("status", "Status", 130),
    )

    def __init__(
        self,
        pai: tk.Misc,
        buscar_quartos: Callable[[str, bool], list[Quarto]],
        titulo: str = "Selecionar Quarto"
    ) -> None:
        self._buscar_quartos_fn = buscar_quartos
        self._var_apenas_disponiveis = tk.BooleanVar(value=True)
        super().__init__(
            pai=pai,
            buscar_itens=self._filtrar_quartos,
            colunas=self._COLUNAS,
            titulo=titulo,
            cabecalho="Selecione um quarto para a reserva",
            rotulo_busca="Buscar (número, tipo ou status):",
            singular="quarto",
            plural="quartos",
            mensagem_selecao_vazia="Selecione um quarto na lista.",
            geometria="560x420",
            largura_min=480,
            altura_min=340
        )

    @property
    def quarto_selecionado(self) -> Quarto | None:
        return self.item_selecionado

    def _filtrar_quartos(self, filtro: str) -> list[Quarto]:
        return self._buscar_quartos_fn(filtro, self._var_apenas_disponiveis.get())

    def _construir_filtros_extras(self, container: tk.Frame) -> None:
        tk.Checkbutton(
            container,
            text="Mostrar apenas quartos disponíveis",
            variable=self._var_apenas_disponiveis,
            command=self._carregar_itens,
            bg=CoresTema.COR_FUNDO,
            fg=CoresTema.COR_TEXTO,
            activebackground=CoresTema.COR_FUNDO,
            selectcolor=CoresTema.COR_SURFACE,
            font=FontesTema.FONTE_LABEL_SM,
            cursor="hand2"
        ).pack(anchor="w", pady=(0, 8))

    def _configurar_treeview(self, tree: ttk.Treeview) -> None:
        tree.tag_configure("indisponivel", foreground="#8A2020", background="#FAEAEA")

    def _extrair_valores(self, quarto: Quarto) -> tuple[int, str, str, str]:
        return (
            quarto.get_numero(),
            quarto.get_tipo(),
            f"R$ {quarto.get_valor_diaria():.2f}",
            quarto.estado.obter_atual(),
        )

    def _obter_tags(self, quarto: Quarto) -> tuple[str, ...]:
        if quarto.estado.obter_atual() == "Disponível":
            return ()
        return ("indisponivel",)
