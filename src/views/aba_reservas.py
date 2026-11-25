from datetime import date, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable
from controllers.estadia_controller import EstadiaController
from models.cliente import Cliente
from models.estadia import Reserva
from models.quarto import Quarto
from .componentes.seletor_cliente import JanelaSelecionarCliente
from .componentes.seletor_data import JanelaCalendario
from .componentes.seletor_quarto import JanelaSelecionarQuarto
from .estilo.constantes import CoresTema, FontesTema


class AbaReservas(tk.Frame):
    """Aba para criação, listagem, alteração e exclusão de reservas."""

    def __init__(self, parent, stay_ctrl: EstadiaController):
        super().__init__(parent, bg=CoresTema.COR_FUNDO)
        self._controller = stay_ctrl
        self._cliente_selecionado: Cliente | None = None
        self._quarto_selecionado: Quarto | None = None
        self._reserva_em_edicao_id: int | None = None
        self._reservas_por_iid: dict[str, Reserva] = {}
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

        self._lbl_titulo_form = tk.Label(
            painel_form,
            text="Nova Reserva",
            font=("Segoe UI", 12, "bold"),
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO
        )
        self._lbl_titulo_form.pack(anchor="w", pady=(0, 10))

        self._lbl_cliente = self._criar_campo_selecao(
            painel_form,
            rotulo="Cliente *",
            texto_padrao="Nenhum cliente selecionado",
            texto_botao="Selecionar Cliente",
            comando=self._popup_pesquisa
        )

        self._lbl_quarto = self._criar_campo_selecao(
            painel_form,
            rotulo="Quarto *",
            texto_padrao="Nenhum quarto selecionado",
            texto_botao="Selecionar Quarto",
            comando=self._popup_quarto
        )

        linha_datas = tk.Frame(painel_form, bg=CoresTema.COR_SURFACE)
        linha_datas.pack(fill="x", pady=(0, 6))

        hoje = date.today()
        self._var_checkin = tk.StringVar(value=hoje.strftime("%d/%m/%Y"))
        self._var_checkout = tk.StringVar(value=(hoje + timedelta(days=1)).strftime("%d/%m/%Y"))

        self._entry_checkin = self._criar_campo_data(
            linha_datas,
            rotulo="Check-in *",
            variavel=self._var_checkin,
            coluna=0,
            padx=(0, 6)
        )
        self._entry_checkout = self._criar_campo_data(
            linha_datas,
            rotulo="Check-out *",
            variavel=self._var_checkout,
            coluna=1,
            padx=(6, 0)
        )
        linha_datas.columnconfigure(0, weight=1)
        linha_datas.columnconfigure(1, weight=1)

        self._var_checkin.trace_add("write", lambda *_: self._atualizar_resumo())
        self._var_checkout.trace_add("write", lambda *_: self._atualizar_resumo())

        self._lbl_resumo = tk.Label(
            painel_form,
            text="",
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO_SOFT,
            anchor="w"
        )
        self._lbl_resumo.pack(fill="x", pady=(2, 4))

        self._msg_form = tk.Label(
            painel_form,
            text="",
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_SURFACE,
            wraplength=220,
            justify="left"
        )
        self._msg_form.pack(anchor="w", pady=(2, 0))

        self._btn_salvar = tk.Button(
            painel_form,
            text="Cadastrar Reserva",
            command=self._salvar_reserva,
            bg=CoresTema.COR_ACCENT,
            fg="white",
            font=FontesTema.FONTE_BOTAO,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            activebackground=CoresTema.COR_ACCENT_DARK,
            activeforeground="white"
        )
        self._btn_salvar.pack(fill="x", pady=(8, 0))

        self._btn_cancelar_edicao = tk.Button(
            painel_form,
            text="Cancelar alteração",
            command=self._limpar_formulario,
            bg=CoresTema.COR_BORDA,
            fg=CoresTema.COR_TEXTO,
            font=FontesTema.FONTE_LABEL_SM,
            relief="flat",
            cursor="hand2",
            pady=4
        )

        # Painel direito (listagem no mesmo estilo das abas Clientes e Quartos)
        painel_lista = tk.Frame(self, bg=CoresTema.COR_FUNDO)
        painel_lista.pack(side="left", fill="both", expand=True, padx=(6, 12), pady=12)

        topo = tk.Frame(painel_lista, bg=CoresTema.COR_FUNDO)
        topo.pack(fill="x", pady=(0, 6))
        tk.Label(
            topo,
            text="Reservas Cadastradas",
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

        cols = ("id", "cliente", "quarto", "checkin", "checkout", "total", "status")
        self._tree = ttk.Treeview(
            frame_tree,
            columns=cols,
            show="headings",
            selectmode="browse"
        )
        cabecalhos = {
            "id": "#",
            "cliente": "Cliente",
            "quarto": "Quarto",
            "checkin": "Check-in",
            "checkout": "Check-out",
            "total": "Total (R$)",
            "status": "Status",
        }
        larguras = {
            "id": 36,
            "cliente": 135,
            "quarto": 70,
            "checkin": 82,
            "checkout": 82,
            "total": 82,
            "status": 88,
        }
        for c in cols:
            self._tree.heading(c, text=cabecalhos[c])
            self._tree.column(c, width=larguras[c], anchor="w")

        sb = ttk.Scrollbar(frame_tree, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=sb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self._tree.bind("<Double-1>", lambda _e: self._iniciar_edicao())

        barra_acoes = tk.Frame(painel_lista, bg=CoresTema.COR_FUNDO)
        barra_acoes.pack(fill="x", pady=(6, 0))

        tk.Button(
            barra_acoes,
            text="Excluir selecionada",
            command=self._excluir_selecionada,
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
            text="Alterar selecionada",
            command=self._iniciar_edicao,
            bg="#E6EFF8",
            fg=CoresTema.COR_ACCENT_DARK,
            font=FontesTema.FONTE_LABEL_SM,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4
        ).pack(side="right", padx=(0, 8))

        self._atualizar_resumo()
        self._atualizar_lista()

    def _criar_campo_selecao(
        self,
        pai: tk.Frame,
        rotulo: str,
        texto_padrao: str,
        texto_botao: str,
        comando: Callable[[], None]
    ) -> tk.Label:
        tk.Label(
            pai,
            text=rotulo,
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO_SOFT
        ).pack(anchor="w")

        lbl_valor = tk.Label(
            pai,
            text=texto_padrao,
            font=FontesTema.FONTE_LABEL,
            bg=CoresTema.COR_FUNDO,
            fg=CoresTema.COR_TEXTO_SOFT,
            anchor="w",
            padx=8,
            pady=5,
            width=26,
            highlightthickness=1,
            highlightbackground=CoresTema.COR_BORDA
        )
        lbl_valor.pack(fill="x", pady=(2, 5))

        tk.Button(
            pai,
            text=texto_botao,
            command=comando,
            bg=CoresTema.COR_ACCENT,
            fg="white",
            font=FontesTema.FONTE_LABEL_SM,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=3,
            activebackground=CoresTema.COR_ACCENT_DARK,
            activeforeground="white"
        ).pack(anchor="w", pady=(0, 8))

        return lbl_valor

    def _criar_campo_data(
        self,
        pai: tk.Frame,
        rotulo: str,
        variavel: tk.StringVar,
        coluna: int,
        padx: tuple[int, int]
    ) -> tk.Entry:
        bloco = tk.Frame(pai, bg=CoresTema.COR_SURFACE)
        bloco.grid(row=0, column=coluna, sticky="ew", padx=padx)

        tk.Label(
            bloco,
            text=rotulo,
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO_SOFT
        ).pack(anchor="w")

        linha_input = tk.Frame(bloco, bg=CoresTema.COR_SURFACE)
        linha_input.pack(fill="x", pady=(2, 0))

        entry = tk.Entry(
            linha_input,
            textvariable=variavel,
            width=10,
            font=FontesTema.FONTE_LABEL,
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=CoresTema.COR_BORDA,
            highlightcolor=CoresTema.COR_ACCENT
        )
        entry.pack(side="left", fill="x", expand=True)

        tk.Button(
            linha_input,
            text="📅",
            command=lambda: self._abrir_calendario(variavel, rotulo.replace(" *", "")),
            bg=CoresTema.COR_FUNDO,
            fg=CoresTema.COR_TEXTO,
            font=FontesTema.FONTE_LABEL_SM,
            relief="flat",
            cursor="hand2",
            padx=5,
            pady=1
        ).pack(side="left", padx=(4, 0))

        return entry

    def _abrir_calendario(self, variavel: tk.StringVar, titulo_campo: str) -> None:
        try:
            data_atual = self._controller.converter_data(variavel.get())
        except ValueError:
            data_atual = date.today()

        popup = JanelaCalendario(self, data_atual, titulo=f"Selecionar {titulo_campo}")
        self.wait_window(popup)
        if popup.data_selecionada is not None:
            variavel.set(popup.data_selecionada.strftime("%d/%m/%Y"))

    def _popup_pesquisa(self):
        popup = JanelaSelecionarCliente(self, self._controller.listar_clientes)
        self.wait_window(popup)
        if popup.cliente_selecionado is not None:
            self._definir_cliente_selecionado(popup.cliente_selecionado)

    def _popup_quarto(self):
        popup = JanelaSelecionarQuarto(self, self._controller.listar_quartos)
        self.wait_window(popup)
        if popup.quarto_selecionado is not None:
            self._definir_quarto_selecionado(popup.quarto_selecionado)

    def _definir_cliente_selecionado(self, cliente: Cliente) -> None:
        self._cliente_selecionado = cliente
        self._lbl_cliente.config(
            text=f"{cliente.get_nome()} ({cliente.get_cpf()})",
            fg=CoresTema.COR_TEXTO
        )

    def _definir_quarto_selecionado(self, quarto: Quarto) -> None:
        self._quarto_selecionado = quarto
        self._lbl_quarto.config(
            text=f"Quarto {quarto.get_numero()} - {quarto.get_tipo()} (R$ {quarto.get_valor_diaria():.2f})",
            fg=CoresTema.COR_TEXTO
        )
        self._atualizar_resumo()

    def _atualizar_resumo(self) -> None:
        try:
            dt_in = self._controller.converter_data(self._var_checkin.get())
            dt_out = self._controller.converter_data(self._var_checkout.get())
            dias = (dt_out - dt_in).days
        except ValueError:
            self._lbl_resumo.config(text="")
            return

        if dias < 1:
            self._lbl_resumo.config(text="Período mínimo: 1 diária", fg=CoresTema.COR_ERRO)
            return

        sufixo = "diária" if dias == 1 else "diárias"
        if self._quarto_selecionado is not None:
            total = dias * self._quarto_selecionado.get_valor_diaria()
            texto = f"{dias} {sufixo} · Total estimado: R$ {total:.2f}"
        else:
            texto = f"{dias} {sufixo}"
        self._lbl_resumo.config(text=texto, fg=CoresTema.COR_TEXTO_SOFT)

    def _salvar_reserva(self) -> None:
        try:
            data_checkin = self._controller.converter_data(self._var_checkin.get())
            data_checkout = self._controller.converter_data(self._var_checkout.get())

            if self._reserva_em_edicao_id is None:
                reserva = self._controller.realizar_reserva(
                    self._cliente_selecionado,
                    self._quarto_selecionado,
                    data_checkin,
                    data_checkout,
                )
                msg = f"Reserva #{reserva.id} cadastrada com sucesso."
            else:
                reserva = self._controller.alterar_reserva(
                    self._reserva_em_edicao_id,
                    self._cliente_selecionado,
                    self._quarto_selecionado,
                    data_checkin,
                    data_checkout,
                )
                msg = f"Reserva #{reserva.id} alterada com sucesso."

            self._limpar_formulario(limpar_msg=False)
            self._msg_form.config(text=msg, fg=CoresTema.COR_SUCESSO)
            self._atualizar_lista()
        except ValueError as e:
            self._msg_form.config(text=str(e), fg=CoresTema.COR_ERRO)

    def _atualizar_lista(self) -> None:
        self._tree.delete(*self._tree.get_children())
        self._reservas_por_iid.clear()
        for reserva in self._controller.obter_todas_reservas():
            quarto_txt = f"Q. {reserva.quarto.get_numero()}" if reserva.quarto else "-"
            total_txt = f"R$ {reserva.calcular_total_estimado():.2f}"
            iid = self._tree.insert(
                "",
                "end",
                values=(
                    reserva.id,
                    reserva.hospede.get_nome(),
                    quarto_txt,
                    reserva.data_checkin.strftime("%d/%m/%Y"),
                    reserva.data_checkout.strftime("%d/%m/%Y"),
                    total_txt,
                    reserva.status,
                ),
            )
            self._reservas_por_iid[iid] = reserva

    def _obter_reserva_selecionada(self) -> Reserva | None:
        selecao = self._tree.selection()
        if not selecao:
            messagebox.showwarning("Atenção", "Selecione uma reserva na lista.")
            return None
        return self._reservas_por_iid.get(selecao[0])

    def _iniciar_edicao(self) -> None:
        reserva = self._obter_reserva_selecionada()
        if reserva is None or reserva.id is None:
            return

        self._reserva_em_edicao_id = reserva.id
        self._lbl_titulo_form.config(text=f"Alterar Reserva #{reserva.id}")
        self._btn_salvar.config(text="Salvar Alterações")
        self._btn_cancelar_edicao.pack(fill="x", pady=(6, 0))
        self._msg_form.config(text="")

        self._definir_cliente_selecionado(reserva.hospede)
        if reserva.quarto is not None:
            self._definir_quarto_selecionado(reserva.quarto)
        self._var_checkin.set(reserva.data_checkin.strftime("%d/%m/%Y"))
        self._var_checkout.set(reserva.data_checkout.strftime("%d/%m/%Y"))
        self._atualizar_resumo()

    def _excluir_selecionada(self) -> None:
        reserva = self._obter_reserva_selecionada()
        if reserva is None or reserva.id is None:
            return

        if messagebox.askyesno(
            "Confirmar",
            f"Excluir a reserva #{reserva.id} de {reserva.hospede.get_nome()}?"
        ):
            try:
                id_excluido = reserva.id
                self._controller.remover_reserva(id_excluido)
                if self._reserva_em_edicao_id == id_excluido:
                    self._limpar_formulario(limpar_msg=False)
                self._msg_form.config(
                    text=f"Reserva #{id_excluido} excluída.",
                    fg=CoresTema.COR_SUCESSO
                )
                self._atualizar_lista()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))

    def _limpar_formulario(self, limpar_msg: bool = True) -> None:
        self._reserva_em_edicao_id = None
        self._cliente_selecionado = None
        self._quarto_selecionado = None

        self._lbl_titulo_form.config(text="Nova Reserva")
        self._btn_salvar.config(text="Cadastrar Reserva")
        self._btn_cancelar_edicao.pack_forget()

        self._lbl_cliente.config(text="Nenhum cliente selecionado", fg=CoresTema.COR_TEXTO_SOFT)
        self._lbl_quarto.config(text="Nenhum quarto selecionado", fg=CoresTema.COR_TEXTO_SOFT)

        hoje = date.today()
        self._var_checkin.set(hoje.strftime("%d/%m/%Y"))
        self._var_checkout.set((hoje + timedelta(days=1)).strftime("%d/%m/%Y"))
        self._atualizar_resumo()
        if limpar_msg:
            self._msg_form.config(text="")

        self._atualizar_resumo()

    def _atualizar_resumo(self) -> None:
        try:
            dt_in = self._controller.converter_data(self._var_checkin.get())
            dt_out = self._controller.converter_data(self._var_checkout.get())
            dias = (dt_out - dt_in).days
        except ValueError:
            self._lbl_resumo.config(text="")
            return

        if dias < 1:
            self._lbl_resumo.config(text="Período mínimo: 1 diária", fg=CoresTema.COR_ERRO)
            return

        sufixo = "diária" if dias == 1 else "diárias"
        if self._quarto_selecionado is not None:
            total = dias * self._quarto_selecionado.get_valor_diaria()
            texto = f"{dias} {sufixo} · Total estimado: R$ {total:.2f}"
        else:
            texto = f"{dias} {sufixo}"
        self._lbl_resumo.config(text=texto, fg=CoresTema.COR_TEXTO_SOFT)

    def _salvar_reserva(self) -> None:
        try:
            data_checkin = self._controller.converter_data(self._var_checkin.get())
            data_checkout = self._controller.converter_data(self._var_checkout.get())

            if self._reserva_em_edicao_id is None:
                reserva = self._controller.realizar_reserva(
                    self._cliente_selecionado,
                    self._quarto_selecionado,
                    data_checkin,
                    data_checkout,
                )
                msg = f"Reserva #{reserva.id} cadastrada com sucesso."
            else:
                reserva = self._controller.alterar_reserva(
                    self._reserva_em_edicao_id,
                    self._cliente_selecionado,
                    self._quarto_selecionado,
                    data_checkin,
                    data_checkout,
                )
                msg = f"Reserva #{reserva.id} alterada com sucesso."

            self._limpar_formulario(limpar_msg=False)
            self._msg_form.config(text=msg, fg=CoresTema.COR_SUCESSO)
            self._atualizar_lista()
        except ValueError as e:
            self._msg_form.config(text=str(e), fg=CoresTema.COR_ERRO)

    def _atualizar_lista(self) -> None:
        self._tree.delete(*self._tree.get_children())
        self._reservas_por_iid.clear()
        for reserva in self._controller.obter_todas_reservas():
            quarto_txt = f"Q. {reserva.quarto.get_numero()}" if reserva.quarto else "-"
            total_txt = f"R$ {reserva.calcular_total_estimado():.2f}"
            iid = self._tree.insert(
                "",
                "end",
                values=(
                    reserva.id,
                    reserva.hospede.get_nome(),
                    quarto_txt,
                    reserva.data_checkin.strftime("%d/%m/%Y"),
                    reserva.data_checkout.strftime("%d/%m/%Y"),
                    total_txt,
                    reserva.status,
                ),
            )
            self._reservas_por_iid[iid] = reserva

    def _obter_reserva_selecionada(self) -> Reserva | None:
        selecao = self._tree.selection()
        if not selecao:
            messagebox.showwarning("Atenção", "Selecione uma reserva na lista.")
            return None
        return self._reservas_por_iid.get(selecao[0])

    def _iniciar_edicao(self) -> None:
        reserva = self._obter_reserva_selecionada()
        if reserva is None or reserva.id is None:
            return

        self._reserva_em_edicao_id = reserva.id
        self._lbl_titulo_form.config(text=f"Alterar Reserva #{reserva.id}")
        self._btn_salvar.config(text="Salvar Alterações")
        self._btn_cancelar_edicao.pack(fill="x", pady=(6, 0))
        self._msg_form.config(text="")

        self._definir_cliente_selecionado(reserva.hospede)
        if reserva.quarto is not None:
            self._definir_quarto_selecionado(reserva.quarto)
        self._var_checkin.set(reserva.data_checkin.strftime("%d/%m/%Y"))
        self._var_checkout.set(reserva.data_checkout.strftime("%d/%m/%Y"))
        self._atualizar_resumo()

    def _excluir_selecionada(self) -> None:
        reserva = self._obter_reserva_selecionada()
        if reserva is None or reserva.id is None:
            return

        if messagebox.askyesno(
            "Confirmar",
            f"Excluir a reserva #{reserva.id} de {reserva.hospede.get_nome()}?"
        ):
            try:
                id_excluido = reserva.id
                self._controller.remover_reserva(id_excluido)
                if self._reserva_em_edicao_id == id_excluido:
                    self._limpar_formulario(limpar_msg=False)
                self._msg_form.config(
                    text=f"Reserva #{id_excluido} excluída.",
                    fg=CoresTema.COR_SUCESSO
                )
                self._atualizar_lista()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))

    def _limpar_formulario(self, limpar_msg: bool = True) -> None:
        self._reserva_em_edicao_id = None
        self._cliente_selecionado = None
        self._quarto_selecionado = None

        self._lbl_titulo_form.config(text="Nova Reserva")
        self._btn_salvar.config(text="Cadastrar Reserva")
        self._btn_cancelar_edicao.pack_forget()

        self._lbl_cliente.config(text="Nenhum cliente selecionado", fg=CoresTema.COR_TEXTO_SOFT)
        self._lbl_quarto.config(text="Nenhum quarto selecionado", fg=CoresTema.COR_TEXTO_SOFT)

        hoje = date.today()
        self._var_checkin.set(hoje.strftime("%d/%m/%Y"))
        self._var_checkout.set((hoje + timedelta(days=1)).strftime("%d/%m/%Y"))
        self._atualizar_resumo()
        if limpar_msg:
            self._msg_form.config(text="")