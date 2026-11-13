import tkinter as tk
from tkinter import ttk
from controllers.quarto_controller import QuartoController
from controllers.cliente_controller import ClienteController
from controllers.estadia_controller import EstadiaController
from .aba_clientes import AbaClientes
from .aba_quartos import AbaQuartos
from .aba_reservas import AbaReservas
from .estilo.constantes import CoresTema, FontesTema


def _configurar_estilo():
    """Configura o estilo da aplicação Tkinter."""
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TNotebook", background=CoresTema.COR_FUNDO, borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        background=CoresTema.COR_BORDA,
        foreground=CoresTema.COR_TEXTO_SOFT,
        padding=[14, 6],
        font=("Segoe UI", 10)
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", CoresTema.COR_SURFACE)],
        foreground=[("selected", CoresTema.COR_ACCENT)]
    )
    style.configure(
        "Treeview",
        background=CoresTema.COR_SURFACE,
        foreground=CoresTema.COR_TEXTO,
        rowheight=26,
        fieldbackground=CoresTema.COR_SURFACE,
        font=FontesTema.FONTE_LABEL_SM
    )
    style.configure(
        "Treeview.Heading",
        background=CoresTema.COR_ACCENT,
        foreground="white",
        font=("Segoe UI", 9, "bold"),
        relief="flat"
    )
    style.map("Treeview", background=[("selected", "#D0E4F5")])
    style.configure("TCombobox", fieldbackground=CoresTema.COR_SURFACE, font=FontesTema.FONTE_LABEL)


class JanelaPrincipal(tk.Tk):
    """Classe que representa a janela principal do sistema."""

    def __init__(
        self,
        cliente_ctrl: ClienteController,
        quarto_ctrl: QuartoController,
        stay_ctrl: EstadiaController
    ):
        super().__init__()
        self.title("Sistema de Gestão de Hotel")
        self.geometry("820x520")
        self.minsize(720, 480)
        self.configure(bg=CoresTema.COR_FUNDO)
        _configurar_estilo()
        self._construir(cliente_ctrl, quarto_ctrl, stay_ctrl)

    def _construir(
        self,
        cliente_ctrl: ClienteController,
        quarto_ctrl: QuartoController,
        stay_ctrl: EstadiaController
    ):
        header = tk.Frame(self, bg=CoresTema.COR_ACCENT, height=52)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header,
            text="🏨  Sistema de Gestão de Hotel",
            font=("Segoe UI", 14, "bold"),
            bg=CoresTema.COR_ACCENT,
            fg="white"
        ).pack(side="left", padx=16, pady=12)
        tk.Label(
            header,
            text="Protótipo MVC · Tkinter",
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_ACCENT,
            fg="#A8C8E8"
        ).pack(side="right", padx=16)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        aba_clientes = AbaClientes(notebook, cliente_ctrl)
        notebook.add(aba_clientes, text="  👤  Clientes  ")

        aba_quartos = AbaQuartos(notebook, quarto_ctrl)
        notebook.add(aba_quartos, text="  🛏  Quartos  ")

        # aba_reservas = AbaReservas(notebook, stay_ctrl)
        # notebook.add(aba_reservas, text="  📖  Reservas  ")
