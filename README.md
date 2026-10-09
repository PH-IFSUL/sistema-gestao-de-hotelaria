# Sistema de gestão de Hotelaria

## Descrição do projeto

Sistema de gestão hoteleira desenvolvida em Python, com controle dos quartos e reservas dos hóspedes, integrado com banco de dados.

### Padrões de Projeto:

O projeto segue uma arquitetura em camadas e o o pattern **MVC** para garantir a manutenibilidade e escalabilidade do código. As principais camadas são:

| Camada | Responsabilidade | Arquivos |
|--------|------------------|----------|
| **View** | Interface com o usuário | `src/views/` |
| **Controller** | Intermediação entre Model e View | `src/controllers/` |
| **Model** | Lógica de negócio e acesso a dados | `src/models/` |

**Para visualizar detalhes da arquitetura acesse:** [Detalhes da Arquitetura](docs/Arquitetura.md)

## Instruções para execução:

**Para clonar o repositório:**

```bash
git clone https://github.com/PH-IFSUL/sistema-gestao-de-hotelaria.git
```

**O Programa não precisa ser instalado, basta executar o arquivo main.py ou o comando:**

```bash
python src/main.py
```


## Integrantes do grupo, user do github e atribuições:

| Nome | GitHub | Responsabilidade |
|------|--------|------------------|
| Pedro Henrique dos Santos | [@PH-IFSUL](https://github.com/PH-IFSUL) | Banco e Testes |
| Róger André de Campos | [@RogerCampos97](https://github.com/RogerCampos97) | Backend e Frontend |
| Guilherme Guimarães Audibert | [@Guijermino](https://github.com/Guijermino) | Projeto |
| Guilherme Dallacort Zembruski | [@zembruski](https://github.com/zembruski) | Backend |

## Documentação

* [Requisitos Funcionais e Não Funcionais](docs/requisitos.md)
* [Regras de Negócio](docs/regras_de_negocio.md)

## Diagramas

* [Diagrama de Classes](docs/Class_diagrams.md)
* [Diagrama de Componentes](docs/diagrama_componentes.md)
* [Diagrama de Estrutura Composta](docs/composite_structure.png)


