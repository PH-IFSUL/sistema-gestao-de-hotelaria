import tkinter as tk
from typing import Callable
from models.estadia import Reserva
from .seletor_base import ColunaSeletor, JanelaSeletorBase


class JanelaSelecionarReserva(JanelaSeletorBase[Reserva]):
    """Janela modal para pesquisar e selecionar uma reserva confirmada."""

    _COLUNAS = (
        ColunaSeletor("id", "#", 45),
        ColunaSeletor("cliente", "Cliente", 170),
        ColunaSeletor("quarto", "Quarto", 80),
        ColunaSeletor("checkin", "Check-in", 95),
        ColunaSeletor("checkout", "Check-out", 95),
    )

    def __init__(
        self,
        pai: tk.Misc,
        buscar_reservas: Callable[[str], list[Reserva]],
        titulo: str = "Selecionar Reserva"
    ) -> None:
        super().__init__(
            pai=pai,
            buscar_itens=buscar_reservas,
            colunas=self._COLUNAS,
            titulo=titulo,
            cabecalho="Selecione uma reserva confirmada para check-in",
            rotulo_busca="Buscar (cliente, CPF ou quarto):",
            singular="reserva",
            plural="reservas",
            mensagem_selecao_vazia="Selecione uma reserva na lista.",
            geometria="560x400",
            largura_min=480,
            altura_min=320,
        )

    @property
    def reserva_selecionada(self) -> Reserva | None:
        return self.item_selecionado

    def _extrair_valores(self, reserva: Reserva) -> tuple[int | None, str, str, str, str]:
        quarto_txt = f"Q. {reserva.quarto.get_numero()}" if reserva.quarto else "-"
        return (
            reserva.id,
            reserva.hospede.get_nome(),
            quarto_txt,
            reserva.data_checkin.strftime("%d/%m/%Y"),
            reserva.data_checkout.strftime("%d/%m/%Y"),
        )
