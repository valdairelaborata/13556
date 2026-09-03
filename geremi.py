class Carro:
    def __init__ (self, modelo, marca):
        self.modelo = modelo
        self.marca= marca
   
    def descricao(self):
       return  f"a marca deste carro é um { self.marca}, { self.modelo}"
 
 
volvo = Carro("C60 -2.0 - 2012", "volvo")

print (volvo.descricao())
 