from tkinter import *
import itertools
import sys

class DefragWindow:
    def __init__(self, canvas:Canvas, disk:str):
        self.canvas = canvas
        self.blocks = []
        self.disk = self.layout(disk)
        self.move = 0
        self.front = 0
        self.back = len(self.disk) - 1

        # self.canvas.bind("<Button-1>", self.canvas_onclick)
        # self.text_id = self.canvas.create_text(300, 200, anchor='se')
        # self.canvas.itemconfig(self.text_id, text='hello')

    def layout(self, disk:str):
        layout = []
        for idx, pair in enumerate(itertools.batched(disk, n=2)):
            for _ in range(int(pair[0])):
                layout.append(idx)
            if len(pair) == 2:
                for _ in range(int(pair[1])):
                    layout.append('.')

        x, y, w, h = (1, 1, 10, 10)
        for c in layout:
            color = 'white' if c == '.' else 'green'
            block = self.canvas.create_rectangle(x, y, x+w, y+h, outline="black", fill=color)
            self.blocks.append(block)
            x += w
            if x+w >= self.canvas.winfo_reqwidth():
                x = 1
                y += h
        return layout

    def defrag(self):
        while self.front < self.back:
            if self.disk[self.back] == '.':
                self.back -= 1
                continue
            if self.disk[self.front] != '.':
                self.front += 1
                continue
            self.disk[self.front] = self.disk[self.back]
            self.disk[self.back] = '.'
            break
        return self.front, self.back

    def draw(self):
        old_front = self.front
        front, back = self.defrag()
        # self.canvas.itemconfig(self.blocks[old_front], fill='green')
        self.canvas.itemconfig(self.blocks[front], fill='blue')
        self.canvas.itemconfig(self.blocks[back], fill='white')
        self.canvas.after(1, self.draw)

def main():
    if len(sys.argv) < 2:
        print("missing file arg")
        return -1

    fname = sys.argv[1]

    root = Tk()
    root.title = "Disk Defragmentor"
    root.resizable(0,0)
    root.wm_attributes("-topmost", 1)

    canvas = Canvas(root, width=1280, height=768, bd=0, highlightthickness=0, relief=GROOVE, borderwidth=2)
    canvas.pack()

    with open(fname) as fd:
        lines = fd.read()
        defrag = DefragWindow(canvas, lines)
        defrag.draw()
        root.mainloop()
    return 0

if __name__ == "__main__":
    sys.exit(main())