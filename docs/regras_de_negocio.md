# Regras de Negócio

Regras simples de uma entidade ficam na **classe de domínio** (Model).  
Regras que envolvem mais de uma classe ficam no **Controller**.

---

## RN01 — Disponibilidade de quarto para reserva
**Onde:** `ReservaController`

Antes de criar uma reserva, o sistema verifica se o quarto está disponível (`ocupado = False`) e se não há outra reserva ativa para o mesmo período.

```python
if quarto.ocupado:
    raise ValueError("Quarto já está ocupado.")
if reserva_dao.existe_conflito(quarto, data_entrada, data_saida):
    raise ValueError("Já existe reserva para este quarto no período informado.")
```

---

## RN02 — Período mínimo de reserva
**Onde:** `Reserva` (Model)

A data de saída deve ser pelo menos 1 dia após a data de entrada.

```python
def get_numero_diarias(self):
    dias = (self.data_saida - self.data_entrada).days
    if dias < 1:
        raise ValueError("A saída deve ser ao menos 1 dia após a entrada.")
    return dias
```

---

## RN03 — Check-in exige reserva ativa
**Onde:** `ReservaController`

O check-in só pode ser realizado para reservas com status `CONFIRMADA`. Após o check-in, o quarto é marcado como `ocupado = True`.

```python
if reserva.status != "CONFIRMADA":
    raise ValueError("Check-in só pode ser realizado para reservas confirmadas.")
quarto.ocupado = True
```

---

## RN04 — Cálculo do total no check-out
**Onde:** `Reserva.calcular_total()` (Model)

```
Total = (número de diárias × valor da diária) + soma dos consumos
```

```python
def calcular_total(self):
    total_diarias = self.get_numero_diarias() * self.quarto.valor_diaria
    total_consumos = sum(p.valor for p in self.consumos)
    return total_diarias + total_consumos
```

---

## RN05 — CPF único por hóspede
**Onde:** `HospedeController`

Não é permitido cadastrar dois hóspedes com o mesmo CPF.

```python
if hospede_dao.existe_por_cpf(cpf):
    raise ValueError(f"Já existe um hóspede com o CPF: {cpf}")
```

---

## Resumo

| Regra | Camada | Onde |
|-------|--------|------|
| RN01 | Controller | `ReservaController.criar_reserva()` |
| RN02 | Model | `Reserva.get_numero_diarias()` |
| RN03 | Controller | `ReservaController.realizar_checkin()` |
| RN04 | Model | `Reserva.calcular_total()` |
| RN05 | Controller | `HospedeController.cadastrar()` |
