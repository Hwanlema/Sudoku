import tkinter
import random
import threading

class SolveBtn(tkinter.Button):
    def __init__(self):
        super().__init__(tk, text="Solve", command=solve)


class GoBackBtn(tkinter.Button):
    def __init__(self):
        super().__init__(tk, text="Go Back", command=menu)

class SolverBtn(tkinter.Button):
    def __init__(self) -> None:
        super().__init__(tk, text=" Solver  ", command=solver)


class PracticeBtn(tkinter.Button):
    def __init__(self) -> None:
        super().__init__(tk, text="Practice", command=lambda: print("Practice :)"))


class Cell():
        repeated = None
        selected_cell = None
        def __init__(self, x, y):
            self.box = None #index of the box
            self.number_id = None #tk id for the number
            self.rectangle_id = None #tk id for the rectangle representing the cell
            self.text_id = None #tk id for the coords for each box
            self.number = 0
            self.x = x
            self.y = y
        
        def fill(self):
            if self.box%2 == 0:
                return "#e0e0e0"
            else:
                return "white"
        
        def __repr__(self) -> str:
            return f"cell at {self.x},{self.y}"
        
        def select_cell(self, *event):
            if Cell.selected_cell:
                Cell.selected_cell.unselect_cell()
            self.highlight("cyan")
            canvas.focus_set()
            canvas.tag_bind(self.rectangle_id, "<Button-1>", self.unselect_cell)
            if self.number_id:
                canvas.tag_bind(self.number_id, "<Button-1>", self.unselect_cell)
            canvas.bind("<KeyPress>", self.key_press)
            Cell.selected_cell = self
            return self

        def unselect_cell(self, *event):
            if Cell.repeated:
                if self in Cell.repeated:
                    self.highlight()
                else:
                    self.highlight(self.fill())
            else:
                self.highlight(self.fill())
            canvas.tag_bind(self.rectangle_id, "<Button-1>", self.select_cell)
            if self.number_id:
                canvas.tag_bind(self.number_id, "<Button-1>", self.select_cell)
            return self
        
        def highlight(self, colour="red"):
            canvas.itemconfig(self.rectangle_id, fill=colour)

        def set_number(self, number, fill="black"):
            if number != 0:
                canvas.delete(self.number_id)
                self.number_id = canvas.create_text(self.x*box_size-15, self.y*box_size-15, text=number, font=("Ariel", 40), fill=fill)   
                canvas.tag_bind(self.number_id, "<Button-1>", self.select_cell)
                self.number = int(number)
                self.check()
            if number == 0:
                canvas.delete(self.number_id)
                self.number = 0
                self.number_id = None
                self.check()

        def key_press(self, a):
            if a.char.isnumeric() and a.char != "0":
                self.set_number(a.char)
            elif a.keysym == "BackSpace":
                self.set_number(0)

        def check(self):
            repeated_list = set()
            for j in cells:
                if j.number != 0:
                    for i in range(9):
                        if board[j.y-1][i].number == j.number and board[j.y-1][i] is not j:
                            repeated_list.add(board[j.y-1][i])
                            repeated_list.add(j)
                    for i in range(9): 
                        if board[i][j.x-1].number == j.number and board[i][j.x-1] is not j:   
                            repeated_list.add(board[i][j.x-1])
                            repeated_list.add(j)
                    for i in boxes[j.box]:
                        if i.number == j.number and i is not j:
                            repeated_list.add(i)
                            repeated_list.add(j)
            if Cell.repeated:
                for i in Cell.repeated:
                    i.highlight(i.fill())
            if Cell.selected_cell:
                Cell.selected_cell.highlight("cyan")
            if len(repeated_list) != 0:
                for i in repeated_list:
                    i.highlight()
                Cell.repeated = repeated_list
                return False
            else:
                Cell.repeated = None
                return True
                           
def solve():
    for y in range(9):
        for x in range(9):
            if board[y][x].number == 0:
                for n in range(1,10):
                    if board[y][x].check():
                        board[y][x].set_number(n, fill="green")
                        tk.update()
                        solve()
                        board[y][x].set_number(0)
                return
    return


def solver():
    tk.geometry("600x500")
    canvas.place(x=0, y=0, anchor=tkinter.NW)
    gobackbtn.place(x=100, y=470)
    solvebtn.place(x=300, y=470)
    solverbtn.place_forget()
    practicebtn.place_forget()

    for a in range(len(board)):  
        for b in board[a]:
            b.rectangle_id = canvas.create_rectangle(b.x*box_size-40, b.y*box_size-40 ,b.x*box_size+10, b.y*box_size+10, fill="white", outline="black")
            b.text_id = canvas.create_text(b.x*box_size-30, b.y*box_size-32,text=f"{b.x},{b.y}", font=("Arial", 10), fill="black")
            canvas.lower(b.text_id)
            canvas.tag_bind(b.rectangle_id, "<Button-1>", b.select_cell)
            canvas.tag_bind(b.text_id, "<Button-1>", b.select_cell)
    
    for c in range(3):
        for d in range(3):
            canvas.create_rectangle(10+box_size*3*(c+1), 10+box_size*3*(c+1), 10+box_size*3*d, 10+box_size*3*d, width=4, outline="black")
        
    for a in boxes[::2]:
        for b in a:
            b.highlight("#e0e0e0")


def menu():
    for i in cells:
        i.set_number(0)
    tk.geometry("400x400+300+200")
    canvas.place_forget()
    gobackbtn.place_forget()
    solvebtn.place_forget()
    solverbtn.place(x=150, y=100)


board = [[],[],[],[],[],[],[],[],[]]
boxes = [[],[],[],[],[],[],[],[],[]]
cells = []
box_size = 50

for a in range(9):
        "create the board"
        for b in range(9):
            cell = Cell(b+1, a+1)
            board[a].append(cell) #by row
            cells.append(cell) #all cells

for a in range(9): 
    for i in range(3): 
        boxes[a] += board[a//3*3+i][3*(a%3):3*((a%3)+1)] 

for a in boxes:
    for b in a:
        b.box = boxes.index(a)

tk = tkinter.Tk()
tk.title("SUDOKU YAY")
canvas = tkinter.Canvas(tk, width=500, height=510)
solvebtn = SolveBtn()
solverbtn = SolverBtn()
practicebtn = PracticeBtn()
gobackbtn = GoBackBtn()
menu()   
tk.mainloop()

