import queue

biscoitos = queue.LifoQueue()
m = "treloso"

def fill_stack(n):
	for i in range(0,n):
		biscoitos.put(m + str(i+1))

def show_stack_pop(qtd):
	r = qtd
	while not biscoitos.empty():
		item_topo = biscoitos.get()
		for i in range(qtd-1,r):
			print("| ", item_topo, " |", end= " ")
		for i in range(qtd):
			print("| ", "        ", " |", end=" ")
			#print('| {message: <{width}} |'.format(message=' ', width=len(m)), end=" ")
			#print("| ", "        ".ljust(len(m)), " |", end=" ")
		print()
		qtd -= 1

def show_stack_push(qtd):
	r = qtd
	while not biscoitos.empty():
		item_topo = biscoitos.get()
		for i in range(qtd):
			print("| ", "        ", " |", end=" ")
		for i in range(qtd-1,r):
			print("| ", item_topo, " |", end= " ")
		print()
		qtd -= 1

size_stack = 6
print("Empilhando os biscoitos...")
fill_stack(size_stack)
show_stack_push(size_stack)
print("\nDesempilhando os biscoitos...")
fill_stack(size_stack)
show_stack_pop(size_stack)
