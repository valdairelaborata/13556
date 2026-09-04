class Carro:
    def __init__(self, marca, modelo, ano):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
    
    def descricao(self):
        return f'{self.marca} {self.modelo} {self.ano}'


# class Esportivo(Carro):
#     def __init__(self, marca, modelo, ano, velocidade_maxima):
#         super().__init__(marca, modelo, ano)
#         self.velocidade_maxima = velocidade_maxima

#     def descricao(self):
#         return super().descricao() + f' Velocidade máxima: {self.velocidade_maxima}'


class Esportivo(Carro):   
    def __init__(self, marca, modelo, ano, velocidade_maxima):
        super().__init__(marca, modelo, ano)
        self.velocidade_maxima = velocidade_maxima
    
    def descricao(self):
        return super().descricao() + f' Velocidade máxima: {self.velocidade_maxima}'


class Sedan(Carro):
    def __init__(self, marca, modelo, ano, tamanho_porta_malas):        
        super().__init__(marca, modelo, ano)
        self.tamanho_porta_malas = tamanho_porta_malas
    
    def descricao(self):
        return super().descricao() + f' Tamanho do porta malas: {self.tamanho_porta_malas}'


uno_escada = Esportivo("Fiat", "Uno", 1994, 100000)
uno_descricao = uno_escada.descricao()

virtus = Sedan("Volkswagem", "Virtus", 2018, "521L")
print(virtus.descricao())
