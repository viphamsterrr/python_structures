import structs


stck = structs.Stack.create(int)
stck.put(5)
stck.put(4)
stck.put(88)
print(stck.get_size())
for i in stck:
    print(i)

