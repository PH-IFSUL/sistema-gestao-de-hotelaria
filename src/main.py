from models.guest.refactor_repo import ClienteRepositorio
from models.room.refactor_repos import QuartoRepositorio
from controllers.controller import ClienteController, QuartoController
from views.view import JanelaPrincipal


def main():
    repo_clientes = ClienteRepositorio()
    repo_quartos  = QuartoRepositorio()

    ctrl_clientes = ClienteController(repo_clientes)
    ctrl_quartos  = QuartoController(repo_quartos)

    app = JanelaPrincipal(ctrl_clientes, ctrl_quartos)
    app.mainloop()


if __name__ == "__main__":
    main()
