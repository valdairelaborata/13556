

def pai(funcao):
    def wrapper():
        print('Compra uma cerveja também')
        funcao()
        print('Coloca a cerveja na geladeria')

    return wrapper


@pai
def comprar_pao():
    print('Comprou o pão')


comprar_pao()