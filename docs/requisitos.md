# Requisitos do Sistema

## Requisitos Funcionais

| ID | Requisito | Descrição |
|----|-----------|-----------|
| RF01 | Cadastrar hóspede | Registrar hóspedes com nome, CPF e telefone |
| RF02 | Consultar hóspede | Buscar hóspede pelo CPF ou nome |
| RF03 | Cadastrar quarto | Registrar quartos com número, andar, quantidade de camas, ar-condicionado e disponibilidade |
| RF04 | Consultar disponibilidade | Listar quartos disponíveis para um período informado |
| RF05 | Criar reserva | Reservar quarto para um hóspede com datas de entrada e saída |
| RF06 | Cancelar reserva | Cancelar reserva antes do check-in |
| RF07 | Realizar check-in | Confirmar entrada do hóspede e marcar quarto como ocupado |
| RF08 | Registrar consumo | Adicionar produtos/serviços consumidos à reserva durante a estadia |
| RF09 | Realizar check-out | Encerrar a reserva e calcular o total a pagar |
| RF10 | Registrar pagamento | Registrar forma de pagamento e confirmar liquidação |
| RF11 | Cadastrar atendente | Registrar atendentes com nome, CPF e controle de acesso |
| RF12 | Consultar reservas | Listar reservas ativas e histórico por hóspede |

---

## Requisitos Não Funcionais

| ID | Categoria | Descrição |
|----|-----------|-----------|
| RNF01 | Usabilidade | A interface deve permitir realizar um check-in em no máximo cinco ações |
| RNF02 | Segurança | Acesso ao sistema protegido por login e senha do atendente |
| RNF03 | Desempenho | Consultas de disponibilidade devem retornar em menos de 2 segundos |
| RNF04 | Manutenibilidade | Código organizado em camadas (MVC) com responsabilidades bem separadas |
| RNF05 | Persistência | Dados armazenados em banco de dados para não serem perdidos ao encerrar o sistema |
