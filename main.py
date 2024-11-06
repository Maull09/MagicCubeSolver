import random
import threading
import tkinter as tk
import tkintertools as tkt
from tkintertools import tools_3d as t3d
from cube.cube import MagicCube  # Assuming you have MagicCube implemented with number-based display
import typing
from gui import ui

__VERSION__ = "1.2"
__AUTHOR__ = "Adapted from Xiaokang2022"

STOP_SEARCH = False
SEARCH_ALGO = 4  # Default to Hill Climbing (HC) for local search

# Custom Space class for 3D sorting
class Space(t3d.Space):
    """Custom Space class for 3D sorting with enhanced depth management"""

    @typing.override
    def space_sort(self) -> None:
        self._items_3d.sort(
            key=lambda item: item._camera_distance(), reverse=True)
        for item in self._items_3d:
            self.lift(item.item)

# Tkinter setup
root = tkt.Tk(f"5x5x5 Magic Cube v{__VERSION__}", 1600, 1000)
root.resizable(False, False)
bg = tkt.PhotoImage("background.png")

# 3D Space setup
space = Space(root, 1000, 1000, 0, 0, bg="black")
space.pack(fill="both", expand=True)
bg1 = space.create_image(0, 0, image=bg, anchor="nw")

mc = MagicCube(space, size=5)  # Initialize Magic Cube with number-based display

# Display progress in the objective function as local search runs
def display_objective_progress():
    """Displays the objective function value as local search progresses."""
    while not STOP_SEARCH:
        current_value = mc.objective_function()
        # t_count.set(f'Objective: {current_value}')
        if current_value == 0:  # Check for solution
            STOP_SEARCH = True
            break
        root.update()

# Local Search with Iterative Swaps
def local_search():
    """Executes a local search to reduce the cube's objective function value."""
    global STOP_SEARCH
    STOP_SEARCH = False
    threading.Thread(target=display_objective_progress, daemon=True).start()
    while not STOP_SEARCH:
        pos1 = (random.randint(0, 4), random.randint(0, 4), random.randint(0, 4))
        pos2 = (random.randint(0, 4), random.randint(0, 4), random.randint(0, 4))
        mc.swap_blocks(pos1, pos2)
        if mc.objective_function() > mc.objective_function():
            mc.swap_blocks(pos1, pos2)  # Revert if no improvement
        space.space_sort()
        root.update()

def stop_local_search():
    """Stops the local search."""
    global STOP_SEARCH
    STOP_SEARCH = True

def create_title(canvas: tkt.Canvas, x: int, y: int, text: str) -> None:
    """create a virtual title on Canvas"""
    canvas.create_rectangle(x, y, x+10, y+40, fill='orange', outline='')
    canvas.create_text(x+20, y+20, text=text, fill='white',
                       anchor='w', font=(tkt.FONT, -36))
    
config = tkt.Canvas(root, 600, 1000, 1000, 0, bg='#1F1F1F')
bg2 = config.create_image(-1000, 0, image=bg, anchor="nw")
config.create_line(0, 10, 0, 990, fill='grey')
config.create_text(300, 990, anchor="s", fill='grey', justify="center", font=(
    tkt.FONT, -20), text=f"Author: {__AUTHOR__}\nFramework: tkintertools v2.6.21.1")

create_title(config, 20, 20, "Magic Cube Solver")

# Select search algorithm for local search
def select_search_algo(value: int):
    global SEARCH_ALGO
    SEARCH_ALGO = value

def switch_search_algo(id: int) -> None:
    """switch algorithm of searching"""
    global SEARCH_ALGO
    choose_fill = ui.navbutton["color_fill"][:]
    choose_fill[0] = "cornflowerblue"
    choose_outline = ui.navbutton["color_outline"][:]
    choose_outline[0] = "cornflowerblue"
    for btn in (buttons := [nb0, nb1, nb2, nb3, nb4, nb5]):
        btn.configure(
            color_fill=ui.navbutton["color_fill"], color_outline=ui.navbutton["color_outline"])
        btn.state()
    buttons[id].configure(color_fill=choose_fill, color_outline=choose_outline)
    buttons[id].state()
    SEARCH_ALGO = id

# Switch search algorithm for local search
config.create_text(20, 540, text='选择算法', anchor="w", fill='white')
nb0 = tkt.Button(config, 130, 520, 70, 40, text='BFS',
                 command=lambda: switch_search_algo(0), **ui.navbutton)
nb1 = tkt.Button(config, 205, 520, 70, 40, text='DFS',
                 command=lambda: switch_search_algo(1),  **ui.navbutton)
nb2 = tkt.Button(config, 280, 520, 70, 40, text='UCS',
                 command=lambda: switch_search_algo(2),  **ui.navbutton)
nb3 = tkt.Button(config, 355, 520, 70, 40, text='A/A*',
                 command=lambda: switch_search_algo(3),  **ui.navbutton)
nb4 = tkt.Button(config, 430, 520, 70, 40, text='HC',
                 command=lambda: switch_search_algo(4),  **ui.navbutton)
nb5 = tkt.Button(config, 505, 520, 70, 40, text='REV',
                 command=lambda: switch_search_algo(5),  **ui.navbutton)
switch_search_algo(SEARCH_ALGO)

class SearchTree(tkt.Toplevel):
    """display a tree when searching"""

    def __init__(self) -> None:
        x, y = root.winfo_x(), root.winfo_y()
        tkt.Toplevel.__init__(
            self, root, 'Search Tree', 600, 670, x+1000, y, bg="#1F1F1F", shutdown=self.close)
        self.resizable(False, False)
        self.transient(root)
        self.cv = tkt.Canvas(self, 600, 670, 0, 0, bg="#1F1F1F")
        self.num = len(mc.steps) + 1
        if self.num <= 1 or self.num >= 10:
            self.num = 10
        self.lines: list[list[int]] = [[] for _ in range(self.num)]
        self.build()

    def close(self) -> None:
        """"""
        search = config.itemcget(t_count, "text")
        steps = config.itemcget(t_steps, "text")
        if steps != "0" or search == "1" or STOP_SEARCH:
            self.destroy()

    def build(self) -> None:
        """build UI"""
        self.cv.create_image(
            -1000, 0, image=bg if switch_bg.get() else None, anchor="nw")
        self.cv.create_line(50, 20, 50, 650, fill='grey')
        self.cv.create_line(550, 20, 550, 650, fill='grey')
        self.key = self.cv.create_line(-5, 20, -5, 650, fill='#0FF')

        for depth in range(self.num):
            Y = 65 + (600 // self.num)*depth
            color = tkt.color(("#00FF00", "#FF0000"), depth / (self.num - 1))
            self.cv.create_text(25, Y, text=f"{depth+1:02}", fill=color)
            self.cv.create_text(
                585, Y, anchor="e", text=f"{definition.BASE_NUM}", fill=color)
            self.cv.create_text(
                595, Y-10, anchor="e", text=f"{depth}", fill=color, font=(tkt.FONT, -16))

            if depth == 0:
                total = definition.BASE_NUM
                delta = 480/total
            elif depth == 1:
                total = definition.BASE_NUM**2
                delta = 480/total
            else:
                total = 480
                delta = 1

            self.lines[depth] = [
                self.cv.create_line(
                    60+delta*i, Y, 60+delta*(i+1), Y, fill="#444", width=15)
                for i in range(total)
            ]

    def light(self, trace: list[definition.OP], index: int = 0, *, highlight: str = None) -> None:
        """light a point"""
        depth = len(trace) - 1
        if depth >= self.num:
            return
        for op in trace:
            index *= definition.BASE_NUM
            index += definition.OPS[::-1].index(op)
        if depth >= 2:
            index = int(index/definition.BASE_NUM**(depth+1)*480)
        color = tkt.color(("#AAAA00", "#CC00CC"), depth / (self.num - 1))
        self.cv.itemconfigure(
            self.lines[depth][index], fill=color if highlight is None else highlight)
        if highlight is not None:
            if depth == 0:
                index *= 480/definition.BASE_NUM
            elif depth == 1:
                index *= 480/definition.BASE_NUM**2
            self.cv.coords(self.key, 60+index, 20, 60+index, 650)

def clear_data() -> None:
    """clear up the data of searching"""
    config.itemconfigure(t_count, text="0")
    config.itemconfigure(t_steps, text="0")
    pb.load(0)

def start_search() -> None:
    """start searching the recover method"""

    def func() -> None:
        global STOP_SEARCH
        STOP_SEARCH = False
        evaluate.exponent = len(mc.steps)
        match SEARCH_ALGO:
            case 0: trace = search.BFS(array.array('b', mc.data), counter, tl)
            case 1: trace = search.DFS(array.array('b', mc.data), counter, tl, depth=int(depth.get()) if depth.get().isdigit() else len(mc.steps))
            case 2: trace = search.UCS(array.array('b', mc.data), counter, tl)
            case 3: trace = search.AS(array.array('b', mc.data), counter, tl)
            case 4: trace = search.HC(array.array('b', mc.data), counter, tl)
            case _: trace = [(op, not rev) for op, rev in reversed(mc.steps)]
        if trace is None:
            return
        config.itemconfigure(t_steps, text=f'{len(trace)}')
        if tl:
            for i in range(len(trace)):
                tl(trace[:i+1], highlight="#0FF")
        recover(mc, trace, animate=ani.get())

    clear_data()
    tl = SearchTree().light if tree.get() and SEARCH_ALGO != 5 else None
    threading.Thread(target=func, daemon=True).start()

# Start and Stop buttons for local search
tkt.Button(config, 380, 790, 200, 40, text='Start Local Search', command=local_search, **ui.button)
tkt.Button(config, 380, 840, 200, 40, text='Stop Local Search', command=stop_local_search, **ui.button)

# Run Tkinter main loop
root.mainloop()
