from random import randint
conta = {}
n = randint(0,30)
conta[n] = 1

for i in range(0,9):
    boo = True
    n = randint(0,30)
    for j in conta.keys():
        if(n == j):
            boo = False

    if(boo == True):
        conta[n] = 1
    else:
        conta[n] += 1

print(conta)
