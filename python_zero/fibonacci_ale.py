from random import randint

fibonacci = set()

def seq_fib(n):
  if( n <= 2):
    return 1
  else:
    return seq_fib(n-1) + seq_fib(n-2)

for i in range(0,5):
  n = randint(2,100)
  n1 = 0
  f = True
  next_fib = 1
  while(f == True):
    if (n > seq_fib(next_fib)):
      next_fib += 1
    else:
      f = False
      n1 = seq_fib(next_fib)
  if(n == n1):
    fibonacci.add(n)
print(fibonacci)
