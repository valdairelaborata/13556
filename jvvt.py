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
             return "Valor inválido"
        else:
            self.__saldo += valor
 
    def sacar(self, valor):
        if valor <= self.__saldo:
            self.__saldo -= valor
        else:
            print("Saldo insuficiente")
 
class TestContaBancaria(unittest.TestCase):
 
    def test_saldo(self):
        conta = ContaBancaria('João')
        self.assertEqual(self.saldo, 0)
 
    def test_depositar_valor_positivo(self):
        conta = ContaBancaria('João')
        novo_saldo = self.depositar(50)
        self.assertEqual(novo_saldo, 50)
       
    def test_depositar_valo_invalido(self):
        conta = ContaBancaria('João')
        resultado = self.depositar(-10)
        self.assertEqual(resultado, "Valor inválido")
 
    def test_sacar_valor_valido(self):
        conta = ContaBancaria('João')
        novo_saldo = self.sacar(20)
        self.assertEqual(novo_saldo, 30)
 
    def test_sacar_valor_invalido(self):
        conta = ContaBancaria('João')
        self.sacar(-1)
 
    def test_sacar_saldo_insuficiente(self):
        conta = ContaBancaria('João')
        self.sacar(2000)
