s = '24:00  02/01[/15]  11 [#000000|EYK001/YK001/YK001/YK001/YK001]'

b = s.split("|",1)
listadeeventos = b[1].split("/")
lista = []
print listadeeventos
for i in listadeeventos:
	if len(i) == 5 or i[5] == ']':
		i = 'i' + i
	tr = b[0] + '|' + i.rstrip(']') + ']'
	lista.append(tr)


print lista