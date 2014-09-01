#En este archivo se encuentran los ejemplos de como trabajar con listas,tuplas y diccionarios



#LISTAS

#las listas en python son equivalentes a los arreglos o vectores
#las posiciones en python comienzan desde 0

#ejemplo de una lista 

lista=[22,True,["gustavo","ariel","martinez"],'c',34,34,34,12,67]

#podemos obtener el elemento en una posicion de la lista indicando entre corchetes la posicion

Elem=lista[1]
print Elem

#para obtener un elemento de una lista q se encuentra dentro de otra lista debemos indicarlo de la siguiente manera:
#el primer corchete indica la posicion de la lista q se encuentra mas afuera y el segundo corchete hace referencia a la posicion
#de la lista que se encuentra mas adentro
Elem=lista[2][0]
print Elem


#ahora vamos a modificar un elemento de lista
lista[1]=False
Elem=lista[1]
print Elem

#el operador [] es muy potente me permite definir desde que numero comienza el inicio por ej podria decir q el primer
#elemento esta en la posicion -1 indicando [-1] y no ded 0 [0]

#en el sgte ejemplo defino con que parte de la lista me quiero quedar
#con esto puedo definir desde que posicion hasta antes de q posicion quiero
Elem=lista[1:3]
print Elem

#al definir que quiero los elementos de la posicion en funcion de [x:y:z] le digo devolve los elementos entre las posiciones
# "x" y "z" pero no quiero el elemento de la posicion "z" 
Elem=lista[0:3:2]
print Elem

#sino coloco el fin python me toma por defecto el fin de la lista 
#para el inicio sucede lo mismo
Elem=lista[2:]
print Elem

#con este mecanismo tambien podemos cambiar valores

lista[0:4]=[False]
print lista


#TUPLAS 

#para definir una tupla se realiza de la siguiente manera

tupla=(1,"gustavo",('a','b'))

#para trabajar con las tuplas se realiza de la misma manera q con las listas,tienen la misma sintaxis
print tupla[0]
print tupla[2][0]
print tupla[1:]
print tupla[:2]


#DICCIONARIOS





