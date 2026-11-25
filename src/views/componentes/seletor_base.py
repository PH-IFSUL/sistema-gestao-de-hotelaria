from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, Callable, Generic, TypeVar
from ..estilo.constantes import CoresTema, FontesTema

T = TypeVar("T")


@dataclass(frozen=True)
class ColunaSeletor:
    """Definição de uma coluna da tabela de seleção."""
    chave: str
    titulo: str
    largura: int


class JanelaSeletorBase(tk.Toplevel, Generic[T]):
    """Janela modal base reutilizável para pesquisa e seleção de registros."""

    def __init__(
        self,
        pai: tk.Misc,
        buscar_itens: Callable[[str], list[T]],
        colunas: tuple[ColunaSeletor, ...],
        titulo: str,
        cabecalho: str,
        rotulo_busca: str,
        singular: str = "item",
        plural: str = "itens",
        mensagem_selecao_vazia: str = "Selecione um item na lista.",
        geometria: str = "600x420",
        largura_min: int = 500,
        altura_min: int = 340
    ) -> None:
        super().__init__(pai)
        self._buscar_itens = buscar_itens
        self._colunas = colunas
        self._cabecalho = cabecalho
        self._rotulo_busca = rotulo_busca
        self._singular = singular
        self._plural = plural
        self._mensagem_selecao_vazia = mensagem_selecao_vazia
        self._itens_por_iid: dict[str, T] = {}
        self.item_selecionado: T | None = None

        self.title(titulo)
        self.geometry(geometria)
        self.minsize(largura_min, altura_min)
        self.configure(bg=CoresTema.COR_FUNDO)

        self._construir()
        self._carregar_itens()

        self.transient(pai.winfo_toplevel())
        self.grab_set()
        self._centralizar(pai.winfo_toplevel())
        self._entry_busca.focus_set()

        self.bind("<Escape>", lambda _e: self._cancelar())
        self.protocol("WM_DELETE_WINDOW", self._cancelar)

    def _construir(self) -> None:
        container = tk.Frame(self, bg=CoresTema.COR_FUNDO)
        container.pack(fill="both", expand=True, padx=14, pady=14)

        tk.Label(
            container,
            text=self._cabecalho,
            font=("Segoe UI", 12, "bold"),
            bg=CoresTema.COR_FUNDO,
            fg=CoresTema.COR_TEXTO
        ).pack(anchor="w", pady=(0, 8))

        barra_busca = tk.Frame(
            container,
            bg=CoresTema.COR_SURFACE,
            highlightthickness=1,
            highlightbackground=CoresTema.COR_BORDA
        )
        barra_busca.pack(fill="x", pady=(0, 10), ipadx=8, ipady=8)

        tk.Label(
            barra_busca,
            text=self._rotulo_busca,
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO_SOFT
        ).pack(side="left", padx=(4, 8))

        self._var_busca = tk.StringVar()
        self._entry_busca = tk.Entry(
            barra_busca,
            textvariable=self._var_busca,
            font=FontesTema.FONTE_LABEL,
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=CoresTema.COR_BORDA,
            highlightcolor=CoresTema.COR_ACCENT
        )
        self._entry_busca.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self._entry_busca.bind("<KeyRelease>", lambda _e: self._carregar_itens())
        self._entry_busca.bind("<Return>", self._ao_pressionar_enter)

        tk.Button(
            barra_busca,
            text="Limpar",
            command=self._limpar_busca,
            bg=CoresTema.COR_FUNDO,
            fg=CoresTema.COR_TEXTO_SOFT,
            font=FontesTema.FONTE_LABEL_SM,
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=3
        ).pack(side="right", padx=(0, 4))

        self._construir_filtros_extras(container)

        frame_lista = tk.Frame(container, bg=CoresTema.COR_FUNDO)
        frame_lista.pack(fill="both", expand=True)

        chaves = [col.chave for col in self._colunas]
        self._tree = ttk.Treeview(
            frame_lista,
            columns=chaves,
            show="headings",
            selectmode="browse"
        )
        for col in self._colunas:
            self._tree.heading(col.chave, text=col.titulo)
            self._tree.column(col.chave, width=col.largura, anchor="w")

        self._configurar_treeview(self._tree)

        sb = ttk.Scrollbar(frame_lista, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=sb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self._tree.bind("<Double-1>", lambda _e: self._confirmar())

        rodape = tk.Frame(container, bg=CoresTema.COR_FUNDO)
        rodape.pack(fill="x", pady=(10, 0))

        self._lbl_status = tk.Label(
            rodape,
            text="",
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_FUNDO,
            fg=CoresTema.COR_TEXTO_SOFT
        )
        self._lbl_status.pack(side="left")

        tk.Button(
            rodape,
            text="Selecionar",
            command=self._confirmar,
            bg=CoresTema.COR_ACCENT,
            fg="white",
            font=FontesTema.FONTE_BOTAO,
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=5,
            activebackground=CoresTema.COR_ACCENT_DARK,
            activeforeground="white"
        ).pack(side="right")

        tk.Button(
            rodape,
            text="Cancelar",
            command=self._cancelar,
            bg=CoresTema.COR_BORDA,
            fg=CoresTema.COR_TEXTO,
            font=FontesTema.FONTE_LABEL,
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=5
        ).pack(side="right", padx=(0, 8))

    def _construir_filtros_extras(self, _container: tk.Frame) -> None:
        """Ponto de extensão para subclasses adicionarem filtros adicionais."""

    def _configurar_treeview(self, _tree: ttk.Treeview) -> None:
        """Ponto de extensão para subclasses configurarem tags ou estilos da Treeview."""

    def _extrair_valores(self, item: T) -> tuple[Any, ...]:
        raise NotImplementedError

    def _obter_tags(self, _item: T) -> tuple[str, ...]:
        return ()

    def _carregar_itens(self) -> None:
        self._tree.delete(*self._tree.get_children())
        self._itens_por_iid.clear()

        filtro = self._var_busca.get()
        itens = self._buscar_itens(filtro)

        for item in itens:
            iid = self._tree.insert(
                "",
                "end",
                values=self._extrair_valores(item),
                tags=self._obter_tags(item)
            )
            self._itens_por_iid[iid] = item

        total = len(itens)
        if total == 0:
            self._lbl_status.config(text=f"Nenhum {self._singular} encontrado.")
        elif total == 1:
            self._lbl_status.config(text=f"1 {self._singular} encontrado.")
        else:
            self._lbl_status.config(text=f"{total} {self._plural} encontrados.")

    def _limpar_busca(self) -> None:
        self._var_busca.set("")
        self._carregar_itens()
        self._entry_busca.focus_set()

    def _ao_pressionar_enter(self, _evento: tk.Event) -> None:
        itens = self._tree.get_children()
        if not self._tree.selection() and len(itens) == 1:
            self._tree.selection_set(itens[0])
        if self._tree.selection():
            self._confirmar()

    def _confirmar(self) -> None:
        selecao = self._tree.selection()
        if not selecao:
            messagebox.showwarning(
                "Atenção",
                self._mensagem_selecao_vazia,
                parent=self
            )
            return
        self.item_selecionado = self._itens_por_iid.get(selecao[0])
        self.destroy()

    def _cancelar(self) -> None:
        self.item_selecionado = None
        self.destroy()

    def _centralizar(self, janela_pai: tk.Misc) -> None:
        self.update_idletasks()
        largura = self.winfo_width()
        altura = self.winfo_height()
        x = janela_pai.winfo_rootx() + (janela_pai.winfo_width() - largura) // 2
        y = janela_pai.winfo_rooty() + (janela_pai.winfo_height() - altura) // 2
        self.geometry(f"+{max(0, x)}+{max(0, y)}")
