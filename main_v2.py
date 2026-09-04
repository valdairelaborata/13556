
class Carro:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo
        self.__velocidade = 0   

    @property
    def velocidade(self):
        return self.__velocidade

    @velocidade.setter
    def velocidade(self, valor):
        if valor >= 0:
            self.__velocidade = valor
        else:
            print("A velocidade não pode ser negativa!")
        

    def acelerar(self, valor):
        self.velocidade = valor


meu_carro = Carro("Toyota", "Corola")
meu_carro.acelerar(10)


print(meu_carro.velocidade)


