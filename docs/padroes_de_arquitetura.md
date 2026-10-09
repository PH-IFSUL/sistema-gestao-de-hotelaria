# Padrões de Arquitetura

Este documento descreve os padrões de arquitetura do Sistema de Gestão de Hotelaria. Ele explica as camadas, o que cada camada faz e como as camadas se comunicam.

## Resumo

| Padrão | Função no sistema |
|--------|-------------------|
| Arquitetura em camadas | Divide o sistema em quatro níveis, cada um com uma responsabilidade |
| MVC | Organiza o código do protótipo em Model, View e Controller |

Os dois padrões trabalham juntos. A arquitetura em camadas é a visão geral do sistema. O MVC é a forma como o protótipo em Tkinter organiza o código dentro dessas camadas.

## 1. Arquitetura em camadas

O sistema tem quatro camadas. Cada camada usa somente a camada que está logo abaixo.

```
+-------------------------------+
| 1. Apresentação               |  telas e formulários
+-------------------------------+
| 2. Serviços (aplicação)       |  casos de uso e regras de negócio
+-------------------------------+
| 3. Domínio                    |  classes do hotel
+-------------------------------+
| 4. Persistência               |  repositórios e banco de dados
+-------------------------------+
```

| Camada | O que faz | Exemplos |
|--------|-----------|----------|
| Apresentação | Mostra dados e recebe as ações do atendente | Telas de cliente e de quarto |
| Serviços | Valida os dados e executa os casos de uso | Cadastrar cliente, cadastrar quarto |
| Domínio | Guarda os dados e o comportamento de cada entidade | `Cliente`, `Quarto` |
| Persistência | Grava e busca os dados | `ClienteRepositorio`, `QuartoRepositorio` |

### Regra de dependência

- A camada de cima chama a camada de baixo.
- A camada de baixo nunca chama a camada de cima.
- A apresentação não acessa a persistência.
- O domínio não conhece a tela.

### Onde ficam as coisas

| Item | Camada |
|------|--------|
| Classes de domínio | Domínio |
| Regras de negócio simples de uma entidade | Domínio |
| Regras de negócio que usam mais de uma classe | Serviços |
| Validação dos campos digitados | Serviços |
| Acesso ao banco de dados | Persistência |

## 2. MVC (Model, View, Controller)

O protótipo usa o MVC com três arquivos.

| Parte | Arquivo | Responsabilidade |
|-------|---------|------------------|
| Model | `model.py` | Classes `Cliente` e `Quarto` e os repositórios |
| View | `view.py` | Telas em Tkinter |
| Controller | `controller.py` | Valida os dados e aplica as regras de negócio |
| Ligação | `main.py` | Cria os objetos e liga uma parte na outra |

### Relação entre o MVC e as camadas

| Camada | Parte do MVC no protótipo |
|--------|---------------------------|
| Apresentação | View (`view.py`) |
| Serviços | Controller (`controller.py`) |
| Domínio | Model (`Cliente`, `Quarto`) |
| Persistência | Model (`ClienteRepositorio`, `QuartoRepositorio`) |

No protótipo, o Controller faz o papel da camada de Serviços. Os repositórios guardam os dados em memória e ficam em `model.py`. Quando o banco de dados for ligado, os repositórios passam a gravar no banco. Os outros arquivos não mudam.

### Regras do MVC no código

- A View chama somente o Controller.
- O Controller não usa Tkinter.
- O Model não conhece a View nem o Controller.
- O Controller envia os erros de regra de negócio como `ValueError`. A View mostra a mensagem.

## 3. Como as camadas se comunicam

Exemplo: cadastrar um cliente.

1. O atendente preenche o formulário e clica em "Cadastrar Cliente".
2. A View chama `ClienteController.cadastrar`.
3. O Controller remove os espaços e valida os campos. O CPF deve ter 11 números.
4. O Controller cria o objeto `Cliente`.
5. O Controller chama `ClienteRepositorio.adicionar`.
6. O repositório recusa o cliente se o CPF já existe.
7. O Controller devolve uma mensagem de sucesso, ou a View mostra o erro.
8. A View atualiza a lista de clientes.

O atendente fala somente com a View. Os dados ficam no repositório. Nenhuma outra parte do sistema grava dados.

## Estado atual e próximos passos

| Item | Estado |
|------|--------|
| MVC no protótipo | Implementado para clientes e quartos |
| Persistência em memória | Implementada |
| Persistência em banco de dados | Será feita na próxima etapa |
| Reservas, hospedagens e pagamentos | Estão nos diagramas. Ainda não estão no protótipo |

## Decisões de arquitetura

| Decisão | Motivo | Alternativa descartada |
|---------|--------|------------------------|
| Arquitetura em camadas | Fácil de entender e de manter (requisito RNF04) | Tudo em um só arquivo |
| MVC no protótipo | A interface em Tkinter se encaixa bem no MVC | MVP e MVVM, que são mais complexos |
| Aplicação em um só programa | O sistema é pequeno | Microsserviços |
| Repositórios separados do domínio | Facilita a troca da memória pelo banco | Gravar direto no banco dentro do controller |
