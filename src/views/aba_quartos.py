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

        cols = ("numero", "tipo", "valor", "status")
        self._tree = ttk.Treeview(painel_lista, columns=cols, show="headings", selectmode="browse")
        cabecalhos = {"numero": "Número", "tipo": "Tipo", "valor": "Diária (R$)", "status": "Status"}
        larguras = {"numero": 80, "tipo": 120, "valor": 120, "status": 100}
        for c in cols:
            self._tree.heading(c, text=cabecalhos[c])
            self._tree.column(c, width=larguras[c], anchor="w")

        self._tree.tag_configure("ocupado", foreground="#8A2020", background="#FAEAEA")
        self._tree.pack(fill="both", expand=True)

        sb = ttk.Scrollbar(painel_lista, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        tk.Button(
            painel_lista,
            text="Remover selecionado",
            command=self._remover,
            bg="#F5EAEA",
            fg=CoresTema.COR_ERRO,
            font=FontesTema.FONTE_LABEL_SM,
            relief="flat",
            cursor="hand2",
            pady=4
        ).pack(anchor="e", pady=(6, 0))

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
            tag = () if status == "Disponível" else ("ocupado",)
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
