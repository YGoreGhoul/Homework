class BinaryTree:

    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data

# Insert для создания узлов
    def insert(self, data):

        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = BinaryTree(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = BinaryTree(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data
# findval для сравнения значения с узлами
    def findval(self, lkpval):
        if lkpval < self.data:
            if self.left is None:
                return "Значение "+ str(lkpval)+" не найдено"
            return self.left.findval(lkpval)
        elif lkpval > self.data:
            if self.right is None:
                return "Значение "+ str(lkpval)+" не найдено"
            return self.right.findval(lkpval)
        else:
            print('Значение ' + str(self.data) + ' найдено')

# Рисуем дерево
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print(self.data),
        if self.right:
            self.right.PrintTree()

root = BinaryTree(15)
root.insert(7)
root.insert(16)
root.insert(2)
print(root.findval(int(input())))
print(root.findval(int(input())))