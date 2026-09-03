class Calculadora:
 
    def add(self, a, b):
        return a + b
 
    def sub(self, a, b):
        return a - b
 
    def mult(self, a, b):
        return a * b
 
    def div(self, a, b):
        return a / b
 
 
calculadora = Calculadora()
numero1 = float(input("Digite o primeiro número: "))
 
numero2 = float(input("Digite o segundo número: "))
 
resultado_add = calculadora.add(numero1, numero2)
 
resultado_sub = calculadora.sub(numero1, numero2)
 
resultado_mult = calculadora.mult(numero1, numero2)
 
resultado_div = calculadora.div(numero1, numero2)
 
print(f"{resultado_add}")
print(f"{resultado_sub}")
print(f"{resultado_mult}")
print(f"{resultado_div}")