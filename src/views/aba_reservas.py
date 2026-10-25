import tkinter as tk
from tkinter import ttk
from controllers.estadia_controller import EstadiaController
from .estilo.constantes import CoresTema


class AbaReservas(ttk.Frame):
    """Aba para gerenciamento de reservas (em desenvolvimento)."""

    def __init__(self, parent, stay_ctrl: EstadiaController):
        super().__init__(parent)
        self._controller = stay_ctrl
        self._construir()

    def _construir(self):
        painel_reserva = tk.Frame(
            self,
            bg=CoresTema.COR_SURFACE,
            bd=0,
            highlightthickness=1,
            highlightbackground=CoresTema.COR_BORDA
        )
        painel_reserva.pack(side="left", fill="y", padx=(12, 6), pady=12, ipadx=12, ipady=12)
