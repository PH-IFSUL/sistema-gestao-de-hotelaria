from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
'''
Info_data é uma classe que representa informações de criação e atualização de dados.
'''
@dataclass
class Info_data:
    data_criacao: datetime = field(default_factory=datetime.now)
    data_atualizado: datetime = field(default_factory=datetime.now)
    data_checkin_previsto: Optional[datetime] = None
    data_checkout_previsto: Optional[datetime] = None
    data_checkin: Optional[datetime] = None
    data_checkout: Optional[datetime] = None

    def atualizar_data(self):
        self.data_atualizado = datetime.now()

    @staticmethod
    def formatar_data(data: datetime):
        return data.strftime("%d/%m/%Y %H:%M:%S")

    @staticmethod
    def intervalo_entre_datas(final: datetime, primeira: datetime):
        intervalo = final - primeira
        return intervalo

    def calcular_tempo_desde_ultimo_update(self):
        return Info_data.intervalo_entre_datas(datetime.now(), self.data_atualizado)

    def calcular_tempo_ate_checkin_previsto(self):
        if self.data_checkin_previsto is None:
            return "Data de check-in previsto não definida."
        return Info_data.intervalo_entre_datas(datetime.now(), self.data_checkin_previsto)

    def calcular_tempo_desde_checkout_previsto(self):
        if self.data_checkout_previsto is None:
            return "Data de checkout previsto não definida."
        return Info_data.intervalo_entre_datas(datetime.now(), self.data_checkout_previsto)

    def inserir_datas_previstas(self, checkin_previsto: datetime, checkout_previsto: datetime):
        self.data_checkin_previsto = checkin_previsto
        self.data_checkout_previsto = checkout_previsto

    def realizar_checkin(self):
        self.data_checkin = datetime.now()
        self.atualizar_data()

    def realizar_checkout(self):
        self.data_checkout = datetime.now()
        self.atualizar_data()



    def reservar(self, checkin_previsto: datetime, checkout_previsto: datetime):
        self.inserir_datas_previstas(checkin_previsto, checkout_previsto)
        self.atualizar_data()