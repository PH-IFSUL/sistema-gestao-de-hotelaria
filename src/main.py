from models.database.repositories.cliente_memory_repository import InMemoryClienteRepository
from models.database.repositories.room_memory_repository import InMemoryRoomRepository
from controllers.quarto_controller import QuartoController
from controllers.cliente_controller import ClienteController
from views.main_windows.main import JanelaPrincipal


def main():
    repo_clientes = InMemoryClienteRepository()
    repo_quartos  = InMemoryRoomRepository()

    ctrl_clientes = ClienteController(repo_clientes)
    ctrl_quartos  = QuartoController(repo_quartos)

    app = JanelaPrincipal(ctrl_clientes, ctrl_quartos)
    app.mainloop()


if __name__ == "__main__":
    main()