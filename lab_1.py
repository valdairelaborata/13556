# 1- Crie uma classe chamada Carro com atributos marca e modelo. Adicione um método descricao() que retorna uma string formatada com a marca e o modelo do carro. Crie uma instância dessa classe e chame o método descricao().

class Carro:
    def __init__ (self, marca, modelo):
        self.marca = marca
        self.modelo = modelo
 
    def descricao(self):
        return (f'{self.marca} {self.modelo}')
 
Saveiro = Carro("Volkswagem", "Saveiro rebaixada")
print(Saveiro.descricao())
 