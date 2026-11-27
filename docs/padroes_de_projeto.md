# Padrões de Projeto

Este documento descreve os padrões de projeto usados no protótipo do Sistema de Gestão de Hotelaria. Cada padrão tem o motivo da escolha e o arquivo onde aparece no código.

## Resumo

| Padrão | Onde aparece | Para que serve |
|--------|--------------|----------------|
| Repository | `src/models/database/` | Separar o armazenamento dos dados do resto do sistema |
| Injeção de dependência | `src/main.py` | Entregar a cada classe os objetos de que ela precisa |
| MVC | `src/models/`, `src/views/`, `src/controllers/` | Separar dados, regras e tela |
| State | `src/models/estado_quarto.py` | Controlar o que cada situação do quarto permite |
| Singleton | `src/views/estilo/ajudante_estilo.py` | Ter uma só instância dos estilos da tela |

## 1. Repository

**Problema.** O sistema precisa guardar clientes, quartos, reservas e estadias. O armazenamento pode mudar, de memória para banco de dados. O restante do código não deve mudar quando isso acontecer.

**Solução.** Cada entidade tem uma classe de repositório com interface definida via `Protocol`. Só essa classe sabe como os dados são guardados. As outras classes usam os métodos `salvar`, `listar`, `buscar` e `remover`.

**Onde está.** As interfaces `ClienteRepositorio`, `QuartoRepositorio`, `ReservaRepositorio` e `EstadiaRepositorio` ficam em `src/models/database/interfaces/`. As implementações ficam em `src/models/database/repositories/`: uma versão em memória (`...Memoria`) e uma versão SQLite (`...SQLite`) para cada interface.

```python
class ClienteRepositorioMemoria:
    def __init__(self):
        self._clientes: list[Cliente] = []

    def salvar(self, cliente: Cliente) -> None:
        if self.buscar_por_cpf(cliente.get_cpf()):
            raise ValueError(f"Já existe um cliente com o CPF {cliente.get_cpf()}.")
        self._clientes.append(cliente)
```

**Decisão de projeto.** A regra "o CPF é único" e a regra "o número do quarto é único" ficam dentro do repositório. Assim, nenhum caminho do sistema consegue gravar um dado repetido.

**Como a troca foi feita.** A classe `ClienteRepositorioSQLite` implementa a mesma interface `ClienteRepositorio`. O controller e a view não mudaram. Só o `main.py` passou a criar a classe nova.

## 2. Injeção de dependência

**Problema.** Se o controller criasse o próprio repositório, ele ficaria preso a uma forma de armazenamento. Também seria difícil testar o controller sozinho.

**Solução.** O `main.py` cria os objetos e entrega cada um para quem precisa, pelo construtor.

**Onde está.** `src/main.py`, `src/controllers/` e `src/views/`.

```python
banco = ConexaoBanco()
repo_clientes = ClienteRepositorioSQLite(banco)
ctrl_clientes = ClienteController(repo_clientes)
app = JanelaPrincipal(ctrl_clientes, ctrl_quartos, ctrl_estadias)
```

**Decisão de projeto.** Nenhuma classe cria os objetos dos quais depende. Só o `main.py` conhece todas as camadas e liga uma na outra.

## 3. MVC (Model, View, Controller)

O MVC é também o padrão de arquitetura do sistema. A explicação completa está em [Padrões de Arquitetura](padroes_de_arquitetura.md). Aqui está o resumo do que cada camada faz no código.

| Camada | Arquivo/Pasta | Responsabilidade |
|--------|---------------|------------------|
| Model | `src/models/` | Classes de domínio (`Cliente`, `Quarto`, etc.) e repositórios |
| View | `src/views/` | Telas em Tkinter (`JanelaPrincipal`, abas, componentes de formulário) |
| Controller | `src/controllers/` | Valida os dados da tela e aplica as regras de negócio |

**Regras que o código segue:**

- A view chama o controller para buscar dados e executar ações.
- O controller não usa Tkinter.
- O model não conhece a view nem o controller.
- Erros de regra de negócio saem do controller como `ValueError`. A view mostra a mensagem para o usuário.

## Decisões de projeto

| Decisão | Motivo | Alternativa descartada |
|---------|--------|------------------------|
| Gravar os dados no SQLite | Os dados não se perdem ao fechar o sistema (RNF05) | Guardar só em memória |
| Usar repositórios em vez de listas soltas | Facilita a troca para o banco | Lista dentro do controller |
| Validar os campos no controller | A view fica simples | Validar dentro de cada tela |
| Atributos privados com métodos `get_` | Encapsulamento | Atributos públicos |

## Padrões estudados e não adotados

Estes padrões fazem sentido para o sistema, mas ainda não estão no código.

| Padrão | Uso possível | Situação |
|--------|--------------|----------|
| Observer | Atualizar a lista da tela quando um cadastro muda | Não implementado |
| Factory | Criar `Atendente` ou `Gerente` conforme o cargo | Será avaliado quando houver funcionários |

## 4. State

**Problema.** Um quarto age de forma diferente em cada situação. Não é permitido fazer check-in em um quarto em manutenção. Sem o padrão, o código teria `if` em muitos lugares.

**Solução.** Cada situação do quarto é uma classe: disponível, reservado, ocupado, limpeza e manutenção. O quarto guarda o estado atual e repassa cada operação para ele. O estado recusa a operação que não é permitida.

**Onde está.** `src/models/estado_quarto.py` (`EstadoContexto`, `Estado`, `Disponivel`, `Reservado`, `Ocupado`, `Limpeza`, `Manutencao`).

**Decisão de projeto.** A regra "o que é permitido em cada situação" fica nas classes de estado. O controller chama a operação e mostra o erro para o usuário.

## 5. Singleton

**Problema.** Os estilos da tela devem ser iguais em todas as abas. Criar o estilo várias vezes gera repetição.

**Solução.** A classe `AjudanteEstilo` tem uma só instância. Todas as telas usam essa instância.

**Onde está.** `src/views/estilo/ajudante_estilo.py`. O método `__new__` devolve sempre a mesma instância.
