
class Carro:
    def __init__(self, cor, placa, status, tipo):
        self.cor = cor
        self.placa = placa
        self.status = status
        self.tipo = tipo

    
    def ligar(self):
        self.status = "ligado"

    def desligar(self):
        self.status = "Desligado"



celta = Carro("Vermelha", "AKH 2522", "desligado", "hatch")
fusca = Carro("Preta", "XTO 2536", "Ligado", "1500")

celta.ligar()
fusca.desligar()