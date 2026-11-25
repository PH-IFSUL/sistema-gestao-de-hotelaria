import calendar
from datetime import date
import tkinter as tk
from ..estilo.constantes import CoresTema, FontesTema


class JanelaCalendario(tk.Toplevel):
    """Janela modal compacta para selecionar uma data no calendário."""

    _MESES = (
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    )
    _DIAS_SEMANA = ("Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom")

    def __init__(
        self,
        pai: tk.Misc,
        data_inicial: date | None = None,
        titulo: str = "Selecionar Data"
    ) -> None:
        super().__init__(pai)
        referencia = data_inicial if data_inicial is not None else date.today()
        self._ano = referencia.year
        self._mes = referencia.month
        self._data_inicial = data_inicial
        self.data_selecionada: date | None = None

        self.title(titulo)
        self.resizable(False, False)
        self.configure(bg=CoresTema.COR_FUNDO)

        self._construir()
        self._renderizar_mes()

        self.transient(pai.winfo_toplevel())
        self.grab_set()
        self._centralizar(pai.winfo_toplevel())
        self.bind("<Escape>", lambda _e: self._cancelar())
        self.protocol("WM_DELETE_WINDOW", self._cancelar)

    def _construir(self) -> None:
        container = tk.Frame(
            self,
            bg=CoresTema.COR_SURFACE,
            highlightthickness=1,
            highlightbackground=CoresTema.COR_BORDA
        )
        container.pack(fill="both", expand=True, padx=10, pady=10, ipadx=8, ipady=8)

        cabecalho = tk.Frame(container, bg=CoresTema.COR_SURFACE)
        cabecalho.pack(fill="x", pady=(0, 8))

        tk.Button(
            cabecalho,
            text="‹",
            command=self._mes_anterior,
            bg=CoresTema.COR_FUNDO,
            fg=CoresTema.COR_TEXTO,
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            cursor="hand2",
            width=3
        ).pack(side="left")

        self._lbl_mes = tk.Label(
            cabecalho,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO
        )
        self._lbl_mes.pack(side="left", expand=True)

        tk.Button(
            cabecalho,
            text="›",
            command=self._proximo_mes,
            bg=CoresTema.COR_FUNDO,
            fg=CoresTema.COR_TEXTO,
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            cursor="hand2",
            width=3
        ).pack(side="right")

        self._grade = tk.Frame(container, bg=CoresTema.COR_SURFACE)
        self._grade.pack()

        rodape = tk.Frame(container, bg=CoresTema.COR_SURFACE)
        rodape.pack(fill="x", pady=(8, 0))

        tk.Button(
            rodape,
            text="Hoje",
            command=lambda: self._selecionar(date.today()),
            bg=CoresTema.COR_FUNDO,
            fg=CoresTema.COR_ACCENT,
            font=FontesTema.FONTE_LABEL_SM,
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=2
        ).pack(side="left")

        tk.Button(
            rodape,
            text="Cancelar",
            command=self._cancelar,
            bg=CoresTema.COR_BORDA,
            fg=CoresTema.COR_TEXTO,
            font=FontesTema.FONTE_LABEL_SM,
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=2
        ).pack(side="right")

    def _renderizar_mes(self) -> None:
        for widget in self._grade.winfo_children():
            widget.destroy()

        self._lbl_mes.config(text=f"{self._MESES[self._mes - 1]} {self._ano}")

        for col, nome_dia in enumerate(self._DIAS_SEMANA):
            tk.Label(
                self._grade,
                text=nome_dia,
                font=FontesTema.FONTE_LABEL_SM,
                bg=CoresTema.COR_SURFACE,
                fg=CoresTema.COR_TEXTO_SOFT,
                width=4
            ).grid(row=0, column=col, padx=1, pady=2)

        semanas = calendar.monthcalendar(self._ano, self._mes)
        hoje = date.today()
        for row_idx, semana in enumerate(semanas, start=1):
            for col_idx, dia in enumerate(semana):
                if dia == 0:
                    tk.Label(
                        self._grade,
                        text="",
                        bg=CoresTema.COR_SURFACE,
                        width=4
                    ).grid(row=row_idx, column=col_idx, padx=1, pady=1)
                    continue

                data_btn = date(self._ano, self._mes, dia)
                selecionado = data_btn == self._data_inicial
                eh_hoje = data_btn == hoje

                bg = CoresTema.COR_ACCENT if selecionado else (
                    "#E6EFF8" if eh_hoje else CoresTema.COR_FUNDO
                )
                fg = "white" if selecionado else CoresTema.COR_TEXTO

                tk.Button(
                    self._grade,
                    text=str(dia),
                    command=lambda d=data_btn: self._selecionar(d),
                    bg=bg,
                    fg=fg,
                    font=FontesTema.FONTE_LABEL_SM,
                    relief="flat",
                    cursor="hand2",
                    width=4,
                    pady=2,
                    activebackground=CoresTema.COR_ACCENT_DARK,
                    activeforeground="white"
                ).grid(row=row_idx, column=col_idx, padx=1, pady=1)

    def _mes_anterior(self) -> None:
        if self._mes == 1:
            self._mes = 12
            self._ano -= 1
        else:
            self._mes -= 1
        self._renderizar_mes()

    def _proximo_mes(self) -> None:
        if self._mes == 12:
            self._mes = 1
            self._ano += 1
        else:
            self._mes += 1
        self._renderizar_mes()

    def _selecionar(self, data_escolhida: date) -> None:
        self.data_selecionada = data_escolhida
        self.destroy()

    def _cancelar(self) -> None:
        self.data_selecionada = None
        self.destroy()

    def _centralizar(self, janela_pai: tk.Misc) -> None:
        self.update_idletasks()
        largura = self.winfo_width()
        altura = self.winfo_height()
        x = janela_pai.winfo_rootx() + (janela_pai.winfo_width() - largura) // 2
        y = janela_pai.winfo_rooty() + (janela_pai.winfo_height() - altura) // 2
        self.geometry(f"+{max(0, x)}+{max(0, y)}")
