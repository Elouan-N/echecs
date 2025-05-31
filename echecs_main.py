from math import *
from kandinsky import *
from random import *
from ion import *
from time import *
from echecs_graphismes import *
from echecs_objets import *

THEMES=[
  Theme([(0,127,0),(167,167,167),(87,87,87),(255,255,255),(0,0,0),(255,0,0),(255,255,255),(255,0,0)]),
  Theme([(63,63,127),(255,191,127),(127,63,0),(255,255,255),(0,0,0),(63,127,255),(63,255,255),(63,127,255)]),
  Theme([(63,127,63),(255,127,63),(191,63,0),(255,255,255),(0,0,0),(0,0,63),(255,191,127),(191,191,191)]),
]

def pion_bouge(x1,y1,disposition):
  if not ((piece:=disposition.lpos[y1][x1]).blanc==disposition.trait_blanc and 0<y1<7 and 0<=x1<=7):
    return []
  coups=[]
  if disposition.lpos[(y2:=y1-(2*int(piece.blanc)-1))][x1] is None:
    coups.append(Coup([x1,y1],[x1,y2]))
    if y1==int(piece.blanc)*5+1 and disposition.lpos[(y2:=y1-2*(2*int(piece.blanc)-1))][x1] is None:
      coups.append(Coup([x1,y1],[x1,y2]))
  return coups

def pion_mange(x1,y1,disposition):
  if not ((piece:=disposition.lpos[y1][x1]).blanc==disposition.trait_blanc and 0<y1<7 and 0<=x1<=7):
    return []
  coups=[]
  if 0<=(y2:=y1-(2*int(piece.blanc)-1))<=7 and 0<=(x2:=x1+1)<=7 and (target:=disposition.lpos[y2][x2]) is not None and target.blanc!=piece.blanc:
    coups.append(Coup([x1,y1],[x2,y2]))
  if 0<=y2<=7 and 0<=(x2:=x1-1)<=7 and (target:=disposition.lpos[y2][x2]) is not None and target.blanc!=piece.blanc:
    coups.append(Coup([x1,y1],[x2,y2]))
  return coups

def cavalier_bouge(x1,y1,disposition):
  if not ((piece:=disposition.lpos[y1][x1]).blanc==disposition.trait_blanc and 0<=y1<=7 and 0<=x1<=7):
    return []
  coups=[]
  depls_faisables=[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
  for depl in depls_faisables:
    if 0<=(y2:=y1+depl[1])<=7 and 0<=(x2:=x1+depl[0])<=7 and (target:=disposition.lpos[y2][x2]) is None:
      coups.append(Coup([x1,y1],[x2,y2]))
  return coups

def cavalier_mange(x1,y1,disposition):
  if not ((piece:=disposition.lpos[y1][x1]).blanc==disposition.trait_blanc and 0<=y1<=7 and 0<=x1<=7):
    return []
  coups=[]
  depls_faisables=[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
  for depl in depls_faisables:
    if 0<=(y2:=y1+depl[1])<=7 and 0<=(x2:=x1+depl[0])<=7 and (target:=disposition.lpos[y2][x2]) is not None and target.blanc!=piece.blanc:
      coups.append(Coup([x1,y1],[x2,y2]))
  return coups

def fou_mange(x1,y1,disposition):
  if not ((piece:=disposition.lpos[y1][x1]).blanc==disposition.trait_blanc and 0<=y1<=7 and 0<=x1<=7):
    return []
  coups=[]
  depls_faisables=[(-1,-1),(-1,1),(1,-1),(1,1)]
  for depl in depls_faisables:
    y2,x2=y1,x1
    while (0<=(y2:=y2+depl[1])<=7 and 0<=(x2:=x2+depl[0])<=7
    and disposition.lpos[y2][x2] is None):
      pass
    if (0<=y2<=7 and 0<=x2<=7
    and (target:=disposition.lpos[y2][x2]) is not None and target.blanc!=piece.blanc):
      coups.append(Coup([x1,y1],[x2,y2]))
  return coups

def fou_bouge(x1,y1,disposition):
  if not ((piece:=disposition.lpos[y1][x1]).blanc==disposition.trait_blanc and 0<=y1<=7 and 0<=x1<=7):
    return []
  coups=[]
  depls_faisables=[(-1,-1),(-1,1),(1,-1),(1,1)]
  for depl in depls_faisables:
    y2,x2=y1,x1
    while (0<=(y2:=y2+depl[1])<=7 and 0<=(x2:=x2+depl[0])<=7
    and disposition.lpos[y2][x2] is None):
      coups.append(Coup([x1,y1],[x2,y2]))
  return coups

def tour_bouge(x1,y1,disposition):
  if not ((piece:=disposition.lpos[y1][x1]).blanc==disposition.trait_blanc and 0<=y1<=7 and 0<=x1<=7):
    return []
  coups=[]
  depls_faisables=[(-1,0),(0,-1),(0,1),(1,0)]
  for depl in depls_faisables:
    y2,x2=y1,x1
    while (0<=(y2:=y2+depl[1])<=7 and 0<=(x2:=x2+depl[0])<=7
    and disposition.lpos[y2][x2] is None):
      coups.append(Coup([x1,y1],[x2,y2]))
  return coups

def tour_mange(x1,y1,disposition):
  if not ((piece:=disposition.lpos[y1][x1]).blanc==disposition.trait_blanc and 0<=y1<=7 and 0<=x1<=7):
    return []
  coups=[]
  depls_faisables=[(-1,0),(0,-1),(0,1),(1,0)]
  for depl in depls_faisables:
    y2,x2=y1,x1
    while (0<=(y2:=y2+depl[1])<=7 and 0<=(x2:=x2+depl[0])<=7
    and disposition.lpos[y2][x2] is None):
      pass
    if (0<=y2<=7 and 0<=x2<=7
    and (target:=disposition.lpos[y2][x2]) is not None and target.blanc!=piece.blanc):
      coups.append(Coup([x1,y1],[x2,y2]))
  return coups

def dame_bouge(x1,y1,disposition):
  return fou_bouge(x1,y1,disposition)+tour_bouge(x1,y1,disposition)

def dame_mange(x1,y1,disposition):
  return fou_mange(x1,y1,disposition)+tour_mange(x1,y1,disposition)

def roi_bouge(x1,y1,disposition):
  if not ((piece:=disposition.lpos[y1][x1]).blanc==disposition.trait_blanc and 0<=y1<=7 and 0<=x1<=7):
    return []
  coups=[]
  depls_faisables=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
  for depl in depls_faisables:
    if 0<=(y2:=y1+depl[1])<=7 and 0<=(x2:=x1+depl[0])<=7 and (target:=disposition.lpos[y2][x2]) is None:
      coups.append(Coup([x1,y1],[x2,y2]))
  return coups

def roi_mange(x1,y1,disposition):
  if not ((piece:=disposition.lpos[y1][x1]).blanc==disposition.trait_blanc and 0<=y1<=7 and 0<=x1<=7):
    return []
  coups=[]
  depls_faisables=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
  for depl in depls_faisables:
    if 0<=(y2:=y1+depl[1])<=7 and 0<=(x2:=x1+depl[0])<=7 and (target:=disposition.lpos[y2][x2]) is not None and target.blanc!=piece.blanc:
      coups.append(Coup([x1,y1],[x2,y2]))
  return coups

TYPES_DE_PIECE=[
  TypeDePiece("Pion",
              pion_bouge,
              pion_mange,
              dessin_pion,
              1,
  ),
  TypeDePiece("Cavalier",
              cavalier_bouge,
              cavalier_mange,
              dessin_cavalier,
              3,
  ),
  TypeDePiece("Fou",
              fou_bouge,
              fou_mange,
              dessin_fou,
              3,
  ),
  TypeDePiece("Tour",
              tour_bouge,
              tour_mange,
              dessin_tour,
              5,
  ),
  TypeDePiece("Dame",
              dame_bouge,
              dame_mange,
              dessin_dame,
              9,
  ),
  TypeDePiece("Roi",
              roi_bouge,
              roi_mange,
              dessin_roi,
              10,
  ),
]

ORDRE_DES_PIECES=[3,1,2,4,5,2,1,3]

DISPO_DE_BASE=Disposition(
  [
    [Piece(False,TYPES_DE_PIECE[i]) for i in ORDRE_DES_PIECES],
    [Piece(False,TYPES_DE_PIECE[0]) for _ in range(8)],
    [None for _ in range(8)],
    [None for _ in range(8)],
    [None for _ in range(8)],
    [None for _ in range(8)],
    [Piece(True,TYPES_DE_PIECE[0]) for _ in range(8)],
    [Piece(True,TYPES_DE_PIECE[i]) for i in ORDRE_DES_PIECES],
  ],
  True,
  [],
  [],
)

DISPO_DE_BASE.coups_possibles()

focus_target=[[0,0],[0,0]]
mode=0
dispo_courante=DISPO_DE_BASE
i_theme=0
theme_courant=THEMES[i_theme]
t=dict([(i,[]) for i in range(75)])

def attendre(touche):
  while not keydown(touche):
    pass
  sleep(0.2)

def dessin():
  dispo_courante.dessin(theme_courant)
  dessin_focus(60+focus_target[0][0]*25,11+focus_target[0][1]*25,theme_courant.cols[7])
  if mode==1:
    dessin_target(60+focus_target[1][0]*25,11+focus_target[1][1]*25,theme_courant.cols[7])
  sleep(0.2)  

def affichage(messages):  
    fill_rect(50,50,220,122,theme_courant.cols[5])
    for i in range(len(messages)):
      draw_string(messages[i],160-5*len(messages[i]),60+25*i,theme_courant.cols[6],theme_courant.cols[5])
    draw_string("Pour quitter cette",160-5*18,136,theme_courant.cols[6],theme_courant.cols[5])
    draw_string("fenetre pressez OK",160-5*18,154,theme_courant.cols[6],theme_courant.cols[5])

def deplacement():
  global i_theme,theme_courant
  if keydown(KEY_LEFT) and focus_target[mode][0]>0:
    focus_target[mode][0]-=1
    dessin()
  elif keydown(KEY_RIGHT) and focus_target[mode][0]<7:
    focus_target[mode][0]+=1
    dessin()
  elif keydown(KEY_UP) and focus_target[mode][1]>0:
    focus_target[mode][1]-=1
    dessin()
  elif keydown(KEY_DOWN) and focus_target[mode][1]<7:
    focus_target[mode][1]+=1
    dessin()
  elif keydown(KEY_ZERO):
    i_theme=(i_theme+1)%len(THEMES)
    theme_courant=THEMES[i_theme]
    dessin()

def meilleurs_coups(disposition,n):
  result = [(coup,(disposition+coup).evalue(disposition.trait_blanc)) for coup in disposition.coups_possibles]
  meilleurs=[]
  for _ in range(n):
    if result==[]:
      break
    meilleurs.append(max(result,key=lambda paire:paire[1]))
    result.remove(meilleurs[-1])
  return list(map(lambda elt:elt[0],meilleurs))

def ia(disposition):
  meilleurs=meilleurs_coups(disposition,4)
  if len(meilleurs)==1:
    return meilleurs[0]
  dico_meilleurs=dict()
  for coup in meilleurs:
    nouv_dispo=disposition+coup
    nouv_meilleurs=meilleurs_coups(disposition,1)
    dico_meilleurs[coup]=(nouv_dispo+nouv_meilleurs[0]).evalue(disposition.trait_blanc)
  coups_tries=sorted(dico_meilleurs.items(),key=lambda item:item[1],reverse=True)
  return coups_tries[0][0]
  somme=sum(map(lambda item:item[1],coups_tries))
  alea=random()*somme
  for paire in coups_tries:
    alea-=paire[1]
    if alea<=0:
      return paire[0]
  return paire[0]

def main():
  global focus_target,mode,dispo_courante
  focus_target=[[0,0],[0,0]]
  mode=0
  dispo_courante=DISPO_DE_BASE
  theme_courant=THEMES[0]
  fin=None
  sleep(0.2)
  dessin()
  while fin is None:
    while not keydown(KEY_EXE):
      mode=0
      dessin()
      while not keydown(KEY_OK):
        deplacement()
      mode=1
      focus_target[1]=focus_target[0][:]
      dessin()
      while not keydown(KEY_OK) and not keydown(KEY_EXE):
        deplacement()
    mode=0
    coup=Coup(focus_target[0],focus_target[1])
    if repr(focus_target) in list(map(str,dispo_courante.coups_possibles)):
      dispo_courante=dispo_courante+coup
      dessin()
      dispo_courante.coups_possibles()
      if dispo_courante.mat():
        fin=["Les blancs ont","gagne par","echec et mat"]
      elif dispo_courante.pat():
        fin=["Match nul"]
      else:
        dispo_courante=dispo_courante+ia(dispo_courante)
        dessin()
        dispo_courante.coups_possibles()
        if dispo_courante.mat():
          fin=["Les noirs ont","gagne par","echec et mat"]
        elif dispo_courante.pat():
          fin=["Match nul"]
    else:
      affichage([repr(coup)+" n'est","pas valide"])
      attendre(KEY_OK)
  for paire in t.items():
    if paire[1]!=[]:
      print(paire[0],sum(paire[1])/len(paire[1])/paire[0])
  affichage(fin)
  attendre(KEY_OK)
  dessin()

def test1():
  for _ in range(1):
    dispo=DISPO_DE_BASE
    dispo.dessin(THEMES[2])
    while not dispo.mat() and not dispo.pat():
      t1=monotonic()
      dispo=dispo+ia(dispo)
      t2=monotonic()
      print(t2-t1)
      dispo.dessin(THEMES[2])
      dispo.coups_possibles()
