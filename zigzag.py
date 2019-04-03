#s = input()
#rows = input()
s = "PAYPALISHIRING" 
rows = 4
btw = rows - 2
matrix = []

def fillbetween(matrix, sizeoflist, pst, item):
    l = []

    for i in range(sizeoflist):
    	l.append(" ")
    #print(l)
    for i in range(sizeoflist):
        if i == pst:
            l[i] = item
        else:
            l[i] = " "
    #print(l)
    matrix.append(l)
 
i = 0
x = rows
l = []

for j in range(rows):
		l.append(" ")

while i < len(s):
	y = 0
	if i+rows < len(s):
		for j in range(i, x):
			l[y] = s[j]
			y += 1
		#print(l)
		i += rows
		matrix.append(l.copy())
		#print(matrix)
		for j in range(btw):
			fillbetween(matrix, rows, (btw-j), s[i])
			i += 1
		x = i + rows
		#print(matrix) 
	else:
		for j in range(i, len(s)):
			l[y] = s[j]
			y += 1
			i += 1
		while y < rows:
			l[y] = " "
			y += 1
		matrix.append(l.copy())


#print(matrix)
for j in range(rows):
	for z in range(len(matrix)):
		print(matrix[z][j], end="")
	print("")

zigzag = []

for j in range(rows):
	for z in range(len(matrix)):
		if matrix[z][j] != " ":
			zigzag.append(matrix[z][j])
print(zigzag)
