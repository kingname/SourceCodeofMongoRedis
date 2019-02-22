import redis

c = redis.Redis()
c.delete('text')
for i in range(256):
    binary = bin(i)[2:][:: -1]
    index_list = []
    for index, x in enumerate(binary):
        c.setbit('text', 7 - index, int(x))
        if x == '1':
            index_list.append(7 - index)
    y = c.getrange('text', 0, -1)
    print(f'{str(index_list).ljust(30)},  # {i} => {y} => {("0000000" + binary[::-1])[-8:]}')
    # print(f'{i}=>{("0000000" + binary[::-1])[-8:]}=>{y}')