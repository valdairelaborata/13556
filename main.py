
import unittest

class Calculadora:
    def soma(self, a, b):        
        return a + b

    def soma_com_valor_adicional(self, a, b):
        valor_adicional = 2
        return self.soma(a, b) + valor_adicional

    def testeBoleano(self, valor):
        return valor > 0  # Retorna True se o valor for maior que 0, caso contrário retorna False




class TesteCalculadora(unittest.TestCase):

    def test_soma(self):
        calcculadora = Calculadora()
        resultado = calcculadora.soma(2, 3)
        self.assertEqual(resultado, 5)


    def test_soma_com_valor_adicional(self):
        calculadora = Calculadora()
        resultado = calculadora.soma_com_valor_adicional(2, 3)
        self.assertEqual(resultado, 7)  # Espera-se que o resultado seja 7 devido ao valor adicional de 2

    def test_boleano(self):
        calculadora = Calculadora()
        resultado = calculadora.testeBoleano(10)
        self.assertTrue(resultado)  # Verifica se o resultado é maior que 0 

unittest.main()
   