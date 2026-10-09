import tkinter as tk
from tkinter import ttk
from controllers.room_controller import Room_Controller
from controllers.client_controller import Client_Controller
from controllers.stay_controller import Stay_Controller
from views.clients_tab import AbaClientes
from views.rooms_tab import AbaQuartos
from views.reservations_tab import AbaReservas
from views.style.constants import TmColors, TmFonts

def _configurar_estilo():
    """
    Configura o estilo da aplicação.
    """
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TNotebook", background=TmColors.COR_FUNDO, borderwidth=0)
    style.configure("TNotebook.Tab", background=TmColors.COR_BORDA, foreground=TmColors.COR_TEXTO_SOFT,
                    padding=[14, 6], font=("Segoe UI", 10))
    style.map("TNotebook.Tab",
              background=[("selected", TmColors.COR_SURFACE)],
              foreground=[("selected", TmColors.COR_ACCENT)])
    style.configure("Treeview", background=TmColors.COR_SURFACE, foreground=TmColors.COR_TEXTO,
                    rowheight=26, fieldbackground=TmColors.COR_SURFACE, font=TmFonts.FONTE_LABEL_SM)
    style.configure("Treeview.Heading", background=TmColors.COR_ACCENT, foreground="white",
                    font=("Segoe UI", 9, "bold"), relief="flat")
    style.map("Treeview", background=[("selected", "#D0E4F5")])
    style.configure("TCombobox", fieldbackground=TmColors.COR_SURFACE, font=TmFonts.FONTE_LABEL)


class JanelaPrincipal(tk.Tk):
    '''
    Classe que representa a janela principal.
    '''
    def __init__(self, cliente_ctrl: Client_Controller, quarto_ctrl: Room_Controller, stay_ctrl: Stay_Controller):
        super().__init__()
        self.title("Sistema de Gestão de Hotel")
        self.geometry("820x520")
        self.minsize(720, 480)
        self.configure(bg=TmColors.COR_FUNDO)
        _configurar_estilo()
        self._construir(cliente_ctrl, quarto_ctrl, stay_ctrl)

    def _construir(self, cliente_ctrl: Client_Controller, quarto_ctrl: Room_Controller, stay_ctrl: Stay_Controller):
        header = tk.Frame(self, bg=TmColors.COR_ACCENT, height=52)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🏨  Sistema de Gestão de Hotel",  # configurar .ini para mudar nome do hotel
                 font=("Segoe UI", 14, "bold"), bg=TmColors.COR_ACCENT,
                 fg="white").pack(side="left", padx=16, pady=12)
        tk.Label(header, text="Protótipo MVC · Tkinter",
                 font=TmFonts.FONTE_LABEL_SM, bg=TmColors.COR_ACCENT,
                 fg="#A8C8E8").pack(side="right", padx=16)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        aba_clientes = AbaClientes(notebook, cliente_ctrl)
        notebook.add(aba_clientes, text="  👤  Clientes  ")

        aba_quartos = AbaQuartos(notebook, quarto_ctrl)
        notebook.add(aba_quartos, text="  🛏  Quartos  ")

        aba_reservas = AbaReservas(notebook, stay_ctrl)
        notebook.add(aba_reservas, text="  📖  Reservas  ")
