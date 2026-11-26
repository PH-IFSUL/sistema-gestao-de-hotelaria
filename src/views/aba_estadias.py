from datetime import date, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.estadia_controller import EstadiaController
from models.cliente import Cliente
from models.estadia import Estadia, Reserva
from models.quarto import Quarto
from .componentes.formulario import CampoFormulario
from .componentes.seletor_cliente import JanelaSelecionarCliente
from .componentes.seletor_data import CampoData
from .componentes.seletor_quarto import JanelaSelecionarQuarto
from .componentes.seletor_reserva import JanelaSelecionarReserva
from .estilo.constantes import CoresTema, FontesTema


class AbaEstadias(tk.Frame):
    """Aba para check-in (com reserva ou cliente avulso), consumos e check-out."""

    def __init__(self, parent, stay_ctrl: EstadiaController):
        super().__init__(parent, bg=CoresTema.COR_FUNDO)
        self._controller = stay_ctrl
        self._reserva_selecionada: Reserva | None = None
        self._cliente_selecionado: Cliente | None = None
        self._quarto_selecionado: Quarto | None = None
        self._estadias_por_iid: dict[str, Estadia] = {}
        self._construir()

    def _construir(self) -> None:
        painel_form = tk.Frame(
            self,
            bg=CoresTema.COR_SURFACE,
            bd=0,
            highlightthickness=1,
            highlightbackground=CoresTema.COR_BORDA
        )
        painel_form.pack(side="left", fill="y", padx=(12, 6), pady=12, ipadx=12, ipady=10)

        tk.Label(
            painel_form,
            text="Nova Hospedagem",
            font=("Segoe UI", 12, "bold"),
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO
        ).pack(anchor="w", pady=(0, 8))

        # Reserva opcional (deixe sem reserva para cliente que chega avulso)
        tk.Label(
            painel_form,
            text="Reserva (opcional)",
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO_SOFT
        ).pack(anchor="w")

        self._lbl_reserva = tk.Label(
            painel_form,
            text="Sem reserva (hospedagem avulsa)",
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_FUNDO,
            fg=CoresTema.COR_TEXTO_SOFT,
            anchor="w",
            padx=8,
            pady=4,
            width=28,
            highlightthickness=1,
            highlightbackground=CoresTema.COR_BORDA
        )
        self._lbl_reserva.pack(fill="x", pady=(2, 4))

        botoes_reserva = tk.Frame(painel_form, bg=CoresTema.COR_SURFACE)
        botoes_reserva.pack(fill="x", pady=(0, 8))
        self._criar_botao_compacto(
            botoes_reserva,
            "Usar Reserva",
            self._selecionar_reserva,
            bg=CoresTema.COR_FUNDO,
            fg=CoresTema.COR_ACCENT_DARK,
        ).pack(side="left")
        self._btn_limpar_reserva = self._criar_botao_compacto(
            botoes_reserva,
            "Limpar",
            self._limpar_reserva,
            bg=CoresTema.COR_BORDA,
            fg=CoresTema.COR_TEXTO,
        )

        # Cliente
        tk.Label(
            painel_form,
            text="Cliente *",
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO_SOFT
        ).pack(anchor="w")

        self._lbl_cliente = tk.Label(
            painel_form,
            text="Nenhum cliente selecionado",
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
        self._lbl_cliente.pack(fill="x", pady=(2, 4))

        botoes_cliente = tk.Frame(painel_form, bg=CoresTema.COR_SURFACE)
        botoes_cliente.pack(fill="x", pady=(0, 8))
        self._criar_botao_compacto(
            botoes_cliente,
            "Selecionar Cliente",
            self._selecionar_cliente,
        ).pack(side="left")
        self._criar_botao_compacto(
            botoes_cliente,
            "+ Novo Cliente",
            self._cadastrar_novo_cliente,
            bg="#E6EFF8",
            fg=CoresTema.COR_ACCENT_DARK,
        ).pack(side="left", padx=(6, 0))

        # Quarto
        tk.Label(
            painel_form,
            text="Quarto *",
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO_SOFT
        ).pack(anchor="w")

        self._lbl_quarto = tk.Label(
            painel_form,
            text="Nenhum quarto selecionado",
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
        self._lbl_quarto.pack(fill="x", pady=(2, 4))

        self._criar_botao_compacto(
            painel_form,
            "Selecionar Quarto",
            self._selecionar_quarto,
        ).pack(anchor="w", pady=(0, 8))

        # Check-out previsto
        self._campo_checkout = CampoData(
            painel_form,
            "Check-out previsto *",
            data_inicial=date.today() + timedelta(days=1),
            on_change=self._atualizar_resumo,
        )
        self._campo_checkout.pack(fill="x", pady=(0, 4))

        self._lbl_resumo = tk.Label(
            painel_form,
            text="",
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO_SOFT,
            anchor="w"
        )
        self._lbl_resumo.pack(fill="x", pady=(2, 2))

        self._msg_form = tk.Label(
            painel_form,
            text="",
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_SURFACE,
            wraplength=220,
            justify="left"
        )
        self._msg_form.pack(anchor="w", pady=(2, 0))

        tk.Button(
            painel_form,
            text="Realizar Check-in",
            command=self._realizar_checkin,
            bg=CoresTema.COR_ACCENT,
            fg="white",
            font=FontesTema.FONTE_BOTAO,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            activebackground=CoresTema.COR_ACCENT_DARK,
            activeforeground="white"
        ).pack(fill="x", pady=(8, 0))

        # Painel direito (listagem no mesmo estilo das outras abas)
        painel_lista = tk.Frame(self, bg=CoresTema.COR_FUNDO)
        painel_lista.pack(side="left", fill="both", expand=True, padx=(6, 12), pady=12)

        topo = tk.Frame(painel_lista, bg=CoresTema.COR_FUNDO)
        topo.pack(fill="x", pady=(0, 6))
        tk.Label(
            topo,
            text="Estadias Registradas",
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

        cols = ("id", "cliente", "quarto", "checkin", "checkout", "consumos", "total", "status")
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
            "consumos": "Consumos",
            "total": "Total",
            "status": "Status",
        }
        larguras = {
            "id": 34,
            "cliente": 120,
            "quarto": 62,
            "checkin": 78,
            "checkout": 78,
            "consumos": 74,
            "total": 76,
            "status": 86,
        }
        for c in cols:
            self._tree.heading(c, text=cabecalhos[c])
            self._tree.column(c, width=larguras[c], anchor="w")

        self._tree.tag_configure("hospedado", foreground="#1E4266", background="#EEF5FC")
        self._tree.tag_configure("finalizada", foreground=CoresTema.COR_TEXTO_SOFT)

        sb = ttk.Scrollbar(frame_tree, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=sb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        barra_acoes = tk.Frame(painel_lista, bg=CoresTema.COR_FUNDO)
        barra_acoes.pack(fill="x", pady=(6, 0))

        tk.Button(
            barra_acoes,
            text="Excluir",
            command=self._excluir_estadia,
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
            text="Realizar Check-out",
            command=self._realizar_checkout,
            bg=CoresTema.COR_ACCENT,
            fg="white",
            font=FontesTema.FONTE_LABEL_SM,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            activebackground=CoresTema.COR_ACCENT_DARK,
            activeforeground="white"
        ).pack(side="right", padx=(0, 8))

        tk.Button(
            barra_acoes,
            text="Lançar Consumo",
            command=self._abrir_consumo,
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

    def _criar_botao_compacto(
        self,
        pai: tk.Frame,
        texto: str,
        comando,
        bg: str = CoresTema.COR_ACCENT,
        fg: str = "white",
    ) -> tk.Button:
        return tk.Button(
            pai,
            text=texto,
            command=comando,
            bg=bg,
            fg=fg,
            font=FontesTema.FONTE_LABEL_SM,
            relief="flat",
            cursor="hand2",
            padx=9,
            pady=3,
            activebackground=CoresTema.COR_ACCENT_DARK if bg == CoresTema.COR_ACCENT else bg,
            activeforeground=fg,
        )

    def _selecionar_reserva(self) -> None:
        popup = JanelaSelecionarReserva(self, self._controller.listar_reservas_confirmadas)
        self.wait_window(popup)
        if popup.reserva_selecionada is not None:
            self._aplicar_reserva(popup.reserva_selecionada)

    def _aplicar_reserva(self, reserva: Reserva) -> None:
        self._reserva_selecionada = reserva
        self._lbl_reserva.config(
            text=f"Reserva #{reserva.id} · {reserva.hospede.get_nome()}",
            fg=CoresTema.COR_TEXTO,
        )
        self._btn_limpar_reserva.pack(side="left", padx=(6, 0))
        self._definir_cliente_selecionado(reserva.hospede)
        if reserva.quarto is not None:
            self._definir_quarto_selecionado(reserva.quarto)
        self._campo_checkout.set_data(reserva.data_checkout)
        self._atualizar_resumo()

    def _limpar_reserva(self) -> None:
        self._reserva_selecionada = None
        self._lbl_reserva.config(
            text="Sem reserva (hospedagem avulsa)",
            fg=CoresTema.COR_TEXTO_SOFT,
        )
        self._btn_limpar_reserva.pack_forget()

    def _selecionar_cliente(self) -> None:
        popup = JanelaSelecionarCliente(self, self._controller.listar_clientes)
        self.wait_window(popup)
        if popup.cliente_selecionado is not None:
            self._definir_cliente_selecionado(popup.cliente_selecionado)

    def _cadastrar_novo_cliente(self) -> None:
        popup = tk.Toplevel(self)
        popup.title("Novo Cliente (Check-in Avulso)")
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
            text="Cadastrar Novo Cliente",
            font=("Segoe UI", 11, "bold"),
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO
        ).pack(anchor="w", pady=(0, 8))

        campo_nome = CampoFormulario(container, "Nome completo *")
        campo_nome.pack(fill="x", pady=3)
        campo_cpf = CampoFormulario(container, "CPF (11 dígitos) *")
        campo_cpf.pack(fill="x", pady=3)
        campo_tel = CampoFormulario(container, "Telefone *")
        campo_tel.pack(fill="x", pady=3)
        campo_email = CampoFormulario(container, "E-mail")
        campo_email.pack(fill="x", pady=3)

        lbl_erro = tk.Label(
            container,
            text="",
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_ERRO,
            wraplength=230,
            justify="left"
        )
        lbl_erro.pack(anchor="w", pady=(4, 6))

        botoes = tk.Frame(container, bg=CoresTema.COR_SURFACE)
        botoes.pack(fill="x")

        def _salvar():
            try:
                cliente = self._controller.cadastrar_cliente(
                    campo_nome.get(),
                    campo_cpf.get(),
                    campo_tel.get(),
                    campo_email.get(),
                )
                self._definir_cliente_selecionado(cliente)
                self._msg_form.config(
                    text=f"Cliente '{cliente.get_nome()}' cadastrado e selecionado.",
                    fg=CoresTema.COR_SUCESSO,
                )
                popup.destroy()
            except ValueError as e:
                lbl_erro.config(text=str(e))

        tk.Button(
            botoes,
            text="Cadastrar e Selecionar",
            command=_salvar,
            bg=CoresTema.COR_ACCENT,
            fg="white",
            font=FontesTema.FONTE_BOTAO,
            relief="flat",
            cursor="hand2",
            padx=10,
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

        self._centralizar_popup(popup)
        campo_nome.entry.focus_set()

    def _selecionar_quarto(self) -> None:
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
            dt_out = self._controller.converter_data(self._campo_checkout.get())
        except ValueError:
            self._lbl_resumo.config(text="")
            return

        dias = (dt_out - date.today()).days
        if dias < 1:
            self._lbl_resumo.config(
                text="Check-out previsto deve ser após hoje",
                fg=CoresTema.COR_ERRO,
            )
            return

        sufixo = "diária" if dias == 1 else "diárias"
        if self._quarto_selecionado is not None:
            total = dias * self._quarto_selecionado.get_valor_diaria()
            texto = f"{dias} {sufixo} · Diárias est.: R$ {total:.2f}"
        else:
            texto = f"{dias} {sufixo}"
        self._lbl_resumo.config(text=texto, fg=CoresTema.COR_TEXTO_SOFT)

    def _realizar_checkin(self) -> None:
        try:
            data_checkout = self._controller.converter_data(self._campo_checkout.get())
            estadia = self._controller.realizar_checkin(
                cliente=self._cliente_selecionado,
                quarto=self._quarto_selecionado,
                data_checkout=data_checkout,
                reserva=self._reserva_selecionada,
            )
            self._limpar_formulario(limpar_msg=False)
            self._msg_form.config(
                text=f"Check-in da estadia #{estadia.id} realizado com sucesso.",
                fg=CoresTema.COR_SUCESSO,
            )
            self._atualizar_lista()
        except ValueError as e:
            self._msg_form.config(text=str(e), fg=CoresTema.COR_ERRO)

    def _atualizar_lista(self) -> None:
        self._tree.delete(*self._tree.get_children())
        self._estadias_por_iid.clear()
        for estadia in self._controller.obter_todas_estadias():
            quarto_txt = f"Q. {estadia.quarto.get_numero()}" if estadia.quarto else "-"
            consumos_txt = f"R$ {estadia.calcular_total_consumos():.2f}"
            total_txt = f"R$ {estadia.obter_total():.2f}"
            tag = ("hospedado",) if estadia.status == "HOSPEDADO" else ("finalizada",)
            iid = self._tree.insert(
                "",
                "end",
                values=(
                    estadia.id,
                    estadia.hospede.get_nome(),
                    quarto_txt,
                    estadia.data_checkin.strftime("%d/%m/%Y"),
                    estadia.data_checkout.strftime("%d/%m/%Y"),
                    consumos_txt,
                    total_txt,
                    estadia.status,
                ),
                tags=tag,
            )
            self._estadias_por_iid[iid] = estadia

    def _obter_estadia_selecionada(self) -> Estadia | None:
        selecao = self._tree.selection()
        if not selecao:
            messagebox.showwarning("Atenção", "Selecione uma estadia na lista.")
            return None
        return self._estadias_por_iid.get(selecao[0])

    def _abrir_consumo(self) -> None:
        estadia = self._obter_estadia_selecionada()
        if estadia is None or estadia.id is None:
            return
        if estadia.status != "HOSPEDADO":
            messagebox.showwarning("Atenção", "Só é possível lançar consumos em estadias com status HOSPEDADO.")
            return

        catalogo = self._controller.listar_itens_catalogo()
        if not catalogo:
            messagebox.showwarning("Atenção", "Nenhum item de consumo cadastrado.")
            return

        popup = tk.Toplevel(self)
        popup.title(f"Lançar Consumo - Estadia #{estadia.id}")
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
            text=f"Estadia #{estadia.id} · {estadia.hospede.get_nome()}",
            font=("Segoe UI", 10, "bold"),
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            container,
            text="Item *",
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO_SOFT
        ).pack(anchor="w")

        opcoes = [f"{item.nome} (R$ {item.preco:.2f})" for item in catalogo]
        combo_item = ttk.Combobox(container, values=opcoes, state="readonly", font=FontesTema.FONTE_LABEL, width=28)
        combo_item.current(0)
        combo_item.pack(fill="x", pady=(2, 8))

        campo_qtd = CampoFormulario(container, "Quantidade *", largura=10)
        campo_qtd.entry.insert(0, "1")
        campo_qtd.pack(fill="x", pady=(0, 10))

        botoes = tk.Frame(container, bg=CoresTema.COR_SURFACE)
        botoes.pack(fill="x")

        def _confirmar():
            try:
                qtd = int(campo_qtd.get().strip())
                item_escolhido = catalogo[combo_item.current()]
                self._controller.lancar_consumo(estadia.id, item_escolhido.id, qtd)
                self._atualizar_lista()
                popup.destroy()
            except ValueError as e:
                messagebox.showerror("Erro", str(e), parent=popup)

        tk.Button(
            botoes,
            text="Adicionar",
            command=_confirmar,
            bg=CoresTema.COR_ACCENT,
            fg="white",
            font=FontesTema.FONTE_BOTAO,
            relief="flat",
            cursor="hand2",
            padx=10,
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

        self._centralizar_popup(popup)

    def _realizar_checkout(self) -> None:
        estadia = self._obter_estadia_selecionada()
        if estadia is None or estadia.id is None:
            return
        if estadia.status != "HOSPEDADO":
            messagebox.showwarning("Atenção", "Esta estadia já foi finalizada.")
            return

        diarias_val = estadia.calcular_total_diarias()
        consumos_val = estadia.calcular_total_consumos()
        total_val = estadia.obter_total()

        resumo = (
            f"Finalizar estadia #{estadia.id} de {estadia.hospede.get_nome()}?\n\n"
            f"Diárias ({estadia.get_numero_diarias()}x): R$ {diarias_val:.2f}\n"
            f"Consumos: R$ {consumos_val:.2f}\n"
            f"Total geral: R$ {total_val:.2f}"
        )
        if messagebox.askyesno("Confirmar Check-out", resumo):
            try:
                self._controller.realizar_checkout(estadia.id)
                self._msg_form.config(
                    text=f"Check-out da estadia #{estadia.id} concluído (Total: R$ {total_val:.2f}).",
                    fg=CoresTema.COR_SUCESSO,
                )
                self._atualizar_lista()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))

    def _excluir_estadia(self) -> None:
        estadia = self._obter_estadia_selecionada()
        if estadia is None or estadia.id is None:
            return
        if messagebox.askyesno(
            "Confirmar",
            f"Excluir a estadia #{estadia.id} de {estadia.hospede.get_nome()}?"
        ):
            try:
                self._controller.remover_estadia(estadia.id)
                self._atualizar_lista()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))

    def _limpar_formulario(self, limpar_msg: bool = True) -> None:
        self._limpar_reserva()
        self._cliente_selecionado = None
        self._quarto_selecionado = None
        self._lbl_cliente.config(text="Nenhum cliente selecionado", fg=CoresTema.COR_TEXTO_SOFT)
        self._lbl_quarto.config(text="Nenhum quarto selecionado", fg=CoresTema.COR_TEXTO_SOFT)
        self._campo_checkout.set_data(date.today() + timedelta(days=1))
        self._atualizar_resumo()
        if limpar_msg:
            self._msg_form.config(text="")

    def _centralizar_popup(self, popup: tk.Toplevel) -> None:
        popup.transient(self.winfo_toplevel())
        popup.grab_set()
        popup.update_idletasks()
        janela_pai = self.winfo_toplevel()
        x = janela_pai.winfo_rootx() + (janela_pai.winfo_width() - popup.winfo_width()) // 2
        y = janela_pai.winfo_rooty() + (janela_pai.winfo_height() - popup.winfo_height()) // 2
        popup.geometry(f"+{max(0, x)}+{max(0, y)}")
        popup.bind("<Escape>", lambda _e: popup.destroy())
