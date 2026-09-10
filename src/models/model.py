class Cliente:
    def __init__(self, nome: str, cpf: str, telefone: str, email: str):
        self._nome = nome
        self._cpf = cpf
        self._telefone = telefone
        self._email = email

    def get_nome(self) -> str:
        return self._nome

    def get_cpf(self) -> str:
        return self._cpf

    def get_telefone(self) -> str:
        return self._telefone

    def get_email(self) -> str:
        return self._email

    def __str__(self):
        return f"{self._nome} (CPF: {self._cpf})"


class Quarto:
    TIPOS = ["Simples", "Duplo", "Suíte"]

    def __init__(self, numero: int, tipo: str, valor_diaria: float):
        if tipo not in self.TIPOS:
            raise ValueError(f"Tipo inválido. Escolha entre: {self.TIPOS}")
        self._numero = numero
        self._tipo = tipo
        self._valor_diaria = valor_diaria
        self._disponivel = True

    def get_numero(self) -> int:
        return self._numero

    def get_tipo(self) -> str:
        return self._tipo

    def get_valor_diaria(self) -> float:
        return self._valor_diaria

    def is_disponivel(self) -> bool:
        return self._disponivel

    def bloquear(self):
        self._disponivel = False

    def liberar(self):
        self._disponivel = True

    def __str__(self):
        status = "Disponível" if self._disponivel else "Ocupado"
        return f"Quarto {self._numero} | {self._tipo} | R$ {self._valor_diaria:.2f} | {status}"


class ClienteRepositorio:
    def __init__(self):
        self._clientes: list[Cliente] = []

    def adicionar(self, cliente: Cliente) -> None:
        if self.buscar_por_cpf(cliente.get_cpf()):
            raise ValueError(f"Já existe um cliente com o CPF {cliente.get_cpf()}.")
        self._clientes.append(cliente)

    def listar(self) -> list[Cliente]:
        return list(self._clientes)

    def buscar_por_cpf(self, cpf: str) -> Cliente | None:
        for c in self._clientes:
            if c.get_cpf() == cpf:
                return c
        return None

    def remover(self, cpf: str) -> bool:
        cliente = self.buscar_por_cpf(cpf)
        if cliente:
            self._clientes.remove(cliente)
            return True
        return False


class QuartoRepositorio:
    def __init__(self):
        self._quartos: list[Quarto] = []

    def adicionar(self, quarto: Quarto) -> None:
        if self.buscar_por_numero(quarto.get_numero()):
            raise ValueError(f"Já existe um quarto com o número {quarto.get_numero()}.")
        self._quartos.append(quarto)

    def listar(self) -> list[Quarto]:
        return list(self._quartos)

    def buscar_por_numero(self, numero: int) -> Quarto | None:
        for q in self._quartos:
            if q.get_numero() == numero:
                return q
        return None

    def remover(self, numero: int) -> bool:
        quarto = self.buscar_por_numero(numero)
        if quarto:
            self._quartos.remove(quarto)
            return True
        return False
