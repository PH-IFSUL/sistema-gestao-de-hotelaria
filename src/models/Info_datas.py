from dataclasses import dataclass, field
from datetime import datetime
'''
Info_data é uma classe que representa informações de criação e atualização de dados.
'''
@dataclass
class Info_data:
    data_criacao: datetime = field(default=datetime.now())
    data_atualizado: datetime = field(default=datetime.now())
    data_checkin_previsto: datetime = field(default=None)
    data_checkout_previsto: datetime = field(default=None)
    data_checkin: datetime = field(default=None)
    data_checkout: datetime = field(default=None)

def atualizar_data(self):
        self.data_atualizado = datetime.now()

@staticmethod
def formatar_data(data: datetime):
    return data.strftime("%d/%m/%Y %H:%M:%S")

@staticmethod
def calcular_intervalo_entre_datas(final: datetime, primeira: datetime):
    intervalo = final - primeira
    total_segundos = int(intervalo.total_seconds())
    dias = total_segundos // 86400
    horas = (total_segundos % 86400) // 3600
    minutos = (total_segundos % 3600) // 60
    segundos = total_segundos % 60
    tempo_completo = f"{dias}d {horas:02d}:{minutos:02d}:{segundos:02d}"
    return(f": {tempo_completo}")

def calcular_tempo_desde_ultimo_update(self):
    return Info_data.calcular_intervalo_entre_datas(datetime.now(), self.data_atualizado)

def calcular_tempo_desde_checkin_previsto(self):
    if self.data_checkin_previsto is None:
        return "Data de check-in previsto não definida."
    return Info_data.calcular_intervalo_entre_datas(datetime.now(), self.data_checkin_previsto)

def calcular_tempo_desde_checkout_previsto(self):
    if self.data_checkout_previsto is None:
        return "Data de checkout previsto não definida."
    return Info_data.calcular_intervalo_entre_datas(datetime.now(), self.data_checkout_previsto)
