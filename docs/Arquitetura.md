
## 1. Documentação Explicativa das Camadas e Classes
O sistema utiliza o padrão arquitetural **MVC (Model-View-Controller)** em Python, combinado com padrões de projeto comportamentais e estruturais avançados:
- **State Pattern**: Para o controle de ciclo de vida e gerenciamento de transição de estados dos quartos do hotel.
- **Repository Pattern**: Para desacoplar a camada de negócio da persistência de dados (através de interfaces `Protocol`).

### 1.1. Camada de Domínio (`src/models/`)

A camada de domínio agrupa as entidades fundamentais do negócio hoteleiro.

#### **`Client`** ([`client.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/client/client.py))
Representa o cliente/hóspede cadastrado no sistema.
- **Atributos**:
  - `_id`: Identificador único do cliente (opcional até ser atribuído pelo repositório).
  - `_nome`: Nome completo do cliente.
  - `_cpf`: CPF do cliente (usado como chave de validação e busca).
  - `_telefone`: Telefone de contato.
  - `_email`: Endereço de e-mail.
- **Métodos Principais**:
  - Encapsuladores `get_id()`, `set_id()`, `get_nome()`, `get_cpf()`, `get_telefone()`, `get_email()`.

#### **`Room`** ([`room.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/room/room.py))
Representa a unidade física de acomodação (quarto) do hotel.
- **Atributos**:
  - `TIPOS`: Lista estática de tipos permitidos (`["Simples", "Duplo", "Suíte"]`).
  - `_numero`: Número identificador do quarto.
  - `_tipo`: Categoria do quarto (Simples, Duplo ou Suíte).
  - `_valor_diaria`: Preço cobrado por noite/diária.
  - `estado`: Instância de `State_context` responsável pelo controle do estado atual.

#### **`Reservation` e `Guest_Stay`** ([`stay_info.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/client/stay_info.py))
- **`Reservation`**: Registra uma reserva antecipada vinculando um `Client` às datas de check-in e check-out informadas.
- **`Guest_Stay`**: Modela a estadia real/ativa do cliente no hotel. Ela associa o cliente (`Client`) ao quarto (`Room`), guarda as datas reais da hospedagem e mantém a fatura da estadia (`Guest_Bill`).

#### **`Guest_Bill`, `Item` e `Bill_Item`** ([`invoice.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/invoice/invoice.py) & [`itens.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/invoice/itens.py))
- **`Item`**: Representa um produto ou serviço oferecido pelo hotel (ex: Frigobar, Lavanderia, Serviço de Quarto).
- **`Bill_Item`**: Registra o item consumido e a quantidade associada em uma determinada comanda/fatura.
- **`Guest_Bill`**: Gerencia a conta do hóspede durante a estadia, calculando o valor total consumido (`calculate_total()`).

---

### 1.2. Padrão de Projeto: State Pattern ([`state_room.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/room/state_room.py))

O padrão **State** permite alterar dinamicamente o comportamento da classe `Room` conforme o seu estado atual, evitando múltiplos comandos condicionais (`if/else`) espalhados pelo código.

```
Available ──(book)──> Reserved ──(check_in)──> Ocupied ──(check_out)──> Cleaning ──(finish_cleaning)──> Available
    │                                                                        │
    └──(start_maintenance)───────────────> Maintenance <──(start_maint.)─────┘
                                               │
                                      (end_maintenance)
                                               ▼
                                            Cleaning
```

#### **Componentes do State**:
1. **`State_context`**: Funciona como o contexto exposto para a classe `Room`. Armazena a referência para o estado concreto (`_state`) e delega as chamadas de transição (`book()`, `check_in()`, `check_out()`, etc.).
2. **`State` (Classe Base Abstrata - ABC)**: Define a interface comum para todos os estados concretos com os métodos decorados com `@abstractmethod`.
3. **Estados Concretos**:
   - **`Available` (Disponível)**: Quarto pronto para receber novos hóspedes ou entrar em manutenção.
   - **`Reserved` (Reservado)**: Quarto reservado aguardando check-in do hóspede.
   - **`Ocupied` (Ocupado)**: Quarto com hospedagem ativa em andamento.
   - **`Cleaning` (Em Limpeza)**: Quarto recém desocupado aguardando governança/limpeza antes de voltar a ficar disponível.
   - **`Maintenance` (Em Manutenção)**: Quarto bloqueado para reparos técnicos ou manutenção preventiva.

---

### 1.3. Padrão de Projeto: Repository Pattern (`src/models/database/`)

O **Repository Pattern** isola a lógica de domínio do acesso a dados. O sistema utiliza `typing.Protocol` do Python para definir contratos/interfaces estáticas.

#### **Interfaces (`src/models/database/interfaces/`)**:
- **`Client_Repository`** ([`client_repository_interface.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/database/interfaces/client_repository_interface.py)): Interface com as operações essenciais para clientes (`save`, `delete`, `get_all`, `find_by_id`, `find_by_Cpf`, `update`).
- **`Room_Repository`** ([`room_repository_interface.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/database/interfaces/room_repository_interface.py)): Interface para operações com quartos (`add`, `delete`, `list`, `find_by_number`, `get_types`).
- **`Stay_Repository`** ([`stay_interface.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/database/interfaces/stay_interface.py)): Interface para gestão de estadias e faturas.

#### **Implementações Concretas (`src/models/database/repositories/`)**:
- **`In_Memory_Client_Repository`** ([`client_memory_repository.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/database/repositories/client_memory_repository.py)): Implementa `Client_Repository` mantendo os registros em memória através de listas Python e controle de ID incremental (`__next_id`).
- **`In_Memory_Room_Repository`** ([`room_memory_repository.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/database/repositories/room_memory_repository.py)): Implementa `Room_Repository` armazenando a lista de quartos cadastrados em memória.

---

### 1.4. Camada de Controladores / Controllers (`src/controllers/`)

Os controladores realizam a intermediação entre as telas (Views) e as regras de negócio do Domínio.

- **`Client_Controller`** ([`client_controller.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/controllers/client_controller.py)):
  - Valida as entradas do formulário (obrigatoriedade de campos, formatação e 11 dígitos numéricos do CPF).
  - Interage com `Client_Repository` para salvar, listar ou excluir clientes.
- **`Room_Controller`** ([`room_controller.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/controllers/room_controller.py)):
  - Valida dados do quarto (número inteiro positivo, obrigatoriedade de tipo e conversão do valor da diária float).
  - Gerencia quartos através de `Room_Repository`.
  - Provê utilitários para consultar o nome do estado (`get_state_name()`) e a tag textual do estado (`get_state_tag()`).
