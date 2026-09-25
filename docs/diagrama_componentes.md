# Diagrama de Componentes UML

O diagrama abaixo representa a estrutura de componentes da arquitetura em camadas, mostrando como cada parte do sistema se comunica.

```mermaid
graph TD

    subgraph USUARIO["👤 Usuário (Funcionário)"]
        U[Recepcionista / Gerente]
    end

    subgraph L1["Camada de Apresentação"]
        MENU["Menu Principal (SistemaHotel)"]
        TELAS["Telas / Formulários (View)"]
    end

    subgraph L2["Camada de Serviços"]
        CS["ClienteService"]
        RS["ReservaService"]
        HS["HospedagemService"]
        PS["PagamentoService"]
    end

    subgraph L3["Camada de Domínio"]
        CL["Cliente"]
        FU["Funcionario (Recepcionista | Gerente)"]
        QU["Quarto / TipoQuarto"]
        RE["Reserva (StatusReserva)"]
        HO["Hospedagem / ServicoExtra"]
        PG["Pagamento (FormaPagamento)"]
    end

    subgraph L4["Camada de Persistência"]
        CDAO["ClienteDAO"]
        QDAO["QuartoDAO"]
        RDAO["ReservaDAO"]
        HDAO["HospedagemDAO"]
        PDAO["PagamentoDAO"]
    end

    subgraph BD["🗄️ Banco de Dados"]
        DB[(Hotel DB)]
    end

    U --> MENU
    MENU --> TELAS
    TELAS --> CS
    TELAS --> RS
    TELAS --> HS
    TELAS --> PS

    CS --> CL
    RS --> RE
    RS --> QU
    RS --> CL
    HS --> HO
    HS --> RE
    HS --> FU
    PS --> PG

    CS --> CDAO
    RS --> RDAO
    RS --> QDAO
    HS --> HDAO
    PS --> PDAO

    CDAO --> DB
    QDAO --> DB
    RDAO --> DB
    HDAO --> DB
    PDAO --> DB
```

## Como os componentes se comunicam

O usuário interage apenas com a **camada de apresentação**. Esta delega para os **serviços**, que coordenam as classes de **domínio** e acionam os **DAOs** para persistência. O banco de dados é acessado exclusivamente pela camada de persistência.
