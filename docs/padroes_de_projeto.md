# Padrões de Projeto

Este documento descreve os padrões de projeto usados no protótipo do Sistema de Gestão de Hotelaria. Cada padrão tem o motivo da escolha e o arquivo onde aparece no código.

## Resumo

| Padrão | Onde aparece | Para que serve |
|--------|--------------|----------------|
| Repository | `model.py` | Separar o armazenamento dos dados do resto do sistema |
| Injeção de dependência | `main.py` | Entregar a cada classe os objetos de que ela precisa |
| MVC | `model.py`, `view.py`, `controller.py` | Separar dados, regras e tela |

## 1. Repository

**Problema.** O sistema precisa guardar clientes e quartos. Hoje os dados ficam em memória. Mais tarde eles vão para o banco de dados. O restante do código não deve mudar quando isso acontecer.

**Solução.** Cada entidade tem uma classe de repositório. Só essa classe sabe como os dados são guardados. As outras classes usam os métodos `adicionar`, `listar`, `buscar` e `remover`.

**Onde está.** `ClienteRepositorio` e `QuartoRepositorio`, em `model.py`.

```python
class ClienteRepositorio:
    def __init__(self):
        self._clientes: list[Cliente] = []

    def adicionar(self, cliente: Cliente) -> None:
        if self.buscar_por_cpf(cliente.get_cpf()):
            raise ValueError("Já existe um cliente com este CPF.")
        self._clientes.append(cliente)
```

**Decisão de projeto.** A regra "o CPF é único" e a regra "o número do quarto é único" ficam dentro do repositório. Assim, nenhum caminho do sistema consegue gravar um dado repetido.

**Como trocar para o banco de dados.** Criar uma classe nova, por exemplo `ClienteRepositorioSQLite`, com os mesmos métodos. O controller e a view não mudam. Só o `main.py` passa a criar a classe nova.

## 2. Injeção de dependência

**Problema.** Se o controller criasse o próprio repositório, ele ficaria preso a uma forma de armazenamento. Também seria difícil testar o controller sozinho.

**Solução.** O `main.py` cria os objetos e entrega cada um para quem precisa, pelo construtor.

**Onde está.** `main.py`, `controller.py` e `view.py`.

```python
repo_clientes = ClienteRepositorio()
ctrl_clientes = ClienteController(repo_clientes)
app = JanelaPrincipal(ctrl_clientes, ctrl_quartos)
```

**Decisão de projeto.** Nenhuma classe cria os objetos dos quais depende. Só o `main.py` conhece todas as camadas e liga uma na outra.

## 3. MVC (Model, View, Controller)

O MVC é também o padrão de arquitetura do sistema. A explicação completa está em [arquitetura.md](arquitetura.md). Aqui está o resumo do que cada camada faz no código.

| Camada | Arquivo | Responsabilidade |
|--------|---------|------------------|
| Model | `model.py` | Classes `Cliente` e `Quarto` e seus repositórios |
| View | `view.py` | Telas em Tkinter. Mostra dados e recebe cliques |
| Controller | `controller.py` | Valida os dados da tela e aplica as regras de negócio |

**Regras que o código segue:**

- A view chama apenas o controller. Ela não usa o model diretamente.
- O controller não usa Tkinter.
- O model não conhece a view nem o controller.
- Erros de regra de negócio saem do controller como `ValueError`. A view mostra a mensagem para o usuário.

## Decisões de projeto

| Decisão | Motivo | Alternativa descartada |
|---------|--------|------------------------|
| Guardar os dados em memória no protótipo | Entrega rápida da primeira versão | Banco de dados já no protótipo |
| Usar repositórios em vez de listas soltas | Facilita a troca para o banco | Lista dentro do controller |
| Validar os campos no controller | A view fica simples | Validar dentro de cada tela |
| Atributos privados com métodos `get_` | Encapsulamento | Atributos públicos |

## Padrões estudados e não adotados

Estes padrões fazem sentido para o sistema, mas ainda não estão no código. Por isso não fazem parte da implementação atual.

| Padrão | Uso possível | Situação |
|--------|--------------|----------|
| Observer | Atualizar a lista da tela quando um cadastro muda | Não implementado |
| Singleton | Uma única conexão com o banco de dados | Será avaliado na etapa do banco |
| Factory | Criar `Atendente` ou `Gerente` conforme o cargo | Será avaliado quando houver funcionários |
