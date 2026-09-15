# 1 - Crie uma classe ContaBancaria que permita depósitos, saques e verificação de saldo. Escreva testes para os métodos dessa classe.


import unittest


class ContaBancaria:
    def __init__(self, titular: str):
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
        else:
            return 'Saldo insuficiente'
      

class Teste_ContaBancaria(unittest.TestCase):

    def test_depositar(self):
        conta = ContaBancaria("João")
        conta.depositar(50)
        self.assertEqual(conta.saldo, 50)

    def test_sacar(self):
        conta = ContaBancaria("João")
        conta.depositar(100)
        conta.sacar(50)        
        self.assertEqual(conta.saldo, 50)

    def test_sacar_valor_insuficiente(self):
        conta = ContaBancaria("João")
        conta.depositar(100)
        resultado = conta.sacar(150)
        self.assertEqual(resultado, 'Saldo insuficiente')
        self.assertEqual(conta.saldo, 100) 

unittest.main()



    # def test_saldo_inicial(self):
    #     conta = ContaBancaria("João")
    #     self.assertEqual(conta.saldo, 0)

    # def test_depositar_valor_positivo(self):
    #     conta = ContaBancaria("João")
    #     conta.depositar(100)
    #     self.assertEqual(conta.saldo, 100)

    # def test_depositar_valor_invalido(self):
    #     conta = ContaBancaria("João")
    #     resultado = conta.depositar(-50)
    #     self.assertEqual(resultado, 'Valor invalido')

    # def test_sacar_valor_valido(self):
    #     conta = ContaBancaria("João")
    #     conta.depositar(100)
    #     conta.sacar(50)
    #     self.assertEqual(conta.saldo, 50)

    # def test_sacar_valor_invalido(self):
    #     conta = ContaBancaria("João")
    #     resultado = conta.sacar(-10)
    #     self.assertEqual(resultado, 'Saldo insuficiente')

    # def test_sacar_saldo_insuficiente(self):
    #     conta = ContaBancaria("João")
    #     resultado = conta.sacar(2000)
    #     self.assertEqual(resultado, 'Saldo insuficiente para saque')