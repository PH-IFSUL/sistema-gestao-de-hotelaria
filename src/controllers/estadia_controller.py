from datetime import date, datetime
from models.quarto import Quarto
from models.cliente import Cliente
from models.estado_quarto import Disponivel
from models.estadia import Estadia, Reserva
from models.item import Item, ItemFatura
from models.database.interfaces.cliente_repositorio_interface import ClienteRepositorio
from models.database.interfaces.quarto_repositorio_interface import QuartoRepositorio
from models.database.interfaces.reserva_repositorio_interface import ReservaRepositorio
from models.database.interfaces.estadia_repositorio_interface import EstadiaRepositorio
from models.database.repositories.reserva_repositorio_memoria import ReservaRepositorioMemoria
from models.database.repositories.estadia_repositorio_memoria import EstadiaRepositorioMemoria


class EstadiaController:
    """
    Controlador responsável pelo gerenciamento de estadias e reservas.
    """

    def __init__(
        self,
        cliente_repo: ClienteRepositorio,
        quarto_repo: QuartoRepositorio,
        reserva_repo: ReservaRepositorio | None = None,
        estadia_repo: EstadiaRepositorio | None = None,
    ) -> None:
        self._cliente_repo = cliente_repo
        self._quarto_repo = quarto_repo
        self._reserva_repo: ReservaRepositorio = (
            reserva_repo if reserva_repo is not None else ReservaRepositorioMemoria()
        )
        self._estadia_repo: EstadiaRepositorio = (
            estadia_repo if estadia_repo is not None else EstadiaRepositorioMemoria()
        )

    def listar_clientes(self, filtro: str = "") -> list[Cliente]:
        """Retorna os clientes cadastrados, filtrando opcionalmente por nome ou CPF."""
        clientes = self._cliente_repo.obter_todos()
        termo = filtro.strip().lower()
        if not termo:
            return clientes

        termo_cpf = "".join(ch for ch in termo if ch.isdigit())
        resultado: list[Cliente] = []
        for cliente in clientes:
            nome_match = termo in cliente.get_nome().lower()
            cpf_match = bool(termo_cpf) and termo_cpf in cliente.get_cpf()
            if nome_match or cpf_match:
                resultado.append(cliente)
        return resultado

    def listar_quartos(
        self,
        filtro: str = "",
        apenas_disponiveis: bool = False
    ) -> list[Quarto]:
        """Retorna os quartos cadastrados, filtrando opcionalmente por número, tipo ou status."""
        quartos = self._quarto_repo.listar()
        termo = filtro.strip().lower()
        resultado: list[Quarto] = []
        for quarto in quartos:
            status = quarto.estado.obter_atual()
            if apenas_disponiveis and status != "Disponível":
                continue
            if not termo:
                resultado.append(quarto)
                continue
            numero_match = termo in str(quarto.get_numero())
            tipo_match = termo in quarto.get_tipo().lower()
            status_match = termo in status.lower()
            if numero_match or tipo_match or status_match:
                resultado.append(quarto)
        return resultado

    @staticmethod
    def converter_data(texto: str) -> date:
        """Converte texto no formato DD/MM/AAAA (ou AAAA-MM-DD) para date."""
        valor = texto.strip()
        if not valor:
            raise ValueError("Informe as datas de check-in e check-out.")
        for formato in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(valor, formato).date()
            except ValueError:
                continue
        raise ValueError("Data inválida. Use o formato DD/MM/AAAA.")

    def _validar_reserva(
        self,
        cliente: Cliente | None,
        quarto: Quarto | None,
        data_inicio: date,
        data_fim: date,
        ignorar_id: int | None = None,
    ) -> tuple[Cliente, Quarto]:
        if cliente is None:
            raise ValueError("Selecione um cliente para a reserva.")
        if quarto is None:
            raise ValueError("Selecione um quarto para a reserva.")
        if data_fim <= data_inicio:
            raise ValueError("A data de check-out deve ser posterior ao check-in.")
        if quarto.estado.obter_atual() == "Em Manutenção":
            raise ValueError(f"O quarto {quarto.get_numero()} está em manutenção.")
        if self._reserva_repo.existe_conflito(
            quarto.get_numero(), data_inicio, data_fim, ignorar_id=ignorar_id
        ):
            raise ValueError(
                f"O quarto {quarto.get_numero()} já possui reserva para o período informado."
            )
        return cliente, quarto

    def _sincronizar_estado_quarto(self, numero_quarto: int) -> None:
        quarto = self._quarto_repo.buscar_por_numero(numero_quarto)
        if quarto is None:
            return
        possui_reserva_ativa = any(
            r.status == "CONFIRMADA"
            and r.quarto is not None
            and r.quarto.get_numero() == numero_quarto
            for r in self._reserva_repo.listar()
        )
        estado_atual = quarto.estado.obter_atual()
        if possui_reserva_ativa and estado_atual == "Disponível":
            quarto.estado.reservar(quarto)
        elif not possui_reserva_ativa and estado_atual == "Reservado":
            quarto.estado.set_estado(Disponivel())

        if hasattr(self._quarto_repo, "atualizar_estado"):
            self._quarto_repo.atualizar_estado(quarto)

    def realizar_reserva(
        self,
        cliente: Cliente | None,
        quarto: Quarto | None,
        data_inicio: date,
        data_fim: date,
    ) -> Reserva:
        cliente_ok, quarto_ok = self._validar_reserva(
            cliente, quarto, data_inicio, data_fim
        )
        reserva = Reserva(
            hospede=cliente_ok,
            data_checkin=data_inicio,
            data_checkout=data_fim,
            quarto=quarto_ok,
        )
        self._reserva_repo.salvar(reserva)
        self._sincronizar_estado_quarto(quarto_ok.get_numero())
        return reserva

    def alterar_reserva(
        self,
        reserva_id: int,
        cliente: Cliente | None,
        quarto: Quarto | None,
        data_inicio: date,
        data_fim: date,
    ) -> Reserva:
        existente = self._reserva_repo.buscar_por_id(reserva_id)
        if existente is None:
            raise ValueError(f"Reserva #{reserva_id} não encontrada.")

        cliente_ok, quarto_ok = self._validar_reserva(
            cliente, quarto, data_inicio, data_fim, ignorar_id=reserva_id
        )
        quarto_anterior = existente.quarto.get_numero() if existente.quarto else None

        existente.hospede = cliente_ok
        existente.quarto = quarto_ok
        existente.data_checkin = data_inicio
        existente.data_checkout = data_fim
        self._reserva_repo.atualizar(existente)

        if quarto_anterior is not None and quarto_anterior != quarto_ok.get_numero():
            self._sincronizar_estado_quarto(quarto_anterior)
        self._sincronizar_estado_quarto(quarto_ok.get_numero())
        return existente

    def remover_reserva(self, reserva_id: int) -> None:
        existente = self._reserva_repo.buscar_por_id(reserva_id)
        if existente is None:
            raise ValueError(f"Reserva #{reserva_id} não encontrada.")
        numero_quarto = existente.quarto.get_numero() if existente.quarto else None
        if not self._reserva_repo.remover(reserva_id):
            raise ValueError(f"Não foi possível excluir a reserva #{reserva_id}.")
        if numero_quarto is not None:
            self._sincronizar_estado_quarto(numero_quarto)

    def obter_todas_reservas(self) -> list[Reserva]:
        return self._reserva_repo.listar()

    def listar_reservas_confirmadas(self, filtro: str = "") -> list[Reserva]:
        """Retorna apenas reservas confirmadas para check-in, com filtro opcional."""
        termo = filtro.strip().lower()
        termo_cpf = "".join(ch for ch in termo if ch.isdigit())
        resultado: list[Reserva] = []
        for reserva in self._reserva_repo.listar():
            if reserva.status != "CONFIRMADA":
                continue
            if not termo:
                resultado.append(reserva)
                continue
            nome_match = termo in reserva.hospede.get_nome().lower()
            cpf_match = bool(termo_cpf) and termo_cpf in reserva.hospede.get_cpf()
            quarto_match = reserva.quarto is not None and termo in str(reserva.quarto.get_numero())
            if nome_match or cpf_match or quarto_match:
                resultado.append(reserva)
        return resultado

    def cadastrar_cliente(
        self,
        nome: str,
        cpf: str,
        telefone: str,
        email: str,
    ) -> Cliente:
        """Cadastra rapidamente um novo cliente que chega sem reserva."""
        nome = nome.strip()
        cpf = "".join(ch for ch in cpf.strip() if ch.isdigit()) if any(c in cpf for c in ".-") else cpf.strip()
        telefone = telefone.strip()
        email = email.strip()

        if not nome:
            raise ValueError("O campo Nome é obrigatório.")
        if not cpf:
            raise ValueError("O campo CPF é obrigatório.")
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("CPF deve conter exatamente 11 dígitos numéricos.")
        if not telefone:
            raise ValueError("O campo Telefone é obrigatório.")

        cliente = Cliente(nome, cpf, telefone, email)
        self._cliente_repo.salvar(cliente)
        return cliente

    def realizar_checkin(
        self,
        cliente: Cliente | None,
        quarto: Quarto | None,
        data_checkout: date,
        reserva: Reserva | None = None,
        data_checkin: datetime | None = None,
    ) -> Estadia:
        """Realiza o check-in de um hóspede (com reserva ou avulso sem reserva)."""
        if cliente is None:
            raise ValueError("Selecione ou cadastre um cliente para a hospedagem.")
        if quarto is None:
            raise ValueError("Selecione um quarto para a hospedagem.")

        checkin_dt = data_checkin if data_checkin is not None else datetime.now()
        if data_checkout <= checkin_dt.date():
            raise ValueError("A data de check-out previsto deve ser posterior a hoje.")

        quarto_atual = self._quarto_repo.buscar_por_numero(quarto.get_numero())
        if quarto_atual is None:
            raise ValueError(f"Quarto {quarto.get_numero()} não encontrado.")

        estado_atual = quarto_atual.estado.obter_atual()

        if reserva is not None:
            reserva_atual = self._reserva_repo.buscar_por_id(reserva.id) if reserva.id else None
            if reserva_atual is None or reserva_atual.status != "CONFIRMADA":
                raise ValueError("Check-in só pode ser realizado para reservas confirmadas.")
            if estado_atual not in ("Disponível", "Reservado"):
                raise ValueError(
                    f"O quarto {quarto_atual.get_numero()} está '{estado_atual}' e não pode receber check-in."
                )
            try:
                quarto_atual.estado.check_in(quarto_atual)
            except TypeError as erro:
                raise ValueError(str(erro)) from erro
            reserva_atual.status = "FINALIZADA"
            self._reserva_repo.atualizar(reserva_atual)
        else:
            if estado_atual != "Disponível":
                raise ValueError(
                    f"O quarto {quarto_atual.get_numero()} está '{estado_atual}'. "
                    "Hospedagem sem reserva exige quarto disponível."
                )
            if self._reserva_repo.existe_conflito(
                quarto_atual.get_numero(), checkin_dt.date(), data_checkout
            ):
                raise ValueError(
                    f"O quarto {quarto_atual.get_numero()} possui reserva conflitante no período informado."
                )
            try:
                quarto_atual.estado.check_in(quarto_atual)
            except TypeError as erro:
                raise ValueError(str(erro)) from erro

        if hasattr(self._quarto_repo, "atualizar_estado"):
            self._quarto_repo.atualizar_estado(quarto_atual)

        checkout_dt = datetime.combine(data_checkout, checkin_dt.time())
        estadia = Estadia(
            hospede=cliente,
            quarto=quarto_atual,
            data_checkin=checkin_dt,
            data_checkout=checkout_dt,
            status="HOSPEDADO",
            reserva_id=reserva.id if reserva is not None else None,
        )
        self._estadia_repo.salvar(estadia)
        return estadia

    def realizar_checkout(
        self,
        estadia_id: int,
        data_checkout: datetime | None = None,
    ) -> Estadia:
        """Finaliza a estadia, calcula o total e coloca o quarto em limpeza."""
        estadia = self._estadia_repo.buscar_por_id(estadia_id)
        if estadia is None:
            raise ValueError(f"Estadia #{estadia_id} não encontrada.")
        if estadia.status != "HOSPEDADO":
            raise ValueError("Esta estadia já foi finalizada.")

        agora = data_checkout if data_checkout is not None else datetime.now()
        if agora > estadia.data_checkin:
            estadia.data_checkout = agora

        if estadia.quarto is not None:
            quarto = self._quarto_repo.buscar_por_numero(estadia.quarto.get_numero())
            if quarto is not None:
                if quarto.estado.obter_atual() == "Ocupado":
                    quarto.estado.check_out(quarto)
                    if hasattr(self._quarto_repo, "atualizar_estado"):
                        self._quarto_repo.atualizar_estado(quarto)
                estadia.quarto = quarto

        estadia.status = "FINALIZADA"
        self._estadia_repo.atualizar(estadia)
        return estadia

    def listar_itens_catalogo(self) -> list[Item]:
        return self._estadia_repo.listar_itens_catalogo()

    def lancar_consumo(
        self,
        estadia_id: int,
        item_id: int,
        quantidade: int,
    ) -> Estadia:
        """Lança um item de consumo na fatura da estadia hospedada."""
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        estadia = self._estadia_repo.buscar_por_id(estadia_id)
        if estadia is None:
            raise ValueError(f"Estadia #{estadia_id} não encontrada.")
        if estadia.status != "HOSPEDADO":
            raise ValueError("Só é possível lançar consumos em estadias ativas.")

        item = next((i for i in self._estadia_repo.listar_itens_catalogo() if i.id == item_id), None)
        if item is None:
            raise ValueError("Selecione um item de consumo válido.")

        item_fatura = ItemFatura(id=0, item=item, quantidade=quantidade)
        self._estadia_repo.adicionar_item_fatura(estadia_id, item_fatura)
        atualizada = self._estadia_repo.buscar_por_id(estadia_id)
        return atualizada if atualizada is not None else estadia

    def remover_estadia(self, estadia_id: int) -> None:
        """Remove o registro da estadia; se ainda hospedada, libera o quarto."""
        estadia = self._estadia_repo.buscar_por_id(estadia_id)
        if estadia is None:
            raise ValueError(f"Estadia #{estadia_id} não encontrada.")

        numero_quarto = estadia.quarto.get_numero() if estadia.quarto else None
        estava_hospedado = estadia.status == "HOSPEDADO"

        if not self._estadia_repo.remover(estadia_id):
            raise ValueError(f"Não foi possível remover a estadia #{estadia_id}.")

        if estava_hospedado and numero_quarto is not None:
            quarto = self._quarto_repo.buscar_por_numero(numero_quarto)
            if quarto is not None and quarto.estado.obter_atual() == "Ocupado":
                quarto.estado.set_estado(Disponivel())
                if hasattr(self._quarto_repo, "atualizar_estado"):
                    self._quarto_repo.atualizar_estado(quarto)
                self._sincronizar_estado_quarto(numero_quarto)

    def obter_todas_estadias(self) -> list[Estadia]:
        return self._estadia_repo.listar()


