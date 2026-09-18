import tkinter as tk
from tkinter import ttk, messagebox
from controllers.cliente_controller import ClienteController
from views.style.constants import TmColors, TmFonts
from views.forms.form import CampoFormulario


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
