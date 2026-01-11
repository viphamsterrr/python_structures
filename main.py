import structs


que = structs.Queue.create(int)
for i in range(2000):
    que.put(i)
print(que.get_size())

for i in range(1400):
    print(que.take())
print(que.get_size())
print(1 in que)
