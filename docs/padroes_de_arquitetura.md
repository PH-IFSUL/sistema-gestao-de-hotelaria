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
| Apresentação | Mostra dados e recebe as ações do atendente | Telas de clientes, quartos, reservas e estadias |
| Serviços | Valida os dados e executa os casos de uso | Cadastrar cliente, reservar quarto, fazer check-in e check-out |
| Domínio | Guarda os dados e o comportamento de cada entidade | `Cliente`, `Quarto`, `Estadia`, `Reserva`, `Fatura`, `Item` |
| Persistência | Grava e busca os dados | `ClienteRepositorio`, `QuartoRepositorio`, `EstadiaRepositorio` |

### Regra de dependência

- A camada de cima chama a camada de baixo.
- A camada de baixo nunca chama a camada de cima.
- A apresentação não acessa a persistência.
- O domínio não conhece a tela.

### Onde ficam as coisas

| Item | Camada | Localização |
|------|--------|-------------|
| Classes de domínio | Domínio | `src/models/` |
| Regras de negócio simples de uma entidade | Domínio | `src/models/` |
| Regras de negócio que usam mais de uma classe | Serviços | `src/controllers/` |
| Validação dos campos digitados | Serviços | `src/controllers/` |
| Acesso ao banco de dados | Persistência | `src/models/database/` |

## 2. MVC (Model, View, Controller)

O protótipo organiza o código em três pacotes principais dentro de `src/`.

| Parte | Diretório | Responsabilidade |
|-------|-----------|------------------|
| Model | `src/models/` | Classes de domínio (`Cliente`, `Quarto`, etc.) e contratos de repositório (`database/`) |
| View | `src/views/` | Telas em Tkinter, componentes e estilo visual |
| Controller | `src/controllers/` | Valida os dados e aplica as regras de negócio |
| Ligação | `src/main.py` | Cria os objetos e conecta as dependências |

### Relação entre o MVC e as camadas

| Camada | Parte do MVC no protótipo |
|--------|---------------------------|
| Apresentação | View (`src/views/`) |
| Serviços | Controller (`src/controllers/`) |
| Domínio | Model (`Cliente`, `Quarto`, `Estadia`, etc.) |
| Persistência | Model (repositórios SQLite e `ConexaoBanco`) |

No sistema, o Controller faz o papel da camada de Serviços. Os repositórios gravam os dados no SQLite e ficam em `src/models/database/repositories/`. A classe `ConexaoBanco` abre o banco e cria as tabelas a partir do `schema.sql`. Também existem repositórios em memória. Eles seguem as mesmas interfaces, então o `main.py` troca um pelo outro sem mudar o resto.

### Regras do MVC no código

- A View chama o Controller para buscar dados e executar ações.
- O Controller não usa Tkinter.
- O Model não conhece a View nem o Controller.
- O Controller usa a interface do repositório, não a implementação.
- O Controller envia os erros de regra de negócio como `ValueError`. A View mostra a mensagem.

## 3. Como as camadas se comunicam

Exemplo: cadastrar um cliente.

1. O atendente preenche o formulário e clica em "Cadastrar Cliente".
2. A View chama `ClienteController.cadastrar`.
3. O Controller remove os espaços e valida os campos. O CPF deve ter 11 números.
4. O Controller cria o objeto `Cliente`.
5. O Controller chama `ClienteRepositorio.salvar`.
6. O repositório recusa o cliente se o CPF já existe.
7. O Controller devolve uma mensagem de sucesso, ou a View mostra o erro.
8. A View atualiza a lista de clientes.

O atendente fala somente com a View. Os dados ficam no repositório. Nenhuma outra parte do sistema grava dados.

## Estado atual e próximos passos

| Item | Estado |
|------|--------|
| MVC | Implementado para clientes, quartos, reservas e estadias |
| Persistência em banco de dados | Implementada com SQLite (`src/models/database/`) |
| Persistência em memória | Mantida como alternativa. O `main.py` usa o SQLite |
| Reservas, estadias e faturas | Implementadas com controller, tela e banco |

## Decisões de arquitetura

| Decisão | Motivo | Alternativa descartada |
|---------|--------|------------------------|
| Arquitetura em camadas | Fácil de entender e de manter (requisito RNF04) | Tudo em um só arquivo |
| MVC no protótipo | A interface em Tkinter se encaixa bem no MVC | MVP e MVVM, que são mais complexos |
| Aplicação em um só programa | O sistema é pequeno | Microsserviços |
| Repositórios separados do domínio | Facilita a troca da memória pelo banco | Gravar direto no banco dentro do controller |
| Interface do repositório com `Protocol` | O controller depende do contrato, não da implementação | O controller usar a classe de memória direto |
