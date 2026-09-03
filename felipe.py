class Calc:
    def adicionar(self, a, b):
        return a + b
    def subtrair(self, a, b):
        return a - b
    def multiplicar(self, a, b):
        return a * b
    def dividir(self, a, b):
        return a / b
calc = Calc()
num1 = float(input("Digite o primeiro número: "))
num2 = float(input("Digite o segundo número: "))

resultado_adi = calc.adicionar(num1, num2)
resultado_sub = calc.subtrair(num1, num2)
resultado_mult = calc.multiplicar(num1, num2)
resultado_div = calc.dividir(num1, num2)

print(f"Adicao ({num1} + {num2}): {resultado_adi:.0f }")
print(f"Subtracao ({num1} - {num2}): {resultado_sub}")
print(f"Multiplicacao ({num1} * {num2}): {resultado_mult}")
print(f"Divisao ({num1} / {num2}): {resultado_div}")