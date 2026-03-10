from math import ceil
from tkinter import *
import time
from tkinter import messagebox

from game.models import Coords
from game.collision import (
    collided_bottom,
    collided_left,
    collided_right,
    collided_top,
)

class Game:
    def __init__(self, title, size, image):
        self.tk = Tk()
        self.tk.title(title)
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.width = size
        self.height = size
        self.canvas = Canvas(self.tk, width=self.width, height=self.height, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.bg = PhotoImage(file=image)
        self.sprites = []
        self.running = True

        w = self.bg.width()
        h = self.bg.height()
        len_w = ceil(self.canvas.winfo_width() / w)
        len_h = ceil(self.canvas.winfo_height() / h)

        for x in range(0, len_w):
            for y in range(0, len_h):
                self.canvas.create_image(x * w, y * h, image=self.bg, anchor='nw')

        print("{}x{} images needed / game start ...".format(len_w, len_h))

    def mainloop(self):
        while self.running:
            for sprite in self.sprites:
                sprite.move()
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)

    def add_sprite(self, sprite:Sprite):
        if sprite.type == "HP": self.hp = sprite
        self.sprites.append(sprite)

class Sprite:
    def __init__(self, game, type=None):
        self.game = game
        self.type = type
        self.coordinateds = None
    def move(self):
        pass
    def coords(self):
        return self.coordinateds

class Bar(Sprite):
    def __init__(self, game, image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = PhotoImage(file=image)
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
        self.coordinateds = Coords(x, y, x + width, y + height)

class Item(Sprite):
    def __init__(self, game, image, x, y, width, height):
        Sprite.__init__(self, game, "item")
        self.photo_image = PhotoImage(file=image)
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
        self.coordinateds = Coords(x, y, x + width, y + height)

class HelthBar(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game, "HP")
        self.image = PhotoImage(file="assets/helth.png")
        self.image0 = PhotoImage(file="assets/helth0.png")
        self.game.canvas.create_text(10, 5, text="HP", anchor='nw', fill='red', font=('Arial', 12, 'bold'))
        self.reset()

    def move(self):
        if time.time() - self.last_time > 2:
            if(self.hp == 0):
                if messagebox.askyesno("확인", "HP가 0이 되었습니다.다시 시작하시겠습니까?"):
                    self.reset()
                else:
                    self.game.running = False
                return

            self.last_time = time.time()
            self.hp -= 1

            w = self.image0.width()
            for x in range(0, 10 - self.hp):
                self.game.canvas.create_image(40 + x * w, 10, image=self.image0, anchor='nw')

    def reset(self):
        self.game.canvas.create_image(40, 10, image=self.image, anchor='nw')
        self.last_time = time.time()
        self.hp = 10

class StickFigureSprite(Sprite):
    def __init__(self, game, figure_name=0):
        Sprite.__init__(self, game)
        self.x = -2
        self.y = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinateds = Coords()
        self.figure_name = figure_name
        self.figure_names = [ "basic", "공룡", "mon" ]
        self.load_images()
        self.size = self.images["left"][0].height()
        self.image = self.game.canvas.create_image(0, self.size, image=self.images["left"][self.current_image], anchor='nw')

        self.game.canvas.bind_all('<KeyPress-Escape>', self.escape)
        self.game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.game.canvas.bind_all('<space>', self.jump)

    def load_images(self):
        self.images = {
            "left": [ PhotoImage(file="assets/figure/{}/L{}.png".format(self.figure_names[self.figure_name], i)) for i in range(1, 4) ],
            "right": [ PhotoImage(file="assets/figure/{}/R{}.png".format(self.figure_names[self.figure_name], i)) for i in range(1, 4) ]
        }

    def escape(self, evt):
        if messagebox.askyesno("확인", "종료하시겠습니까?"):
            self.game.running = False
    def turn_left(self, evt):
        if self.y == 0:
            self.x = -2
    def turn_right(self, evt):
        if self.y == 0:
            self.x = 2
    def jump(self, evt):
        if self.x != 0:
            self.figure_name = self.figure_name+1 if self.figure_name+1 < len(self.figure_names) else 0
            self.load_images()

        if self.y == 0:
            self.y = -4
            self.jump_count = 0

    def animate(self):
        if self.x != 0:
            if self.y == 0:
                if time.time() - self.last_time > 0.1:
                    self.last_time = time.time()
                    self.current_image += self.current_image_add
                if self.current_image >= 2: 
                    self.current_image_add = -1
                if self.current_image <= 0: 
                    self.current_image_add = 1

            count = self.current_image if self.y == 0 else 2
            way = "left" if self.x < 0 else "right"
            self.game.canvas.itemconfig(self.image, image=self.images[way][count])

    def coords(self):
        xy = self.game.canvas.coords(self.image)
        self.coordinateds.x1 = xy[0]
        self.coordinateds.y1 = xy[1]
        self.coordinateds.x2 = xy[0] + self.size
        self.coordinateds.y2 = xy[1] + self.size
        return self.coordinateds
    
    def move(self):
        self.animate()

        if self.y < 0:
            self.jump_count += 1
            if self.jump_count > self.size:
                self.y = 4

        if self.y > 0:
            self.jump_count -= 1

        co = self.coords()
        left = True
        right = True
        top = True
        bottom = True
        falling = True

        if self.y > 0 and co.y2 >= self.game.height:
            self.y = 0
            bottom = False
        elif self.y < 0 and co.y1 <= 0:
            self.y = 0
            top = False
        if self.x > 0 and co.x2 >= self.game.width:
            self.x = 0
            right = False
        elif self.x < 0 and co.x1 <= 0:
            self.x = 0
            left = False

        for sprite in self.game.sprites:
            if sprite == self:
                continue
            if sprite.coordinateds == None:
                continue

            sprite_co = sprite.coords()

            if sprite.type == "item":
                if collided_left(co, sprite_co) or collided_right(co, sprite_co) or collided_top(co, sprite_co) or collided_bottom(0, co, sprite_co):
                    self.game.hp.reset()
                    self.game.canvas.delete(sprite.image)
                    self.game.sprites.remove(sprite)
                    continue

            if top and self.y < 0 and collided_top(co, sprite_co):
                self.y = -self.y
                top = False
            if bottom and self.y > 0 and collided_bottom(self.y, co, sprite_co):
                self.y = sprite_co.y1 - co.y2
                if self.y < 0:
                    self.y = 0
                bottom = False
                top = False
            if bottom and falling and self.y == 0 and co.y2 < self.game.height and collided_bottom(1, co, sprite_co):
                falling = False
            if left and self.x < 0 and collided_left(co, sprite_co):
                self.x = 0
                left = False
            if right and self.x > 0 and collided_right(co, sprite_co):
                self.x = 0
                right = False
            if falling and bottom and self.y == 0 and co.y2 < self.game.height:
                self.y = 4

        self.game.canvas.move(self.image, self.x, self.y)

if __name__ == "__main__":
    g = Game("Dinosaur Escape Room", 500, "assets/background.gif")

    g.add_sprite(Bar(g, "assets/bar1.gif",   0, 490, 100, 10))
    g.add_sprite(Bar(g, "assets/bar1.gif", 110, 440, 100, 10))
    g.add_sprite(Bar(g, "assets/bar1.gif", 220, 410, 100, 10))
    g.add_sprite(Bar(g, "assets/bar1.gif", 330, 390, 100, 10))
    g.add_sprite(Bar(g, "assets/bar1.gif", 400, 350, 100, 10))
    g.add_sprite(Item(g, "assets/item/고기.png", 300, 300, 30, 30))
    g.add_sprite(HelthBar(g))
    g.add_sprite(StickFigureSprite(g))

    g.mainloop()
