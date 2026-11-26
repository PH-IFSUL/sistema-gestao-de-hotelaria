from models.quarto import Quarto
from models.database.interfaces.quarto_repositorio_interface import QuartoRepositorio


class QuartoController:
    """
    Classe para gerenciar os quartos.

    Args:
        repo: repositório de quartos

    Returns:
        Objeto do tipo QuartoController.
    """

    ESTADOS_DISPONIVEIS = (
        "Disponível",
        "Em Limpeza",
        "Em Manutenção",
        "Ocupado",
        "Reservado",
    )

    def __init__(self, repo: QuartoRepositorio) -> None:
        self._repo = repo

    def cadastrar(
        self,
        numero_str: str,
        tipo: str,
        valor_str: str
    ) -> str:
        """
        Cadastra um novo quarto.

        Args:
            numero_str: número do quarto
            tipo: tipo do quarto
            valor_str: valor da diária do quarto

        Returns:
            String informando que o quarto foi cadastrado com sucesso.
        """
        numero_str = numero_str.strip()
        valor_str = valor_str.strip().replace(",", ".")

        if not numero_str:
            raise ValueError("O campo Número é obrigatório.")
        if not numero_str.isdigit():
            raise ValueError("Número do quarto deve ser um valor inteiro.")
        if not tipo:
            raise ValueError("Selecione um tipo de quarto.")
        if not valor_str:
            raise ValueError("O campo Valor da Diária é obrigatório.")

        try:
            valor = float(valor_str)
        except ValueError:
            raise ValueError("Valor da diária deve ser um número (ex: 150.00).")

        if valor <= 0:
            raise ValueError("Valor da diária deve ser maior que zero.")

        quarto = Quarto(int(numero_str), tipo, valor)
        self._repo.adicionar(quarto)
        return f"Quarto {numero_str} ({tipo}) cadastrado com sucesso."

    def listar(self) -> list[Quarto]:
        """
        Lista todos os quartos.

        Returns:
            Lista de quartos.
        """
        return self._repo.listar()

    def remover(self, numero_str: str) -> str:
        """
        Remove um quarto.

        Args:
            numero_str: número do quarto

        Returns:
            String informando que o quarto foi removido com sucesso.
        """
        numero_str = numero_str.strip()
        if not numero_str.isdigit():
            raise ValueError("Informe um número de quarto válido.")
        if not self._repo.remover(int(numero_str)):
            raise ValueError(f"Nenhum quarto encontrado com número {numero_str}.")
        return f"Quarto {numero_str} removido."

    def obter_nome_estado(self, quarto: Quarto) -> str:
        """Obtém o nome do estado do quarto."""
        return quarto.estado.obter_atual()

    def obter_tag_estado(self, quarto: Quarto) -> str:
        """Obtém a tag do estado do quarto."""
        return quarto.estado.__str__()

    def alterar_estado(self, numero_str: str, novo_estado: str) -> str:
        """Altera o estado do quarto respeitando as transições do domínio e persiste."""
        numero_str = str(numero_str).strip()
        if not numero_str.isdigit():
            raise ValueError("Informe um número de quarto válido.")

        novo_estado = novo_estado.strip()
        if novo_estado not in self.ESTADOS_DISPONIVEIS:
            raise ValueError("Selecione um status válido para o quarto.")

        quarto = self._repo.buscar_por_numero(int(numero_str))
        if quarto is None:
            raise ValueError(f"Nenhum quarto encontrado com número {numero_str}.")

        estado_atual = quarto.estado.obter_atual()
        if estado_atual == novo_estado:
            return f"Quarto {numero_str} já está com o status '{novo_estado}'."

        try:
            if novo_estado == "Em Manutenção":
                quarto.estado.iniciar_manutencao(quarto)
            elif novo_estado == "Em Limpeza":
                if estado_atual == "Em Manutenção":
                    quarto.estado.finalizar_manutencao(quarto)
                elif estado_atual == "Ocupado":
                    quarto.estado.check_out(quarto)
                else:
                    quarto.estado.iniciar_limpeza(quarto)
            elif novo_estado == "Disponível":
                if estado_atual == "Em Manutenção":
                    quarto.estado.finalizar_manutencao(quarto)
                    quarto.estado.finalizar_limpeza(quarto)
                else:
                    quarto.estado.finalizar_limpeza(quarto)
            elif novo_estado == "Ocupado":
                quarto.estado.check_in(quarto)
            elif novo_estado == "Reservado":
                quarto.estado.reservar(quarto)
        except TypeError as erro:
            raise ValueError(str(erro)) from erro

        self._repo.atualizar_estado(quarto)
        return f"Status do quarto {numero_str} alterado para '{quarto.estado.obter_atual()}'."

