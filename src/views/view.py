import tkinter as tk
from tkinter import ttk, messagebox
from controllers.quarto_controller import QuartoController
from controllers.cliente_controller import ClienteController
from models.room.room import Quarto
from typing import NamedTuple
from .style_helper import Estilo

class ThemeColors(NamedTuple):
    COR_FUNDO: str
    COR_SURFACE: str
    COR_ACCENT: str
    COR_ACCENT_DARK: str
    COR_TEXTO: str
    COR_TEXTO_SOFT: str
    COR_BORDA: str
    COR_ERRO: str
    COR_SUCESSO: str

class ThemeFonts(NamedTuple):
    FONTE_LABEL: tuple[str, int]
    FONTE_LABEL_SM: tuple[str, int]
    FONTE_BOTAO: tuple[str, int, str]

style_helper = Estilo()

theme_colors = ThemeColors(
    COR_FUNDO=style_helper.get_color("COR_FUNDO"),
    COR_SURFACE=style_helper.get_color("COR_SURFACE"),
    COR_ACCENT=style_helper.get_color("COR_ACCENT"),
    COR_ACCENT_DARK=style_helper.get_color("COR_ACCENT_DARK"),
    COR_TEXTO=style_helper.get_color("COR_TEXTO"),
    COR_TEXTO_SOFT=style_helper.get_color("COR_TEXTO_SOFT"),
    COR_BORDA=style_helper.get_color("COR_BORDA"),
    COR_ERRO=style_helper.get_color("COR_ERRO"),
    COR_SUCESSO=style_helper.get_color("COR_SUCESSO")
)

theme_fonts = ThemeFonts(
    FONTE_LABEL=style_helper.get_font("FONTE_LABEL"),
    FONTE_LABEL_SM=style_helper.get_font("FONTE_LABEL_SM"),
    FONTE_BOTAO= style_helper.get_font("FONTE_BOTAO")
)

COR_FUNDO       = theme_colors.COR_FUNDO
COR_SURFACE     = theme_colors.COR_SURFACE
COR_ACCENT      = theme_colors.COR_ACCENT
COR_ACCENT_DARK = theme_colors.COR_ACCENT_DARK
COR_TEXTO       = theme_colors.COR_TEXTO
COR_TEXTO_SOFT  = theme_colors.COR_TEXTO_SOFT
COR_BORDA       = theme_colors.COR_BORDA
COR_ERRO        = theme_colors.COR_ERRO
COR_SUCESSO     = theme_colors.COR_SUCESSO
FONTE_LABEL     = theme_fonts.FONTE_LABEL
FONTE_LABEL_SM  = theme_fonts.FONTE_LABEL_SM
FONTE_BOTAO     = theme_fonts.FONTE_BOTAO


def _configurar_estilo():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TNotebook", background=COR_FUNDO, borderwidth=0)
    style.configure("TNotebook.Tab", background=COR_BORDA, foreground=COR_TEXTO_SOFT,
                    padding=[14, 6], font=("Segoe UI", 10))
    style.map("TNotebook.Tab",
              background=[("selected", COR_SURFACE)],
              foreground=[("selected", COR_ACCENT)])
    style.configure("Treeview", background=COR_SURFACE, foreground=COR_TEXTO,
                    rowheight=26, fieldbackground=COR_SURFACE, font=FONTE_LABEL_SM)
    style.configure("Treeview.Heading", background=COR_ACCENT, foreground="white",
                    font=("Segoe UI", 9, "bold"), relief="flat")
    style.map("Treeview", background=[("selected", "#D0E4F5")])
    style.configure("TCombobox", fieldbackground=COR_SURFACE, font=FONTE_LABEL)


class CampoFormulario(tk.Frame):
    def __init__(self, pai, rotulo: str, largura: int = 28, **kwargs):
        super().__init__(pai, bg=COR_SURFACE, **kwargs)
        tk.Label(self, text=rotulo, font=FONTE_LABEL_SM, bg=COR_SURFACE,
                 fg=COR_TEXTO_SOFT).pack(anchor="w")
        self.entry = tk.Entry(self, width=largura, font=FONTE_LABEL,
                              bg=COR_SURFACE, fg=COR_TEXTO,
                              relief="solid", bd=1, highlightthickness=1,
                              highlightbackground=COR_BORDA,
                              highlightcolor=COR_ACCENT)
        self.entry.pack(fill="x", pady=(2, 0))

    def get(self) -> str:
        return self.entry.get()

    def limpar(self):
        self.entry.delete(0, tk.END)


class AbaClientes(tk.Frame):
    def __init__(self, pai, controller: ClienteController):
        super().__init__(pai, bg=COR_FUNDO)
        self._ctrl = controller
        self._construir()

    def _construir(self):
        painel_form = tk.Frame(self, bg=COR_SURFACE, bd=0,
                               highlightthickness=1, highlightbackground=COR_BORDA)
        painel_form.pack(side="left", fill="y", padx=(12, 6), pady=12, ipadx=12, ipady=12)

        tk.Label(painel_form, text="Novo Cliente", font=("Segoe UI", 12, "bold"),
                 bg=COR_SURFACE, fg=COR_TEXTO).pack(anchor="w", pady=(0, 10))

        self._nome     = CampoFormulario(painel_form, "Nome completo *")
        self._nome.pack(fill="x", pady=4)
        self._cpf      = CampoFormulario(painel_form, "CPF (somente números) *")
        self._cpf.pack(fill="x", pady=4)
        self._telefone = CampoFormulario(painel_form, "Telefone *")
        self._telefone.pack(fill="x", pady=4)
        self._email    = CampoFormulario(painel_form, "E-mail")
        self._email.pack(fill="x", pady=4)

        self._msg_form = tk.Label(painel_form, text="", font=FONTE_LABEL_SM,
                                  bg=COR_SURFACE, wraplength=200, justify="left")
        self._msg_form.pack(anchor="w", pady=(6, 0))

        tk.Button(painel_form, text="Cadastrar Cliente", command=self._cadastrar,
                  bg=COR_ACCENT, fg="white", font=FONTE_BOTAO, relief="flat",
                  cursor="hand2", padx=10, pady=6,
                  activebackground=COR_ACCENT_DARK, activeforeground="white"
                  ).pack(fill="x", pady=(10, 0))

        painel_lista = tk.Frame(self, bg=COR_FUNDO)
        painel_lista.pack(side="left", fill="both", expand=True, padx=(6, 12), pady=12)

        topo = tk.Frame(painel_lista, bg=COR_FUNDO)
        topo.pack(fill="x", pady=(0, 6))
        tk.Label(topo, text="Clientes Cadastrados", font=("Segoe UI", 12, "bold"),
                 bg=COR_FUNDO, fg=COR_TEXTO).pack(side="left")
        tk.Button(topo, text="↻ Atualizar", command=self._atualizar_lista,
                  bg=COR_FUNDO, fg=COR_ACCENT, font=FONTE_LABEL_SM,
                  relief="flat", cursor="hand2").pack(side="right")

        cols = ("nome", "cpf", "telefone", "email")
        self._tree = ttk.Treeview(painel_lista, columns=cols, show="headings", selectmode="browse")
        cabecalhos = {"nome": "Nome", "cpf": "CPF", "telefone": "Telefone", "email": "E-mail"}
        larguras   = {"nome": 200, "cpf": 120, "telefone": 120, "email": 180}
        for c in cols:
            self._tree.heading(c, text=cabecalhos[c])
            self._tree.column(c, width=larguras[c], anchor="w")
        self._tree.pack(fill="both", expand=True)

        sb = ttk.Scrollbar(painel_lista, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        tk.Button(painel_lista, text="Remover selecionado", command=self._remover,
                  bg="#F5EAEA", fg=COR_ERRO, font=FONTE_LABEL_SM,
                  relief="flat", cursor="hand2", pady=4).pack(anchor="e", pady=(6, 0))

        self._atualizar_lista()

    def _cadastrar(self):
        try:
            msg = self._ctrl.cadastrar(
                self._nome.get(), self._cpf.get(),
                self._telefone.get(), self._email.get()
            )
            self._msg_form.config(text=msg, fg=COR_SUCESSO)
            for campo in (self._nome, self._cpf, self._telefone, self._email):
                campo.limpar()
            self._atualizar_lista()
        except ValueError as e:
            self._msg_form.config(text=str(e), fg=COR_ERRO)

    def _atualizar_lista(self):
        self._tree.delete(*self._tree.get_children())
        for c in self._ctrl.listar():
            self._tree.insert("", "end",
                              values=(c.get_nome(), c.get_cpf(),
                                      c.get_telefone(), c.get_email()))

    def _remover(self):
        selecionado = self._tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um cliente na lista.")
            return
        cpf = self._tree.item(selecionado[0], "values")[1]
        if messagebox.askyesno("Confirmar", f"Remover o cliente com CPF {cpf}?"):
            try:
                self._ctrl.remover(cpf)
                self._atualizar_lista()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))


class AbaQuartos(tk.Frame):
    def __init__(self, pai, controller: QuartoController):
        super().__init__(pai, bg=COR_FUNDO)
        self._ctrl = controller
        self._construir()

    def _construir(self):
        painel_form = tk.Frame(self, bg=COR_SURFACE, bd=0,
                               highlightthickness=1, highlightbackground=COR_BORDA)
        painel_form.pack(side="left", fill="y", padx=(12, 6), pady=12, ipadx=12, ipady=12)

        tk.Label(painel_form, text="Novo Quarto", font=("Segoe UI", 12, "bold"),
                 bg=COR_SURFACE, fg=COR_TEXTO).pack(anchor="w", pady=(0, 10))

        self._numero = CampoFormulario(painel_form, "Número do quarto *")
        self._numero.pack(fill="x", pady=4)

        tk.Label(painel_form, text="Tipo *", font=FONTE_LABEL_SM,
                 bg=COR_SURFACE, fg=COR_TEXTO_SOFT).pack(anchor="w", pady=(4, 0))
        self._tipo = ttk.Combobox(painel_form, values=Quarto.TIPOS,
                                   state="readonly", font=FONTE_LABEL, width=26)
        self._tipo.pack(fill="x", pady=(2, 0))

        self._valor = CampoFormulario(painel_form, "Valor da diária (R$) *")
        self._valor.pack(fill="x", pady=4)

        self._msg_form = tk.Label(painel_form, text="", font=FONTE_LABEL_SM,
                                  bg=COR_SURFACE, wraplength=200, justify="left")
        self._msg_form.pack(anchor="w", pady=(6, 0))

        tk.Button(painel_form, text="Cadastrar Quarto", command=self._cadastrar,
                  bg=COR_ACCENT, fg="white", font=FONTE_BOTAO, relief="flat",
                  cursor="hand2", padx=10, pady=6,
                  activebackground=COR_ACCENT_DARK, activeforeground="white"
                  ).pack(fill="x", pady=(10, 0))

        painel_lista = tk.Frame(self, bg=COR_FUNDO)
        painel_lista.pack(side="left", fill="both", expand=True, padx=(6, 12), pady=12)

        topo = tk.Frame(painel_lista, bg=COR_FUNDO)
        topo.pack(fill="x", pady=(0, 6))
        tk.Label(topo, text="Quartos Cadastrados", font=("Segoe UI", 12, "bold"),
                 bg=COR_FUNDO, fg=COR_TEXTO).pack(side="left")
        tk.Button(topo, text="↻ Atualizar", command=self._atualizar_lista,
                  bg=COR_FUNDO, fg=COR_ACCENT, font=FONTE_LABEL_SM,
                  relief="flat", cursor="hand2").pack(side="right")

        cols = ("numero", "tipo", "valor", "status")
        self._tree = ttk.Treeview(painel_lista, columns=cols, show="headings", selectmode="browse")
        cabecalhos = {"numero": "Número", "tipo": "Tipo", "valor": "Diária (R$)", "status": "Status"}
        larguras   = {"numero": 80, "tipo": 120, "valor": 120, "status": 100}
        for c in cols:
            self._tree.heading(c, text=cabecalhos[c])
            self._tree.column(c, width=larguras[c], anchor="w")

        self._tree.tag_configure("ocupado", foreground="#8A2020", background="#FAEAEA")
        self._tree.pack(fill="both", expand=True)

        sb = ttk.Scrollbar(painel_lista, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        tk.Button(painel_lista, text="Remover selecionado", command=self._remover,
                  bg="#F5EAEA", fg=COR_ERRO, font=FONTE_LABEL_SM,
                  relief="flat", cursor="hand2", pady=4).pack(anchor="e", pady=(6, 0))

        self._atualizar_lista()

    def _cadastrar(self):
        try:
            msg = self._ctrl.cadastrar(
                self._numero.get(), self._tipo.get(), self._valor.get()
            )
            self._msg_form.config(text=msg, fg=COR_SUCESSO)
            self._numero.limpar()
            self._tipo.set("")
            self._valor.limpar()
            self._atualizar_lista()
        except ValueError as e:
            self._msg_form.config(text=str(e), fg=COR_ERRO)

    def _atualizar_lista(self):
        self._tree.delete(*self._tree.get_children())
        for q in self._ctrl.listar():
            status = q.estado.get_current()
            tag    = () if status == "Disponível" else ("ocupado",)
            self._tree.insert("", "end",
                              values=(q.get_numero(), q.get_tipo(),
                                      f"R$ {q.get_valor_diaria():.2f}", status),
                              tags=tag)

    def _remover(self):
        selecionado = self._tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um quarto na lista.")
            return
        numero = self._tree.item(selecionado[0], "values")[0]
        if messagebox.askyesno("Confirmar", f"Remover o quarto {numero}?"):
            try:
                self._ctrl.remover(str(numero))
                self._atualizar_lista()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))


class JanelaPrincipal(tk.Tk):
    def __init__(self, cliente_ctrl: ClienteController, quarto_ctrl: QuartoController):
        super().__init__()
        self.title("Sistema de Gestão de Hotel")
        self.geometry("820x520")
        self.minsize(720, 480)
        self.configure(bg=COR_FUNDO)
        _configurar_estilo()
        self._construir(cliente_ctrl, quarto_ctrl)

    def _construir(self, cliente_ctrl, quarto_ctrl):
        header = tk.Frame(self, bg=COR_ACCENT, height=52)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🏨  Sistema de Gestão de Hotel",
                 font=("Segoe UI", 14, "bold"), bg=COR_ACCENT,
                 fg="white").pack(side="left", padx=16, pady=12)
        tk.Label(header, text="Protótipo MVC · Tkinter",
                 font=FONTE_LABEL_SM, bg=COR_ACCENT,
                 fg="#A8C8E8").pack(side="right", padx=16)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        aba_clientes = AbaClientes(notebook, cliente_ctrl)
        notebook.add(aba_clientes, text="  👤  Clientes  ")

        aba_quartos = AbaQuartos(notebook, quarto_ctrl)
        notebook.add(aba_quartos, text="  🛏  Quartos  ")
