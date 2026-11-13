## 1. Documentação Explicativa das Camadas e Classes
O sistema utiliza o padrão arquitetural **MVC (Model-View-Controller)** em Python, combinado com padrões de projeto:
- **State Pattern**: Para o controle de ciclo de vida e gerenciamento de transição de estados dos quartos do hotel.
- **Repository Pattern**: Para desacoplar a camada de negócio da persistência de dados (através de interfaces `Protocol`).

### 1.1. Camada de Domínio (`src/models/`)

A camada de domínio agrupa as entidades fundamentais do negócio hoteleiro, localizadas diretamente em `src/models/`.

#### **`Cliente`** ([`cliente.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/cliente.py))
Representa o cliente/hóspede cadastrado no sistema.
- **Atributos**:
  - `_id`: Identificador único do cliente (opcional até ser atribuído pelo repositório).
  - `_nome`: Nome completo do cliente.
  - `_cpf`: CPF do cliente (usado como chave de validação e busca).
  - `_telefone`: Telefone de contato.
  - `_email`: Endereço de e-mail.
- **Métodos Principais**:
  - Encapsuladores `get_id()`, `set_id()`, `get_nome()`, `get_cpf()`, `get_telefone()`, `get_email()`.

#### **`Quarto`** ([`quarto.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/quarto.py))
Representa a unidade física de acomodação (quarto) do hotel.
- **Atributos**:
  - `TIPOS`: Lista estática de tipos permitidos (`["Simples", "Duplo", "Suíte"]`).
  - `_numero`: Número identificador do quarto.
  - `_tipo`: Categoria do quarto (Simples, Duplo ou Suíte).
  - `_valor_diaria`: Preço cobrado por noite/diária.
  - `estado`: Instância de `EstadoContexto` responsável pelo controle do estado atual.

#### **`Reserva` e `Estadia`** ([`estadia.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/estadia.py))
- **`Reserva`**: Registra uma reserva antecipada vinculando um `Cliente` às datas de check-in e check-out informadas.
- **`Estadia`**: Modela a estadia real/ativa do cliente no hotel. Ela associa o cliente (`Cliente`) ao quarto (`Quarto`), guarda as datas reais da hospedagem e mantém a fatura da estadia (`Fatura`).

#### **`Fatura`, `Item` e `ItemFatura`** ([`fatura.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/fatura.py) & [`item.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/item.py))
- **`Item`**: Representa um produto ou serviço oferecido pelo hotel (ex: Frigobar, Lavanderia, Serviço de Quarto).
- **`ItemFatura`**: Registra o item consumido e a quantidade associada em uma determinada comanda/fatura.
- **`Fatura`**: Gerencia a conta do hóspede durante a estadia, calculando o valor total consumido (`calcular_total()`).

---

### 1.2. Padrão de Projeto: State Pattern ([`estado_quarto.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/estado_quarto.py))

O padrão **State** permite alterar dinamicamente o comportamento da classe `Quarto` conforme o seu estado atual, evitando múltiplos comandos condicionais (`if/else`) espalhados pelo código.

```
Disponivel ──(reservar)──> Reservado ──(check_in)──> Ocupado ──(check_out)──> Limpeza ──(finalizar_limpeza)──> Disponivel
    │                                                                        │
    └──(iniciar_manutencao)───────────────> Manutencao <──(iniciar_manut.)────┘
                                                │
                                       (finalizar_manutencao)
                                                ▼
                                             Limpeza
```

#### **Componentes do State**:
1. **`EstadoContexto`**: Funciona como o contexto exposto para a classe `Quarto`. Armazena a referência para o estado concreto (`_state`) e delega as chamadas de transição (`reservar()`, `check_in()`, `check_out()`, etc.).
2. **`Estado` (Classe Base Abstrata - ABC)**: Define a interface comum para todos os estados concretos com os métodos decorados com `@abstractmethod`.
3. **Estados Concretos**:
   - **`Disponivel` (Disponível)**: Quarto pronto para receber novos hóspedes ou entrar em manutenção.
   - **`Reservado` (Reservado)**: Quarto reservado aguardando check-in do hóspede.
   - **`Ocupado` (Ocupado)**: Quarto com hospedagem ativa em andamento.
   - **`Limpeza` (Em Limpeza)**: Quarto recém desocupado aguardando governança/limpeza antes de voltar a ficar disponível.
   - **`Manutencao` (Em Manutenção)**: Quarto bloqueado para reparos técnicos ou manutenção preventiva.

---

### 1.3. Padrão de Projeto: Repository Pattern (`src/models/database/`)

O **Repository Pattern** isola a lógica de domínio do acesso a dados. O sistema utiliza `typing.Protocol` do Python para definir contratos/interfaces estáticas. Desta forma, a lógica de domínio não sabe como os dados são armazenados ou recuperados, podendo ser implementado em memória, arquivos JSON ou banco de dados relacional.

#### **Interfaces (`src/models/database/interfaces/`)**:
- **`ClienteRepositorio`** ([`cliente_repositorio_interface.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/database/interfaces/cliente_repositorio_interface.py)): Interface com as operações essenciais para clientes (`salvar`, `remover`, `obter_todos`, `buscar_por_id`, `buscar_por_cpf`, `atualizar`).
- **`QuartoRepositorio`** ([`quarto_repositorio_interface.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/database/interfaces/quarto_repositorio_interface.py)): Interface para operações com quartos (`adicionar`, `remover`, `listar`, `buscar_por_numero`, `obter_tipos`).
- **`EstadiaRepositorio`** ([`estadia_repositorio_interface.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/database/interfaces/estadia_repositorio_interface.py)): Interface para gestão de estadias e faturas.

#### **Implementações Concretas (`src/models/database/repositories/`)**:
- **`ClienteRepositorioMemoria`** ([`cliente_repositorio_memoria.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/database/repositories/cliente_repositorio_memoria.py)): Implementa `ClienteRepositorio` mantendo os registros em memória através de listas Python e controle de ID incremental (`_proximo_id`).
- **`QuartoRepositorioMemoria`** ([`quarto_repositorio_memoria.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/models/database/repositories/quarto_repositorio_memoria.py)): Implementa `QuartoRepositorio` armazenando a lista de quartos cadastrados em memória.

---

### 1.4. Camada de Controladores / Controllers (`src/controllers/`)

Os controladores realizam a intermediação entre as telas (Views) e as regras de negócio do Domínio.

- **`ClienteController`** ([`cliente_controller.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/controllers/cliente_controller.py)):
  - Valida as entradas do formulário (obrigatoriedade de campos, formatação e 11 dígitos numéricos do CPF).
  - Interage com `ClienteRepositorio` para salvar, listar ou excluir clientes.
- **`QuartoController`** ([`quarto_controller.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/controllers/quarto_controller.py)):
  - Valida dados do quarto (número inteiro positivo, obrigatoriedade de tipo e conversão do valor da diária float).
  - Gerencia quartos através de `QuartoRepositorio`.
  - Provê utilitários para consultar o nome do estado (`obter_nome_estado()`) e a tag textual do estado para uso na view (`obter_tag_estado()`).
- **`EstadiaController`** ([`estadia_controller.py`](file:///c:/Users/roger/OneDrive/Documentos/GitHub/sistema-gestao-de-hotelaria/src/controllers/estadia_controller.py)):
  - Gerencia o fluxo de reservas, check-in, check-out e vinculação com clientes e quartos.
