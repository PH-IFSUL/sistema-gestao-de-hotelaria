import tkinter as tk
from tkinter import ttk, messagebox
from models.quarto import Quarto
from controllers.quarto_controller import QuartoController
from .estilo.constantes import CoresTema, FontesTema
from .componentes.formulario import CampoFormulario


class AbaQuartos(tk.Frame):
    """
    Classe que representa a aba de quartos.
    """

    def __init__(self, pai, controller: QuartoController):
        super().__init__(pai, bg=CoresTema.COR_FUNDO)
        self._ctrl = controller
        self._construir()

    def _construir(self):
        painel_form = tk.Frame(
            self,
            bg=CoresTema.COR_SURFACE,
            bd=0,
            highlightthickness=1,
            highlightbackground=CoresTema.COR_BORDA
        )
        painel_form.pack(side="left", fill="y", padx=(12, 6), pady=12, ipadx=12, ipady=12)

        tk.Label(
            painel_form,
            text="Novo Quarto",
            font=("Segoe UI", 12, "bold"),
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO
        ).pack(anchor="w", pady=(0, 10))

        self._numero = CampoFormulario(painel_form, "Número do quarto *")
        self._numero.pack(fill="x", pady=4)

        tk.Label(
            painel_form,
            text="Tipo *",
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO_SOFT
        ).pack(anchor="w", pady=(4, 0))

        self._tipo = ttk.Combobox(
            painel_form,
            values=Quarto.TIPOS,
            state="readonly",
            font=FontesTema.FONTE_LABEL,
            width=26
        )
        self._tipo.pack(fill="x", pady=(2, 0))

        self._valor = CampoFormulario(painel_form, "Valor da diária (R$) *")
        self._valor.pack(fill="x", pady=4)

        self._msg_form = tk.Label(
            painel_form,
            text="",
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_SURFACE,
            wraplength=200,
            justify="left"
        )
        self._msg_form.pack(anchor="w", pady=(6, 0))

        tk.Button(
            painel_form,
            text="Cadastrar Quarto",
            command=self._cadastrar,
            bg=CoresTema.COR_ACCENT,
            fg="white",
            font=FontesTema.FONTE_BOTAO,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            activebackground=CoresTema.COR_ACCENT_DARK,
            activeforeground="white"
        ).pack(fill="x", pady=(10, 0))

        painel_lista = tk.Frame(self, bg=CoresTema.COR_FUNDO)
        painel_lista.pack(side="left", fill="both", expand=True, padx=(6, 12), pady=12)

        topo = tk.Frame(painel_lista, bg=CoresTema.COR_FUNDO)
        topo.pack(fill="x", pady=(0, 6))
        tk.Label(
            topo,
            text="Quartos Cadastrados",
            font=("Segoe UI", 12, "bold"),
            bg=CoresTema.COR_FUNDO,
            fg=CoresTema.COR_TEXTO
        ).pack(side="left")
        tk.Button(
            topo,
            text="↻ Atualizar",
            command=self._atualizar_lista,
            bg=CoresTema.COR_FUNDO,
            fg=CoresTema.COR_ACCENT,
            font=FontesTema.FONTE_LABEL_SM,
            relief="flat",
            cursor="hand2"
        ).pack(side="right")

        frame_tree = tk.Frame(painel_lista, bg=CoresTema.COR_FUNDO)
        frame_tree.pack(fill="both", expand=True)

        cols = ("numero", "tipo", "valor", "status")
        self._tree = ttk.Treeview(frame_tree, columns=cols, show="headings", selectmode="browse")
        cabecalhos = {"numero": "Número", "tipo": "Tipo", "valor": "Diária (R$)", "status": "Status"}
        larguras = {"numero": 80, "tipo": 120, "valor": 120, "status": 115}
        for c in cols:
            self._tree.heading(c, text=cabecalhos[c])
            self._tree.column(c, width=larguras[c], anchor="w")

        self._tree.tag_configure("ocupado", foreground="#8A2020", background="#FAEAEA")
        self._tree.tag_configure("limpeza", foreground="#8A5A00", background="#FDF4E3")

        sb = ttk.Scrollbar(frame_tree, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=sb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self._tree.bind("<Double-1>", lambda _e: self._editar_status())

        barra_acoes = tk.Frame(painel_lista, bg=CoresTema.COR_FUNDO)
        barra_acoes.pack(fill="x", pady=(6, 0))

        tk.Button(
            barra_acoes,
            text="Remover selecionado",
            command=self._remover,
            bg="#F5EAEA",
            fg=CoresTema.COR_ERRO,
            font=FontesTema.FONTE_LABEL_SM,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4
        ).pack(side="right")

        tk.Button(
            barra_acoes,
            text="Editar status",
            command=self._editar_status,
            bg="#E6EFF8",
            fg=CoresTema.COR_ACCENT_DARK,
            font=FontesTema.FONTE_LABEL_SM,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4
        ).pack(side="right", padx=(0, 8))


        self._atualizar_lista()

    def _cadastrar(self):
        try:
            msg = self._ctrl.cadastrar(
                self._numero.get(),
                self._tipo.get(),
                self._valor.get()
            )
            self._msg_form.config(text=msg, fg=CoresTema.COR_SUCESSO)
            self._numero.limpar()
            self._tipo.set("")
            self._valor.limpar()
            self._atualizar_lista()
        except ValueError as e:
            self._msg_form.config(text=str(e), fg=CoresTema.COR_ERRO)

    def _atualizar_lista(self):
        self._tree.delete(*self._tree.get_children())
        for q in self._ctrl.listar():
            status = q.estado.obter_atual()
            if status == "Disponível":
                tag = ()
            elif status == "Em Limpeza":
                tag = ("limpeza",)
            else:
                tag = ("ocupado",)
            self._tree.insert(
                "",
                "end",
                values=(
                    q.get_numero(),
                    q.get_tipo(),
                    f"R$ {q.get_valor_diaria():.2f}",
                    status
                ),
                tags=tag
            )

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

    def _editar_status(self):
        selecionado = self._tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um quarto na lista.")
            return

        valores = self._tree.item(selecionado[0], "values")
        numero = str(valores[0])
        status_atual = str(valores[3])

        popup = tk.Toplevel(self)
        popup.title(f"Alterar Status - Quarto {numero}")
        popup.resizable(False, False)
        popup.configure(bg=CoresTema.COR_FUNDO)

        container = tk.Frame(
            popup,
            bg=CoresTema.COR_SURFACE,
            highlightthickness=1,
            highlightbackground=CoresTema.COR_BORDA
        )
        container.pack(fill="both", expand=True, padx=12, pady=12, ipadx=12, ipady=10)

        tk.Label(
            container,
            text=f"Quarto {numero}",
            font=("Segoe UI", 11, "bold"),
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO
        ).pack(anchor="w")

        tk.Label(
            container,
            text=f"Status atual: {status_atual}",
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO_SOFT
        ).pack(anchor="w", pady=(2, 10))

        tk.Label(
            container,
            text="Novo status *",
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO_SOFT
        ).pack(anchor="w")

        combo_status = ttk.Combobox(
            container,
            values=self._ctrl.ESTADOS_DISPONIVEIS,
            state="readonly",
            font=FontesTema.FONTE_LABEL,
            width=24
        )
        combo_status.set(status_atual)
        combo_status.pack(fill="x", pady=(2, 12))

        botoes = tk.Frame(container, bg=CoresTema.COR_SURFACE)
        botoes.pack(fill="x")

        def _confirmar():
            try:
                msg = self._ctrl.alterar_estado(numero, combo_status.get())
                self._atualizar_lista()
                self._msg_form.config(text=msg, fg=CoresTema.COR_SUCESSO)
                popup.destroy()
            except ValueError as e:
                messagebox.showerror("Erro", str(e), parent=popup)

        tk.Button(
            botoes,
            text="Salvar",
            command=_confirmar,
            bg=CoresTema.COR_ACCENT,
            fg="white",
            font=FontesTema.FONTE_BOTAO,
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=4,
            activebackground=CoresTema.COR_ACCENT_DARK,
            activeforeground="white"
        ).pack(side="right")

        tk.Button(
            botoes,
            text="Cancelar",
            command=popup.destroy,
            bg=CoresTema.COR_BORDA,
            fg=CoresTema.COR_TEXTO,
            font=FontesTema.FONTE_LABEL,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4
        ).pack(side="right", padx=(0, 8))

        popup.transient(self.winfo_toplevel())
        popup.grab_set()
        popup.update_idletasks()
        janela_pai = self.winfo_toplevel()
        x = janela_pai.winfo_rootx() + (janela_pai.winfo_width() - popup.winfo_width()) // 2
        y = janela_pai.winfo_rooty() + (janela_pai.winfo_height() - popup.winfo_height()) // 2
        popup.geometry(f"+{max(0, x)}+{max(0, y)}")
        popup.bind("<Escape>", lambda _e: popup.destroy())
        popup.bind("<Return>", lambda _e: _confirmar())