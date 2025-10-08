```python
try:
    n1 = float(input("Ingresa el primer número:"))
    n2 = float(input("Ingresa el segundo número:"))
    opcion = int(input("1)Suma  2)resta  3)multiplicación  4)división"))


    if opcion == 1:
        print(suma(n1,n2))
    elif opcion == 2:
        print(resta(n1,n2))
    elif opcion == 3:
        print(multi(n1,n2))
    elif opcion == 4:
        print(div(n1,n2))
    else:
        print("opción inválida")
    
except ValueError:
    print("Debes de ingresar números, repite el proceso")

def suma(n1 , n2):
    return n1+n2

def multi(n1 , n2):
    return n1*n2

def resta(n1 , n2):
    return n1-n2

def div(n1,n2): 
    if n2==0: 
        print("No se puede dividir entre cero")
    else :
        return(n1/n2)
```


```python

```


```python

```
