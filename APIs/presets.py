from APIs.teclado import *
from pynput.keyboard import Key


def retirarDiferenciado():
    anoInicio = int(input("Digite o ano de inicio:"))
    mesInicio = int(input("Digite o mes de inicio:"))
    anofinal = int(input("Digite o ano final:"))
    mesfinal = int(input("Digite o mes final:"))
    reg = int(input("Digite o registro:"))


    for i in range(3):
        print(i+1)
        sleep(1)


    mes = mesInicio
    for ano in range(anoInicio, anofinal+1):
        tempoTecla = 0.01
        tempoEnter = 1
    
        while mes <= mesfinal:
            stringPress(str(reg), tempoTecla)
            
            keyPress(Key.enter)
            sleep(tempoEnter+0.01)
            
            if(mes < 10):
                stringPress('0',tempoTecla)
            stringPress(str(mes), tempoTecla)
            stringPress(str(ano), tempoTecla)
            keyPress(Key.enter)
            sleep(tempoEnter+0.01)

            keyPress(Key.f9)
            sleep(tempoEnter)
            keyPress(Key.enter)
            sleep(tempoEnter)
            keyPress('s')
            sleep(tempoEnter)
            mes += 1
        mes = 1


