class Calculadora:
    def __init__(self,numero1,numero2):
        self.numero1 = numero1
        self.numero2 = numero2
       
 
    def adicao(self):
        return self.numero1 + self.numero2
 
    def subtracao(self):
        return self.numero1 - self.numero2
 
    def multiplicacao(self):
        return self.numero1 * self.numero2
 
    def divisao(self):
        return self.numero1 / self.numero2
 
calcular = Calculadora (4,2)
 
print(calcular.divisao())
print(calcular.adicao())
print(calcular.multiplicacao())
print(calcular.subtracao())