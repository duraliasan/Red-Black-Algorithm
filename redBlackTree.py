import tkinter as tk
from tkinter import messagebox


class Node:
    def __init__(self, data, color='Red'):
        self.data = data
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(0)
        self.TNULL.color = 'Black'
        self.root = self.TNULL

    def insert(self, key):
        node = Node(key)
        node.left = self.TNULL
        node.right = self.TNULL
        node.parent = None

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 'Black'
            return

        if node.parent.parent == None:
            return

        self.fix_insert(node)

    def fix_insert(self, k):
        while k.parent.color == 'Red':
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 'Red':
                    u.color = 'Black'
                    k.parent.color = 'Black'
                    k.parent.parent.color = 'Red'
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 'Black'
                    k.parent.parent.color = 'Red'
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == 'Red':
                    u.color = 'Black'
                    k.parent.color = 'Black'
                    k.parent.parent.color = 'Red'
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 'Black'
                    k.parent.parent.color = 'Red'
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 'Black'

    def delete_node(self, data):
        self.delete_node_helper(self.root, data)

    def delete_node_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.data == key:
                z = node

            if node.data <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            print("Node not found.")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == 'Black':
            self.fix_delete(x)

    def fix_delete(self, x):
        while x != self.root and x.color == 'Black':
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 'Red':
                    s.color = 'Black'
                    x.parent.color = 'Red'
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 'Black' and s.right.color == 'Black':
                    s.color = 'Red'
                    x = x.parent
                else:
                    if s.right.color == 'Black':
                        s.left.color = 'Black'
                        s.color = 'Red'
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 'Black'
                    s.right.color = 'Black'
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 'Red':
                    s.color = 'Black'
                    x.parent.color = 'Red'
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.color == 'Black' and s.right.color == 'Black':
                    s.color = 'Red'
                    x = x.parent
                else:
                    if s.left.color == 'Black':
                        s.right.color = 'Black'
                        s.color = 'Red'
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 'Black'
                    s.left.color = 'Black'
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 'Black'

    def rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def print_tree(self):
        self.print_helper(self.root, "", True)

    def print_helper(self, node, indent, last):
        if node != self.TNULL:
            print(indent, end=' ')
            if last:
                print("R----", end=' ')
                indent += "     "
            else:
                print("L----", end=' ')
                indent += "|    "

            s_color = "RED" if node.color == 'Red' else "BLACK"
            print(f'{node.data} ({s_color})')
            self.print_helper(node.left, indent, False)
            self.print_helper(node.right, indent, True)

    def draw_tree(self, canvas, x, y, node, dx=60, dy=50):
        if node != self.TNULL:
            # Draw lines to children
            if node.left and node.left != self.TNULL:
                canvas.create_line(x, y, x - dx, y + dy)
            if node.right and node.right != self.TNULL:
                canvas.create_line(x, y, x + dx, y + dy)

            # Draw node
            fill_color = "red" if node.color == 'Red' else "black"
            canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=fill_color)
            canvas.create_text(x, y, text=str(node.data), fill="white")

            # Draw subtrees
            if node.left:
                self.draw_tree(canvas, x - dx, y + dy, node.left, dx // 2, dy)
            if node.right:
                self.draw_tree(canvas, x + dx, y + dy, node.right, dx // 2, dy)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Red-Black Tree")
        self.geometry("800x600")
        self.tree = RedBlackTree()

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(self)
        self.entry.pack(side=tk.LEFT)

        self.insert_button = tk.Button(self, text="Insert", command=self.insert_value)
        self.insert_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(self, text="Delete", command=self.delete_value)
        self.delete_button.pack(side=tk.LEFT)

        self.refresh_button = tk.Button(self, text="Refresh", command=self.refresh)
        self.refresh_button.pack(side=tk.LEFT)

    def insert_value(self):
        try:
            value = int(self.entry.get())
            self.tree.insert(value)
            self.refresh()
        except ValueError:
            messagebox.showerror("Input Error", "Invalid input. Please enter an integer.")

    def delete_value(self):
        try:
            value = int(self.entry.get())
            self.tree.delete_node(value)
            self.refresh()
        except ValueError:
            messagebox.showerror("Input Error", "Invalid input. Please enter an integer.")

    def refresh(self):
        self.canvas.delete("all")
        self.tree.draw_tree(self.canvas, 400, 50, self.tree.root)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
