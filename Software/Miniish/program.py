from pyco import *

# main

def ball(): pass


def _init():
 music(0)
 ball_init(ball)


def _update():
 ball.update()


def _draw():
 cls()
 ball.draw()
# ball

def ball_init(self):
 self.x = 32
 self.y = 48
 self.dx = 2
 self.dy = 1
 self.update = lambda:ball_update(self)
 self.draw = lambda:ball_draw(self)


def ball_update(self):
 self.x += self.dx
 self.y += self.dy

 if self.x < 0 or self.x > 120:
  sfx(0)
  self.dx = -self.dx

 if self.y < 0 or self.y > 120:
  sfx(0)
  self.dy = -self.dy


def ball_draw(self):
 spr(1, (self.x, self.y))
