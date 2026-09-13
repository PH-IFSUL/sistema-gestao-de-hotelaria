from .cliente import Cliente

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
