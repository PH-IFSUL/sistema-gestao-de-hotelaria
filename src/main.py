from models.database.repositories.cliente_repositorio_memoria import ClienteRepositorioMemoria
from models.database.repositories.quarto_repositorio_memoria import QuartoRepositorioMemoria
from controllers.quarto_controller import QuartoController
from controllers.cliente_controller import ClienteController
from controllers.estadia_controller import EstadiaController
from views.janela_principal import JanelaPrincipal


def main():
    """
    Selecionar repositórios (aqui passa a implementação escolhida, não o protocolo/interface).
    Se as classes seguirem o mesmo contrato, ele aceita a implementação.
    """
    repo_clientes = ClienteRepositorioMemoria()
    repo_quartos = QuartoRepositorioMemoria()

    """
    Controller recebe o repositório escolhido.
    """
    ctrl_clientes = ClienteController(repo_clientes)
    ctrl_quartos = QuartoController(repo_quartos)
    stay_ctrl = EstadiaController(repo_clientes, repo_quartos)

    '''
    Abre a janela principal, que recebe os controladores
    '''
    app = JanelaPrincipal(ctrl_clientes, ctrl_quartos, stay_ctrl)
    '''
    Inicia o loop principal da aplicação
    '''
    app.mainloop()


if __name__ == "__main__":
    main()