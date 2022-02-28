def evilGetLength2(ilist):
    a=[3]
    print(id(ilist))
    length = len(ilist)
    ilist = a # Muhaha: clear the list
    print(id(mylist))
    print("a:" ,id(ilist))
    return length # drawing B here

mylist = [12.8, -14.9, 16.6, -3.0]
print(id(mylist))
l = evilGetLength2(mylist)
print(mylist) # predict the answer
print(l) # predict the answer
