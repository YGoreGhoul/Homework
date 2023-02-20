a = int(input('Введите длину первой стороны прямоугольника: '))
b = int(input('Введите длину второй стороны прямоугольника: '))
for i in range(1, b+1):
    print()
    for j in range(i, a*b+1, b):
        print(j, end=' ')
