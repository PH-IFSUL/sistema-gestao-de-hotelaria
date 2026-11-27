# Diagramas de Classes do Sistema

Este documento apresenta a modelagem de classes do **Sistema de Gestão de Hotelaria**. O sistema utiliza o padrão arquitetural **MVC (Model-View-Controller)**.

---

## 1. Diagrama de Classes Geral (Mermaid)

```mermaid
classDiagram
    direction TB

    namespace Models_Dominio {
        class Cliente {
            -_id : int | None
            -_nome : str
            -_cpf : str
            -_telefone : str
            -_email : str
            +get_id() int
            +set_id(id: int) void
            +get_nome() str
            +get_cpf() str
            +get_telefone() str
            +get_email() str
        }

        class Quarto {
            +TIPOS : list~str~
            -_numero : int
            -_tipo : str
            -_valor_diaria : float
            +estado : EstadoContexto
            +get_numero() int
            +get_tipo() str
            +get_valor_diaria() float
        }

        class Reserva {
            -_id : int | None
            -_hospede : Cliente
            -_quarto : Quarto
            -_data_checkin : date
            -_data_checkout : date
            -_status : str
            +hospede : Cliente
            +quarto : Quarto
            +data_checkin : date
            +data_checkout : date
            +get_numero_diarias() int
+           +calcular_total_estimado() float
        }

        class Estadia {
            -_id : int | None
            -_hospede : Cliente
            -_quarto : Quarto
            -_data_checkin : datetime
            -_data_checkout : datetime
            -_status : str
            -_reserva_id : int | None
            -_fatura : Fatura
            +get_numero_diarias() int
            +calcular_total_diarias() float
            +calcular_total_consumos() float
            +obter_total() float
            +adicionar_item(item: ItemFatura) void
        }

        class Item {
            -_id : int
            -_nome : str
            -_preco : float
            +id : int
            +nome : str
            +preco : float
        }

        class ItemFatura {
            -_id : int
            -_item : Item
            -_quantidade : int
            +id : int
            +item : Item
            +quantidade : int
        }

        class Fatura {
            -_id_estadia : int
            -_itens : list~ItemFatura~
            +adicionar_item(item: ItemFatura) void
            +calcular_total() float
        }
    }

    namespace Padrao_State {
        class EstadoContexto {
            -_state : Estado
            +set_estado(novo_estado: Estado) void
            +reservar(quarto: Quarto) void
            +check_in(quarto: Quarto) void
            +check_out(quarto: Quarto) void
            +iniciar_manutencao(quarto: Quarto) void
            +finalizar_manutencao(quarto: Quarto) void
            +finalizar_limpeza(quarto: Quarto) void
            +obter_atual() str
        }

        class Estado {
            <<abstract>>
            +reservar(quarto: Quarto)* void
            +check_in(quarto: Quarto)* void
            +check_out(quarto: Quarto)* void
            +iniciar_manutencao(quarto: Quarto)* void
            +finalizar_manutencao(quarto: Quarto)* void
            +finalizar_limpeza(quarto: Quarto)* void
            +obter_atual()* str
        }

        class Disponivel {
            +reservar(quarto: Quarto) void
            +check_in(quarto: Quarto) void
            +iniciar_manutencao(quarto: Quarto) void
            +obter_atual() str
        }

        class Reservado {
            +check_in(quarto: Quarto) void
            +obter_atual() str
        }

        class Ocupado {
            +check_out(quarto: Quarto) void
            +obter_atual() str
        }

        class Limpeza {
            +iniciar_manutencao(quarto: Quarto) void
            +finalizar_limpeza(quarto: Quarto) void
            +obter_atual() str
        }

        class Manutencao {
            +finalizar_manutencao(quarto: Quarto) void
            +obter_atual() str
        }
    }

    namespace Repositorios {
        class ClienteRepositorio {
            <<interface>>
            +salvar(cliente: Cliente)* void
            +remover(cpf_cliente: str)* bool
            +obter_todos()* list~Cliente~
            +buscar_por_id(id_busca: int)* Cliente
            +buscar_por_cpf(cpf_busca: str)* Cliente
            +atualizar(cliente: Cliente)* bool
        }

        class QuartoRepositorio {
            <<interface>>
            +adicionar(quarto: Quarto)* void
            +remover(numero_busca: int)* bool
            +listar()* list~Quarto~
            +buscar_por_numero(numero_busca: int)* Quarto
            +obter_tipos()* list~str~
            +atualizar_estado(quarto: Quarto)* bool
        }

        class ReservaRepositorio {
            <<interface>>
            +salvar(reserva: Reserva)* void
            +atualizar(reserva: Reserva)* bool
            +remover(id_reserva: int)* bool
            +listar()* list~Reserva~
            +buscar_por_id(id_reserva: int)* Reserva
            +existe_conflito(numero_quarto: int, data_inicio: date, data_fim: date, ignorar_id: int)* bool
        }

        class EstadiaRepositorio {
            <<interface>>
            +salvar(estadia: Estadia)* void
            +atualizar(estadia: Estadia)* bool
            +remover(id_estadia: int)* bool
            +listar()* list~Estadia~
            +buscar_por_id(id_busca: int)* Estadia
            +obter_fatura(id_estadia: int)* Fatura
            +listar_itens_catalogo()* list~Item~
            +adicionar_item_fatura(id_estadia: int, item: ItemFatura)* void
        }

        class ClienteRepositorioMemoria
        class QuartoRepositorioMemoria
        class ReservaRepositorioMemoria
        class EstadiaRepositorioMemoria

        class ClienteRepositorioSQLite
        class QuartoRepositorioSQLite
        class ReservaRepositorioSQLite
        class EstadiaRepositorioSQLite

        class ConexaoBanco {
            -_caminho : str
            -_conexao : Connection
            +conectar() Connection
            +obter_conexao() Connection
            +fechar() void
        }
    }

    namespace Controllers {
        class ClienteController {
            -_repo : ClienteRepositorio
            +cadastrar(nome: str, cpf: str, telefone: str, email: str) str
            +listar() list~Cliente~
            +remover(cpf: str) str
        }

        class QuartoController {
            -_repo : QuartoRepositorio
            +cadastrar(numero_str: str, tipo: str, valor_str: str) str
            +listar() list~Quarto~
            +remover(numero_str: str) str
            +obter_nome_estado(quarto: Quarto) str
            +obter_tag_estado(quarto: Quarto) str
            +alterar_estado(numero_str: str, novo_estado: str) str
        }

        class EstadiaController {
            -_cliente_repo : ClienteRepositorio
            -_quarto_repo : QuartoRepositorio
            -_reserva_repo : ReservaRepositorio
            -_estadia_repo : EstadiaRepositorio
            +listar_clientes(filtro: str) list~Cliente~
            +listar_quartos(filtro: str, apenas_disponiveis: bool) list~Quarto~
            +cadastrar_cliente(nome: str, cpf: str, telefone: str, email: str) Cliente
            +realizar_reserva(cliente: Cliente, quarto: Quarto, data_inicio: date, data_fim: date) Reserva
            +alterar_reserva(reserva_id: int, cliente: Cliente, quarto: Quarto, data_inicio: date, data_fim: date) Reserva
            +remover_reserva(reserva_id: int) void
            +obter_todas_reservas() list~Reserva~
            +listar_reservas_confirmadas(filtro: str) list~Reserva~
            +realizar_checkin(cliente: Cliente, quarto: Quarto, data_checkout: date, reserva: Reserva, data_checkin: datetime) Estadia
            +realizar_checkout(estadia_id: int, data_checkout: datetime) Estadia
            +listar_itens_catalogo() list~Item~
            +lancar_consumo(estadia_id: int, item_id: int, quantidade: int) Estadia
            +remover_estadia(estadia_id: int) void
            +obter_todas_estadias() list~Estadia~
        }
    }

    %% Relacionamentos do Domínio
    Reserva "0..*" --o "1" Cliente : reserva para
    Reserva "0..*" --> "1" Quarto : reserva
    Estadia "0..*" --o "1" Cliente : hóspede
    Estadia "0..*" --o "0..1" Quarto : alocado em
    Estadia ..> Reserva : origem opcional
    Estadia "1" *-- "1" Fatura : possui
    Fatura "1" *-- "0..*" ItemFatura : contém
    ItemFatura "0..*" --o "1" Item : refere-se a

    %% Relacionamentos do State Pattern
    Quarto "1" *-- "1" EstadoContexto : possui estado
    EstadoContexto "1" o-- "1" Estado : estado atual
    Estado <|-- Disponivel : implementa
    Estado <|-- Reservado : implementa
    Estado <|-- Ocupado : implementa
    Estado <|-- Limpeza : implementa
    Estado <|-- Manutencao : implementa

    %% Relacionamentos de Repositórios
    ClienteRepositorio <|.. ClienteRepositorioMemoria : realiza
    QuartoRepositorio <|.. QuartoRepositorioMemoria : realiza
    ReservaRepositorio <|.. ReservaRepositorioMemoria : realiza
    EstadiaRepositorio <|.. EstadiaRepositorioMemoria : realiza
    ClienteRepositorio <|.. ClienteRepositorioSQLite : realiza
    QuartoRepositorio <|.. QuartoRepositorioSQLite : realiza
    ReservaRepositorio <|.. ReservaRepositorioSQLite : realiza
    EstadiaRepositorio <|.. EstadiaRepositorioSQLite : realiza
    ClienteRepositorioSQLite --> ConexaoBanco : usa
    QuartoRepositorioSQLite --> ConexaoBanco : usa
    ReservaRepositorioSQLite --> ConexaoBanco : usa
    EstadiaRepositorioSQLite --> ConexaoBanco : usa

    %% Relacionamentos de Controllers
    ClienteController "1" --> "1" ClienteRepositorio : utiliza
    QuartoController "1" --> "1" QuartoRepositorio : utiliza
    EstadiaController "1" --> "1" ClienteRepositorio : utiliza
    EstadiaController "1" --> "1" QuartoRepositorio : utiliza
    EstadiaController "1" --> "1" ReservaRepositorio : utiliza
    EstadiaController "1" --> "1" EstadiaRepositorio : utiliza
```
