#esto es una cadena
s="Hola Mundo"
print s

#esto es un entero
i=23
print i

#la funcion "type" me determina el tipo de una variable
#me funciona esta funcion cuando lo hago por consola haciendo desde un archivo .py y ejecutandolo no me la reconoce
type(s)


#octal
#el numero octal 027 es el 23 en represaentacion entera
o=027
print o

#hexadecimal
#el valor de h es el 23 en base 10

h=0x17
print h

#numero real
r=1.25
print r

#operadores aritmeticos

print "suma es "
print i+r
print "resta es "
print i-r
print "producto es "
print i*r
#division comun
print "division es "
print i/r
#division entera
print "division entera es "
print i//r
print "modulo es "
print i%r

#cadenas
#con la triple cadena puedo definir una cadena en mas de un renglon
triple="""hola soy
		  gustavo martinez"""
print triple		  

#operaciones con cadenas 
a="gustavo"
b="martinez"
#concatenacion
c=a+b
print c
#repeticion 
c=a*3
print c


#booleanos
a=True
b=False
#conjuncion
c=a and b
print c
#disjuncion
c=a or b
print c
#negacion
c= not b
print c

d=2
e=3
#igualdad
f=e==d
print f
#distinto
f=e!=d
print f
#mayor
f=e>d
print f
#mayor igual
f=e>=d
print f


