
class Carro:
    def __init__(self, marca, modelo, ano):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano

    def descricao(self):
        return f'{self.ano} {self.modelo} {self.marca}'
    

class CarroEsportivo(Carro):
    def __init__(self, marca, modelo, ano, velocidade_maxima):
        super().__init__(marca, modelo, ano)
        self.velocidade_maxima = velocidade_maxima

    def descricao(self):
        return super().descricao() + f' Velocidade máxima: {self.velocidade_maxima}'



class CarroSedan(Carro):
    def __init__(self, marca, modelo, ano, tamanho_porta_malas):
        super().__init__(marca, modelo, ano)
        self.tamanho_porta_malas = tamanho_porta_malas

    def descricao(self):
        return super().descricao() + f' Tamanho do porta malas: {self.tamanho_porta_malas}'



camaro_hatch  = CarroEsportivo("GM", "Celta", 2003, 220)   
print(camaro_hatch.descricao())

uno_de_escada = CarroEsportivo("Fiat" , "Uno", 2002, 300)
print(uno_de_escada.descricao())

prisma = CarroSedan("GM", "Prisma", 2004, "460L")
print(prisma.descricao())


