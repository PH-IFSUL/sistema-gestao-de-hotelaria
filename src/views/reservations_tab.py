import tkinter as tk
from tkinter import ttk, messagebox
from controllers.stay_controller import Stay_Controller
from views.style.constants import TmColors, TmFonts
from .components.forms import CampoFormulario


class AbaReservas(ttk.Frame):
    def __init__(self, parent, stay_ctrl: Stay_Controller):
        super().__init__(parent)
        self._controller = stay_ctrl

        self._construir()
    
    def _construir(self):
        painel_reserva = tk.Frame(self, bg=TmColors.COR_SURFACE, bd=0,
                               highlightthickness=1, highlightbackground=TmColors.COR_BORDA)
        painel_reserva.pack(side="left", fill="y", padx=(12, 6), pady=12, ipadx=12, ipady=12)