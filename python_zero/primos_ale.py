from random import randint
import math

primos = set()
i = 5
while(i > 0):
    primo = True
    n = randint(2,100)
    for j in range(2, 1+(int(math.sqrt(n)))):
      if(n % j == 0):
        primo = False
    for p in primos:
        if(p == n):
            primo = False
    if(primo == True):
      primos.add(n)
      i -= 1
print(primos)
