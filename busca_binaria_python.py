from random import randint
from sortedcontainers import SortedList
lista = []
for i in range(0,100):
  lista.append(randint(0, 1000))
lista_or = SortedList(lista)
print(lista_or)
n = int(input())

def busca(lista_or):
  begin = 0
  last = 0
  half = 49
  if n < lista_or[0] or n > lista_or[len(lista_or)-1]:
    return -1
  while (True):
    if lista_or[half] == n:
      return half
      break
    else:
      if n > lista_or[half]:
        begin = half
        half = (last + begin) // 2
      else:
        last = half
        half = (last + begin) // 2
        
if (busca(lista_or) != -1):
  print(busca(lista_or))
else:
  print("Valor não exite!")