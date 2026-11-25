from datetime import date, datetime
from models.quarto import Quarto
from models.cliente import Cliente
from models.estado_quarto import Disponivel
from models.estadia import Estadia, Reserva
from models.database.interfaces.cliente_repositorio_interface import ClienteRepositorio
from models.database.interfaces.quarto_repositorio_interface import QuartoRepositorio
from models.database.interfaces.reserva_repositorio_interface import ReservaRepositorio
from models.database.repositories.reserva_repositorio_memoria import ReservaRepositorioMemoria


class EstadiaController:
    """
    Controlador responsável pelo gerenciamento de estadias e reservas.
    """

    def __init__(
        self,
        cliente_repo: ClienteRepositorio,
        quarto_repo: QuartoRepositorio,
        reserva_repo: ReservaRepositorio | None = None,
    ) -> None:
        self._cliente_repo = cliente_repo
        self._quarto_repo = quarto_repo
        self._reserva_repo: ReservaRepositorio = (
            reserva_repo if reserva_repo is not None else ReservaRepositorioMemoria()
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

    def adicionar_cliente_estadia(self, estadia: Estadia, cliente: Cliente):
        pass

    def adicionar_quarto_estadia(self, estadia: Estadia, quarto: Quarto):
        pass

    def remover_cliente_estadia(self, estadia: Estadia, cliente: Cliente):
        pass

    def remover_quarto_estadia(self, estadia: Estadia, quarto: Quarto):
        pass

    def check_in(self, estadia: Estadia, data_checkin: datetime):
        pass

    def check_out(self, estadia: Estadia, data_checkout: datetime):
        pass

    def obter_todas_estadias(self):
        pass


