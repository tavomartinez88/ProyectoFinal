#ESTRUCTURAS DE CONTROL
number=123


#estructura de un if
if number==123:
	print "el numero es igual a 123"


#estructura del if-else
if number!=123:
	print "no es un numero"
else: print "es un numero"

#if-elif-else
if number>0:
	print "el numero es positivo"
elif number<0:
	print "el numero es negativo"
else:
	print "el numero es neutro"		

#otra forma de realizar un if-else

state="positivo" if (number>0) else "negativo"
print state	

#BUCLES

#while
edad=0
while edad<21:
	edad=edad+1
	print "felicitaciones tienes:"+str(edad)


#la funcion raw_input() lee lo ingresado por pantalla
salir=False	
while not salir:
	entrada=raw_input()
	if entrada=="adios":
		salir=True
	else: 
		print entrada

#for
ident=["gustavo","ariel","martinez"]
for x in ident:
	print x

#la funcion xrangue me permite imprimir los n-1 numeros comenzando desde 1
for x in xrange(1,25):
 print x

 #FUNCIONES

 #ejemplo de una funcion 
 def agregar(x,y):
 	x = x+3
 	y.append(x)
 	print x,y
 x=25
 y=[27]
agregar(x,y)
print x,y


#ejemplo de una funcion que retorna la suma de dos valores
def sumar(p,q):
     return p+q

print sumar(number,number)


#ejemplo de una funcion que retorna una tupla
def returnTupla(x,q):
     	return x+2 , q*3

print returnTupla(number,number)