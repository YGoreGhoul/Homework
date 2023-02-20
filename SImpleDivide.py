x = int(input('Введите число: '))
for i in range(2, x+1):
    if x % i == 0:
        for y in range(2, i):
            if i % y == 0:
                break
        else:
            print(i)