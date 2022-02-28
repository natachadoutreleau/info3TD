def add_two_thousands(Number) :
    print("adresse number : ",id(Number))
    c=2000
    print("adresse c : ", id(c))
    return c+Number

a= 208
b= 210
print(id(a), id(b))
add_two_thousands(a)
