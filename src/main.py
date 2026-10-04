from models.database.repositories.client_memory_repository import In_Memory_Client_Repository
from models.database.repositories.room_memory_repository import In_Memory_Room_Repository
from controllers.room_controller import Room_Controller
from controllers.client_controller import Client_Controller
from views.main import JanelaPrincipal


def main():
    repo_clientes = In_Memory_Client_Repository()
    repo_quartos  = In_Memory_Room_Repository()

    ctrl_clientes = Client_Controller(repo_clientes)
    ctrl_quartos  = Room_Controller(repo_quartos)

    app = JanelaPrincipal(ctrl_clientes, ctrl_quartos)
    app.mainloop()


if __name__ == "__main__":
    main()