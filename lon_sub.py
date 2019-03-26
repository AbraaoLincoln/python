#Given a string, find the length of the longest substring without repeating characters.
str = "pwwkew"
#str = "abcabcbb"
#str = "bbbbb"
set = set()
m = 0

for i in range(len(str)):
	for j in range(i+1, len(str)):
		aux = str[i:j]
		for x in range(len(aux)):
			set.add(aux[x])
		if(len(aux) == len(set)):
			if(len(aux) > m):
				m = len(aux)
		set.clear()

print(m)