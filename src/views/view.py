import tkinter as tk
from tkinter import ttk, messagebox
from controllers.quarto_controller import QuartoController
from controllers.cliente_controller import ClienteController
from models.room.room import Quarto
from .style.constants import TmColors, TmFonts


class CampoFormulario(tk.Frame):
    def __init__(self, pai, rotulo: str, largura: int = 28, **kwargs):
        super().__init__(pai, bg=TmColors.COR_SURFACE, **kwargs)
        tk.Label(self, text=rotulo, font=TmFonts.FONTE_LABEL_SM, bg=TmColors.COR_SURFACE,
                 fg=TmColors.COR_TEXTO_SOFT).pack(anchor="w")
        self.entry = tk.Entry(self, width=largura, font=TmFonts.FONTE_LABEL,
                              bg=TmColors.COR_SURFACE, fg=TmColors.COR_TEXTO,
                              relief="solid", bd=1, highlightthickness=1,
                              highlightbackground=TmColors.COR_BORDA,
                              highlightcolor=TmColors.COR_ACCENT)
        self.entry.pack(fill="x", pady=(2, 0))

    def get(self) -> str:
        return self.entry.get()

    def limpar(self):
        self.entry.delete(0, tk.END)


class AbaClientes(tk.Frame):
    def __init__(self, pai, controller: ClienteController):
        super().__init__(pai, bg=TmColors.COR_FUNDO)
        self._ctrl = controller
        self._construir()

    def _construir(self):
        painel_form = tk.Frame(self, bg=TmColors.COR_SURFACE, bd=0,
                               highlightthickness=1, highlightbackground=TmColors.COR_BORDA)
        painel_form.pack(side="left", fill="y", padx=(12, 6), pady=12, ipadx=12, ipady=12)

        tk.Label(painel_form, text="Novo Cliente", font=("Segoe UI", 12, "bold"),
                 bg=TmColors.COR_SURFACE, fg=TmColors.COR_TEXTO).pack(anchor="w", pady=(0, 10))

        self._nome     = CampoFormulario(painel_form, "Nome completo *")
        self._nome.pack(fill="x", pady=4)
        self._cpf      = CampoFormulario(painel_form, "CPF (somente números) *")
        self._cpf.pack(fill="x", pady=4)
        self._telefone = CampoFormulario(painel_form, "Telefone *")
        self._telefone.pack(fill="x", pady=4)
        self._email    = CampoFormulario(painel_form, "E-mail")
        self._email.pack(fill="x", pady=4)

        self._msg_form = tk.Label(painel_form, text="", font=TmFonts.FONTE_LABEL_SM,
                                  bg=TmColors.COR_SURFACE, wraplength=200, justify="left")
        self._msg_form.pack(anchor="w", pady=(6, 0))

        tk.Button(painel_form, text="Cadastrar Cliente", command=self._cadastrar,
                  bg=TmColors.COR_ACCENT, fg="white", font=TmFonts.FONTE_BOTAO, relief="flat",
                  cursor="hand2", padx=10, pady=6,
                  activebackground=TmColors.COR_ACCENT_DARK, activeforeground="white"
                  ).pack(fill="x", pady=(10, 0))

        painel_lista = tk.Frame(self, bg=TmColors.COR_FUNDO)
        painel_lista.pack(side="left", fill="both", expand=True, padx=(6, 12), pady=12)

        topo = tk.Frame(painel_lista, bg=TmColors.COR_FUNDO)
        topo.pack(fill="x", pady=(0, 6))
        tk.Label(topo, text="Clientes Cadastrados", font=("Segoe UI", 12, "bold"),
                 bg=TmColors.COR_FUNDO, fg=TmColors.COR_TEXTO).pack(side="left")
        tk.Button(topo, text="↻ Atualizar", command=self._atualizar_lista,
                  bg=TmColors.COR_FUNDO, fg=TmColors.COR_ACCENT, font=TmFonts.FONTE_LABEL_SM,
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
                  bg="#F5EAEA", fg=TmColors.COR_ERRO, font=TmFonts.FONTE_LABEL_SM,
                  relief="flat", cursor="hand2", pady=4).pack(anchor="e", pady=(6, 0))

        self._atualizar_lista()

    def _cadastrar(self):
        try:
            msg = self._ctrl.cadastrar(
                self._nome.get(), self._cpf.get(),
                self._telefone.get(), self._email.get()
            )
            self._msg_form.config(text=msg, fg=TmColors.COR_SUCESSO)
            for campo in (self._nome, self._cpf, self._telefone, self._email):
                campo.limpar()
            self._atualizar_lista()
        except ValueError as e:
            self._msg_form.config(text=str(e), fg=TmColors.COR_ERRO)

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
        super().__init__(pai, bg=TmColors.COR_FUNDO)
        self._ctrl = controller
        self._construir()

    def _construir(self):
        painel_form = tk.Frame(self, bg=TmColors.COR_SURFACE, bd=0,
                               highlightthickness=1, highlightbackground=TmColors.COR_BORDA)
        painel_form.pack(side="left", fill="y", padx=(12, 6), pady=12, ipadx=12, ipady=12)

        tk.Label(painel_form, text="Novo Quarto", font=("Segoe UI", 12, "bold"),
                 bg=TmColors.COR_SURFACE, fg=TmColors.COR_TEXTO).pack(anchor="w", pady=(0, 10))

        self._numero = CampoFormulario(painel_form, "Número do quarto *")
        self._numero.pack(fill="x", pady=4)

        tk.Label(painel_form, text="Tipo *", font=TmFonts.FONTE_LABEL_SM,
                 bg=TmColors.COR_SURFACE, fg=TmColors.COR_TEXTO_SOFT).pack(anchor="w", pady=(4, 0))
        self._tipo = ttk.Combobox(painel_form, values=Quarto.TIPOS,
                                   state="readonly", font=TmFonts.FONTE_LABEL, width=26)
        self._tipo.pack(fill="x", pady=(2, 0))

        self._valor = CampoFormulario(painel_form, "Valor da diária (R$) *")
        self._valor.pack(fill="x", pady=4)

        self._msg_form = tk.Label(painel_form, text="", font=TmFonts.FONTE_LABEL_SM,
                                  bg=TmColors.COR_SURFACE, wraplength=200, justify="left")
        self._msg_form.pack(anchor="w", pady=(6, 0))

        tk.Button(painel_form, text="Cadastrar Quarto", command=self._cadastrar,
                  bg=TmColors.COR_ACCENT, fg="white", font=TmFonts.FONTE_BOTAO, relief="flat",
                  cursor="hand2", padx=10, pady=6,
                  activebackground=TmColors.COR_ACCENT_DARK, activeforeground="white"
                  ).pack(fill="x", pady=(10, 0))

        painel_lista = tk.Frame(self, bg=TmColors.COR_FUNDO)
        painel_lista.pack(side="left", fill="both", expand=True, padx=(6, 12), pady=12)

        topo = tk.Frame(painel_lista, bg=TmColors.COR_FUNDO)
        topo.pack(fill="x", pady=(0, 6))
        tk.Label(topo, text="Quartos Cadastrados", font=("Segoe UI", 12, "bold"),
                 bg=TmColors.COR_FUNDO, fg=TmColors.COR_TEXTO).pack(side="left")
        tk.Button(topo, text="↻ Atualizar", command=self._atualizar_lista,
                  bg=TmColors.COR_FUNDO, fg=TmColors.COR_ACCENT, font=TmFonts.FONTE_LABEL_SM,
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
                  bg="#F5EAEA", fg=TmColors.COR_ERRO, font=TmFonts.FONTE_LABEL_SM,
                  relief="flat", cursor="hand2", pady=4).pack(anchor="e", pady=(6, 0))

        self._atualizar_lista()

    def _cadastrar(self):
        try:
            msg = self._ctrl.cadastrar(
                self._numero.get(), self._tipo.get(), self._valor.get()
            )
            self._msg_form.config(text=msg, fg=TmColors.COR_SUCESSO)
            self._numero.limpar()
            self._tipo.set("")
            self._valor.limpar()
            self._atualizar_lista()
        except ValueError as e:
            self._msg_form.config(text=str(e), fg=TmColors.COR_ERRO)

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



