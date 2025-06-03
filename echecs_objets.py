from math import *
from kandinsky import *
from echecs_graphismes import *

class TypeDePiece:
  def __init__(self,nom,peut_aller,peut_manger,dessin,valeur):
    self.nom=nom
    self.peut_aller=peut_aller
    self.peut_manger=peut_manger
    self.dessin=dessin
    self.valeur=valeur
  
  def __str__(self):
    return nom[0]
  
  def __repr__(self):
    return "Type "+self.nom

class Piece:
  def __init__(self,blanc,type):
    self.blanc=blanc
    self.type=type
  
  def __str__(self):
    return str(self.type)+("b" if self.blanc else "n")
  
  def __repr__(self):
    return self.type.nom+(" blanc(he)" if self.blanc else " noir(e)")

class Coup:
  def __init__(self,origine,destination):
    self.origine=origine
    self.destination=destination
  
  def __str__(self):
    return [self.origine,self.destination]
  
  def __repr__(self):
    cases="ABCDEFGH"
    return (cases[self.origine[0]]
    +str(8-self.origine[1])
    +" -> "
    +cases[self.destination[0]]
    +str(8-self.destination[1]))
  
  def __add__(self,disposition):
    if not isinstance(disposition,Disposition):
      raise TypeError("Can't add 'Coup' object with non-'Disposition' object.")
    else:
      return disposition+self
  
  def est_faisable(self,disposition):
    if self.origine==self.destination:
      return False
    x1,y1=self.origine
    x2,y2=self.destination
    piece=disposition.lpos[y1][x1]
    if piece is None:
      return False
    return ((piece.type.peut_aller(x1,y1,x2,y2,disposition)
    or piece.type.peut_manger(x1,y1,x2,y2,disposition))
    and not (disposition+self).echec(disposition.trait_blanc)
    and piece.blanc==disposition.trait_blanc)


class Disposition:
  def __init__(self,lpos,trait_blanc,historique,manges):
    self.lpos=lpos
    self.trait_blanc=trait_blanc
    self.historique=historique
    self.manges=manges
    self.roipos=[[0,0],[0,0]]
    for y in range(8):
      for x in range(8):
        if (not self.lpos[y][x] is None
        and self.lpos[y][x].type.nom=="Roi"):
          self.roipos[int(self.lpos[y][x].blanc)]=[x,y]
      
  def __repr__(self):
    return self.lpos
  
  def __add__(self,coup):
    x1,y1=coup.origine
    x2,y2=coup.destination
    nouv_lpos=[self.lpos[i][:] for i in range(8)]
    piece=nouv_lpos[y1][x1]
    piece_mangee=nouv_lpos[y2][x2]
    nouv_manges=self.manges[:]
    if piece_mangee is not None:
      nouv_manges.append(piece_mangee)
    nouv_lpos[y1][x1]=None
    nouv_lpos[y2][x2]=piece
    nouv_hist=self.historique+[coup]
    if piece is not None and piece.type.nom=="Pion" and y2==7*int(not piece.blanc):
      from echecs_main import TYPES_DE_PIECE
      nouv_lpos[y2][x2]=Piece(piece.blanc,TYPES_DE_PIECE[4])
    return Disposition(nouv_lpos,not self.trait_blanc,nouv_hist,nouv_manges)
  
  def dessin(self,theme):
    # l'arriere plan
    fill_rect(0,0,320,222,theme.cols[0])
    # l'echiquier
    fill_rect(60,11,200,200,theme.cols[1])
    for i in range(32):
      fill_rect(60+50*(i%4)+25*(1-i//4%2),11+25*(i//4),25,25,theme.cols[2])
    # les pieces
    for y in range(8):
      for x in range(8):
        if (piece:=self.lpos[y][x]) is None: continue
        piece.type.dessin(60+25*x,11+25*y,theme.cols[4-int(piece.blanc)])
    # les pieces mangees
    self.manges.sort(key=lambda piece:(piece.type.valeur,piece.type.nom),reverse=True)
    i=0
    j=0
    for piece in self.manges:
      if piece.blanc:
        piece.type.dessin(260+18*(j%3),11+25*(j//3),theme.cols[3])
        j+=1
      else:
        piece.type.dessin(-1+18*(i%3),11+25*(i//3),theme.cols[4])
        i+=1
    # echec
    if (self+Coup([0,0],[0,0])).echec(self.trait_blanc):
      draw_string("ECHEC",5,191,theme.cols[6],theme.cols[0])

  def coups_possibles(self):
    self.coups_possibles=[]
    for y in range(8):
      for x in range(8):
        if (piece:=self.lpos[y][x]) is None: continue
        self.coups_possibles.extend(piece.type.peut_aller(x,y,self)+piece.type.peut_manger(x,y,self))
    self.coups_possibles=list(filter(lambda coup:not (self+coup).echec(self.trait_blanc),self.coups_possibles))
    return self.coups_possibles
  
  def echec(self,blanc):
    for y in range(8):
      for x in range(8):
        if self.lpos[y][x] is None or self.lpos[y][x].blanc==blanc: continue
        for coup in self.lpos[y][x].type.peut_manger(x,y,self):
          if coup.destination==self.roipos[int(blanc)]:
            return True
    return False
  
  def mat(self):
    return self.coups_possibles==[] and (self+Coup([0,0],[0,0])).echec(self.trait_blanc)
  
  def pat(self):
    return self.coups_possibles==[] and not (self+Coup([0,0],[0,0])).echec(self.trait_blanc)

  def evalue(self,blanc,a,b,c,d):
    if self.mat() or self.pat():
      return 100*int(blanc==self.trait_blanc)-50
    
    points=[0,0]
    menacees=[0,0]
    barycentre=[0,0]
    coeff=0
    for y in range(8):
      for x in range(8):
        if (piece:=self.lpos[y][x]) is not None:
          # difference de points
          points[int(piece.blanc)]+=piece.type.valeur
          # pieces menacees
          menacees[int(piece.blanc)]+=sum(map(
          lambda coup:self.lpos[coup.destination[1]][coup.destination[0]].type.valeur,
          piece.type.peut_manger(x,y,(self,self+Coup([0,0],[0,0]))[int(piece.blanc!=self.trait_blanc)]),
          ))
          # barycentre pondere
          if piece.blanc==blanc:
            barycentre[0]+=x*(9-piece.type.valeur)
            barycentre[1]+=y*(9-piece.type.valeur)
            coeff+=piece.type.valeur
    barycentre[0]/=coeff
    barycentre[1]/=coeff
    # avancement
    X=min(1,len(self.historique)/50)
    objectif=[
      3.5*(1-X)+self.roipos[int(not self.trait_blanc)][0]*X,
      (2.5+2*int(blanc))*(1-X)+self.roipos[int(not self.trait_blanc)][1]*X,
    ]
    return (0
    + a*(points[int(blanc)]-points[int(not blanc)])/49
    + b*(1-sqrt((barycentre[0]-objectif[0])**2+(barycentre[1]-objectif[1])**2)/8)
    + c*menacees[int(blanc)]/40
    - d*menacees[int(not blanc)]/40
    )

class Theme:
  def __init__(self,cols):
    self.cols=cols
  
  def dessin(self,x,y):
    fill_rect(x,y,50,50,self.cols[1])
    fill_rect(x+25,y,25,25,self.cols[2])
    fill_rect(x,y+25,25,25,self.cols[2])
    dessin_cavalier(x,y,self.cols[3])
    dessin_pion(x,y+25,self.cols[3])
    dessin_cavalier(x+25,y,self.cols[4])
    dessin_pion(x+25,y+25,self.cols[4])
