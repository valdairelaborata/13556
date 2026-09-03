
# 2 - Crie uma classe Calculadora com métodos para adição, subtração, multiplicação e divisão. Crie uma instância da classe e realize algumas operações.



class Calculadora:
    def __init__(self, resultado = 0):                
        self.resultado = resultado       
 
    def adicao(self, valor):
         self.resultado = self.resultado + valor
 
    def subtracao(self, valor):
        self.resultado = self.resultado - valor
 
    def multiplicacao(self, valor):
        self.resultado = self.resultado * valor
 
    def divisao(self, valor):
        self.resultado = self.resultado / valor

    def exibir(self):
        print(self.resultado)
 
calculadora = Calculadora ()
calculadora.exibir()

calculadora.adicao(4)
calculadora.exibir()

calculadora.adicao(2)
calculadora.exibir()

calculadora.adicao(4)
calculadora.exibir()

calculadora.multiplicacao(2)
calculadora.exibir()

calculadora.divisao(2)
calculadora.exibir()

calculadora.subtracao(2)
calculadora.exibir()


