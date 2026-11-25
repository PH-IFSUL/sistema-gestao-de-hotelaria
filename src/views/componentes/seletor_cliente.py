import tkinter as tk
from typing import Callable
from models.cliente import Cliente
from .seletor_base import ColunaSeletor, JanelaSeletorBase


class JanelaSelecionarCliente(JanelaSeletorBase[Cliente]):
    """Janela modal para pesquisar e selecionar um cliente cadastrado."""

    _COLUNAS = (
        ColunaSeletor("nome", "Nome", 190),
        ColunaSeletor("cpf", "CPF", 110),
        ColunaSeletor("telefone", "Telefone", 110),
        ColunaSeletor("email", "E-mail", 150),
    )

    def __init__(
        self,
        pai: tk.Misc,
        buscar_clientes: Callable[[str], list[Cliente]],
        titulo: str = "Selecionar Cliente"
    ) -> None:
        super().__init__(
            pai=pai,
            buscar_itens=buscar_clientes,
            colunas=self._COLUNAS,
            titulo=titulo,
            cabecalho="Selecione um cliente para a reserva",
            rotulo_busca="Buscar (nome ou CPF):",
            singular="cliente",
            plural="clientes",
            mensagem_selecao_vazia="Selecione um cliente na lista."
        )

    @property
    def cliente_selecionado(self) -> Cliente | None:
        return self.item_selecionado

    def _extrair_valores(self, cliente: Cliente) -> tuple[str, str, str, str]:
        return (
            cliente.get_nome(),
            cliente.get_cpf(),
            cliente.get_telefone(),
            cliente.get_email(),
        )
