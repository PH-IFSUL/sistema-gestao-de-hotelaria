from models.database.conexao import ConexaoBanco
from models.database.repositories.cliente_repositorio_sqlite import ClienteRepositorioSQLite
from models.database.repositories.quarto_repositorio_sqlite import QuartoRepositorioSQLite
from models.database.repositories.reserva_repositorio_sqlite import ReservaRepositorioSQLite

from controllers.quarto_controller import QuartoController
from controllers.cliente_controller import ClienteController
from controllers.estadia_controller import EstadiaController

from views.janela_principal import JanelaPrincipal


def main():

    banco = ConexaoBanco()

    try:
        repo_clientes = ClienteRepositorioSQLite(banco)
        repo_quartos = QuartoRepositorioSQLite(banco)
        repo_reservas = ReservaRepositorioSQLite(banco, repo_clientes, repo_quartos)

        ctrl_clientes = ClienteController(repo_clientes)
        ctrl_quartos = QuartoController(repo_quartos)
        ctrl_estadias = EstadiaController(repo_clientes, repo_quartos, repo_reservas)

        app = JanelaPrincipal(
            ctrl_clientes,
            ctrl_quartos,
            ctrl_estadias
        )

        app.mainloop()

    finally:
        banco.fechar()

if __name__ == "__main__":
    main()