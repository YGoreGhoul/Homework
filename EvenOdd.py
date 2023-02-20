from itertools import zip_longest
even=[]
odd=[]
while True:
    n=int(input("Введите число: "))
    if n==0:
        break
    if n%2==0:
        even.append(n)
    else:
        odd.append(n)
print(*zip_longest(even, odd, fillvalue=' '), sep='\n')