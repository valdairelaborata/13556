import unittest
 
class ContaBancaria:
    def __init__(self, titular:str):
        self.__titular = titular
        self.__saldo = 0
   
    @property
    def saldo(self):
        return self.__saldo
   
    def depositar(self, valor):
        if valor <= 0:
            return 'Valor invalido'
        self.__saldo += valor
 
    def sacar(self, valor):
        if valor <= self.__saldo:
            self.__saldo -= valor
        if valor < 0:
            return 'Valor negativo'
        else:
            return 'Saldo insuficiente'
       
 
class TestContaBancaria(unittest.TestCase):
 
    def test_saldo(self):
        conta = ContaBancaria('João')
        self.assertEqual(conta.saldo, 0)
 
    def test_depositar_valor_positivo(self):
        conta = ContaBancaria('João')
        conta.depositar(50)
        self.assertEqual(conta.saldo, 50)
       
    def test_depositar_valor_invalido(self):
        conta = ContaBancaria('João')
        resultado = conta.depositar(-10)
        self.assertEqual(resultado, 'Valor invalido')
 
    def test_sacar_valor_valido(self):
        conta = ContaBancaria('João')
        conta.depositar(50)
        conta.sacar(20)
        self.assertEqual(conta.saldo, 30)
 
    def test_sacar_valor_invalido(self):
        conta = ContaBancaria('João')
        resultado = conta.sacar(-1)
        self.assertEqual(resultado, 'Valor negativo')
 
    def test_sacar_saldo_insuficiente(self):
        conta = ContaBancaria('João')
        resultado = conta.sacar(2000)
        self.assertEqual(resultado, 'Saldo insuficiente')
 
unittest.main()