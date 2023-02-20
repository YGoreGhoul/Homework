a = int(input("Введите ширину прямоугольника. "))
b = int(input("Введите высоту прямоугольника. "))
for i in range(0, b):
    for j in range(1, a):
        print("*", end="")
    print("*")