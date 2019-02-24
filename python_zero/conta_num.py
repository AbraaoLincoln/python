conta = {}
n = int(input())
if(n >= 0 and n <= 30):
    conta[n] = 1

    for i in range(0,9):
        boo = True
        n = int(input())

        if(n >= 0 and n <= 30):
            for j in conta.keys():
                if(n == j):
                    boo = False

            if(boo == True):
                conta[n] = 1
            else:
                conta[n] += 1
        else:
            i -= 1

    print(conta)
