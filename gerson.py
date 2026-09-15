import unittest
 
class ContaBancaria:
    def __init__(self, saldo_inicial=0):
        self.saldo = saldo_inicial
       
    def depositar(self, valor):
        self.saldo += valor
       
    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
            return True
        return False
   
    def verificar_saldo(self):
        return self.saldo
   
class TesteContaBancaria(unittest.TestCase):
    def test_deposito(self):
        conta = ContaBancaria()
        conta.depositar(100)
       
        self.assertEqual(conta.verificar_saldo(), 100)
       
    def test_saque(self):
        conta = ContaBancaria(100)
        resultado = conta.sacar(40)
       
        self.assertTrue(resultado)
        self.assertEqual(conta.verificar_saldo(), 60)
       
    def test_saque_sem_saldo_suficiente(self):
        conta = ContaBancaria(50)
        resultado = conta.sacar(100)
       
        self.assertFalse(resultado)
        self.assertEqual(conta.verificar_saldo(), 50)
       
    def test_verificar_saldo(self):
        conta = ContaBancaria(200)
       
        self.assertEqual(conta.verificar_saldo(), 200)
       
unittest.main()
