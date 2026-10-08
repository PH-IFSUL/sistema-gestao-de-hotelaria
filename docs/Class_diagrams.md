# Diagramas de Classes do Sistema

Este documento apresenta a modelagem de classes do **Sistema de Gestão de Hotelaria**. O sistema utiliza o padrão arquitetural **MVC (Model-View-Controller)**

---

## 1. Diagrama de Classes Geral (Mermaid)

```mermaid
classDiagram
    direction TB

    namespace Models_Domain {
        class Client {
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

        class Room {
            +TIPOS : list~str~
            -_numero : int
            -_tipo : str
            -_valor_diaria : float
            +estado : State_context
            +get_numero() int
            +get_tipo() str
            +get_valor_diaria() float
        }

        class Reservation {
            -_id : int | None
            -__guest : Client
            -__checkin : date
            -__checkout : date
            +guest : Client
            +checkin_date : date
            +checkout : date
        }

        class Guest_Stay {
            -_id : int | None
            -__guest : Client
            -__room_number : Room
            -__checkin_date : datetime
            -__checkout_date : datetime
            -__guest_bill : Guest_Bill
            +get_total() float
            +add_item(item: Bill_Item) void
        }

        class Item {
            -_id : int
            -__name : str
            -__price : float
            +id : int
            +name : str
            +price : float
        }

        class Bill_Item {
            -_id : int
            -__item : Item
            -__quantity : int
            +id : int
            +item : Item
            +quantity : int
        }

        class Guest_Bill {
            -_id_stay : int
            -__itens : list~Bill_Item~
            +add_itens(item: Bill_Item) void
            +calculate_total() float
        }
    }

    namespace Pattern_State {
        class State_context {
            -_state : State
            +set_estado(new_state: State) void
            +book(room: Room) void
            +check_in(room: Room) void
            +check_out(room: Room) void
            +start_maintenance(room: Room) void
            +end_maintenance(room: Room) void
            +finish_cleaning(room: Room) void
            +get_current() str
        }

        class State {
            <<abstract>>
            +book(room: Room)* void
            +check_in(room: Room)* void
            +check_out(room: Room)* void
            +start_maintenance(room: Room)* void
            +end_maintenance(room: Room)* void
            +finish_cleaning(room: Room)* void
            +get_current()* str
        }

        class Available {
            +book(room: Room) void
            +check_in(room: Room) void
            +start_maintenance(room: Room) void
            +get_current() str
        }

        class Reserved {
            +check_in(room: Room) void
            +get_current() str
        }

        class Ocupied {
            +check_out(room: Room) void
            +get_current() str
        }

        class Cleaning {
            +start_maintenance(room: Room) void
            +finish_cleaning(room: Room) void
            +get_current() str
        }

        class Maintenance {
            +end_maintenance(room: Room) void
            +get_current() str
        }
    }

    namespace Repositories {
        class Client_Repository {
            <<interface>>
            +save(cliente: Client)* void
            +delete(client_cpf: str)* bool
            +get_all()* list~Client~
            +find_by_id(id_query: int)* Client
            +find_by_Cpf(cpf_query: str)* Client
            +update(guest: Client)* bool
        }

        class In_Memory_Client_Repository {
            -_clients : list~Client~
            -__next_id : int
            +save(cliente: Client) void
            +delete(client_cpf: str) bool
            +get_all() list~Client~
            +find_by_id(id_query: int) Client
            +find_by_Cpf(cpf_query: str) Client
        }

        class Room_Repository {
            <<interface>>
            +add(quarto: Room)* void
            +delete(number_query: int)* bool
            +list()* list~Room~
            +find_by_number(number_query: int)* Room
            +get_types()* list~str~
        }

        class In_Memory_Room_Repository {
            -_quartos : list~Room~
            -_tipos : list~str~
            +add(quarto: Room) void
            +delete(number_query: int) bool
            +list() list~Room~
            +find_by_number(number_query: int) Room
            +get_types() list~str~
        }

        class Stay_Repository {
            <<interface>>
            +get_next_id()* int
            +save(estadia: Guest_Stay)* void
            +delete(client_id: int)* bool
            +get_bill(id_stay: int)* Guest_Bill
            +add_itens_to_bill(id_stay: int, item: Bill_Item)* void
            +find_by_id(id_query: int)* Guest_Stay
            +find_by_cpf(cpf_query: str)* Guest_Stay
            +get_date_reservations(date: date)* list~Guest_Stay~
        }
    }

    namespace Controllers {
        class Client_Controller {
            -_repo : Client_Repository
            +cadastrar(nome: str, cpf: str, telefone: str, email: str) str
            +listar() list~Client~
            +remover(cpf: str) str
        }

        class Room_Controller {
            -_repo : Room_Repository
            +cadastrar(numero_str: str, tipo: str, valor_str: str) str
            +listar() list~Room~
            +remover(numero_str: str) str
            +get_state_name(room: Room) str
            +get_state_tag(room: Room) str
        }
    }

    %% Relacionamentos do Domínio
    Reservation "0..*" --o "1" Client : reserva para
    Guest_Stay "0..*" --o "1" Client : hóspede
    Guest_Stay "0..*" --o "0..1" Room : alocado em
    Guest_Stay "1" *-- "1" Guest_Bill : possui
    Guest_Bill "1" *-- "0..*" Bill_Item : contém
    Bill_Item "0..*" --o "1" Item : refere-se a

    %% Relacionamentos do State Pattern
    Room "1" *-- "1" State_context : possui estado
    State_context "1" o-- "1" State : estado atual
    State <|-- Available : implementa
    State <|-- Reserved : implementa
    State <|-- Ocupied : implementa
    State <|-- Cleaning : implementa
    State <|-- Maintenance : implementa

    %% Relacionamentos de Repositórios
    Client_Repository <|.. In_Memory_Client_Repository : realiza
    Room_Repository <|.. In_Memory_Room_Repository : realiza

    %% Relacionamentos de Controllers
    Client_Controller "1" --> "1" Client_Repository : utiliza
    Room_Controller "1" --> "1" Room_Repository : utiliza
```
