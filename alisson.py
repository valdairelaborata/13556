def meu_microndas(funcao):
    def wrapper():
        print("Beep!")
        funcao()
        print("Beep!, Beep!, Beep!")
       
       
    return wrapper
 
@meu_microndas
def minha_funcao():
    print("Me aperta!")
       
minha_funcao()