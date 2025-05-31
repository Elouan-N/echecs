from kandinsky import *
from time import *

# taille des cellules : 25x25

def dessin_pion(x,y,col):
  fill_rect(x+10,y+6,5,7,col)
  fill_rect(x+9,y+7,7,5,col)
  fill_rect(x+11,y+13,3,3,col)
  fill_rect(x+10,y+16,5,3,col)
  fill_rect(x+8,y+19,9,1,col)
  fill_rect(x+5,y+20,15,3,col)

def dessin_cavalier(x,y,col):
  fill_rect(x+7,y+2,8,10,col)
  fill_rect(x+6,y+4,12,3,col)
  fill_rect(x+17,y+6,3,8,col)
  fill_rect(x+20,y+9,3,6,col)
  fill_rect(x+8,y+9,9,11,col)
  fill_rect(x+5,y+20,15,3,col)

def dessin_roi(x,y,col):
  fill_rect(x+11,y+2,3,18,col)
  fill_rect(x+9,y+4,7,3,col)
  fill_rect(x+2,y+9,21,3,col)
  fill_rect(x+4,y+12,3,9,col)
  fill_rect(x+18,y+12,3,9,col)
  fill_rect(x+6,y+20,13,3,col)

def dessin_tour(x,y,col):
  fill_rect(x+5,y+2,3,5,col)
  fill_rect(x+11,y+2,3,2,col)
  fill_rect(x+17,y+2,3,5,col)
  fill_rect(x+8,y+4,9,16,col)
  fill_rect(x+5,y+20,15,3,col)

def dessin_fou(x,y,col):
  fill_rect(x+11,y+2,4,4,col)
  fill_rect(x+8,y+6,6,3,col)
  fill_rect(x+16,y+7,2,3,col)
  fill_rect(x+5,y+9,8,9,col)
  fill_rect(x+15,y+10,5,8,col)
  fill_rect(x+8,y+15,9,8,col)
  fill_rect(x+5,y+20,15,3,col)

def dessin_dame(x,y,col):
  fill_rect(x+8,y+2,3,11,col)
  fill_rect(x+14,y+2,3,11,col)
  fill_rect(x+7,y+3,5,3,col)
  fill_rect(x+13,y+3,5,3,col)
  fill_rect(x+3,y+7,3,8,col)
  fill_rect(x+19,y+7,3,8,col)
  fill_rect(x+2,y+8,5,3,col)
  fill_rect(x+18,y+8,5,3,col)
  fill_rect(x+5,y+13,15,6,col)
  fill_rect(x+6,y+19,13,4,col)

def dessin_focus(x,y,col):
  fill_rect(x,y,7,2,col)
  fill_rect(x+18,y,7,2,col)
  fill_rect(x,y+23,7,2,col)
  fill_rect(x+18,y+23,7,2,col)
  fill_rect(x,y,2,7,col)
  fill_rect(x+23,y,2,7,col)
  fill_rect(x,y+18,2,7,col)
  fill_rect(x+23,y+18,2,7,col)

def dessin_target(x,y,col):
  fill_rect(x+11,y+8,3,9,col)
  fill_rect(x+8,y+11,9,3,col)
