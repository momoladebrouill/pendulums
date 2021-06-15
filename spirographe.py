import pygame as pg
import noise
import math
import random
from pygame import gfxdraw
from colorsys import hsv_to_rgb
# Constantes :
FPS = 60  # les fps tabernak
WIND = 750  # dimentions de la fentere
NOMBRE = 2 # nombre de barres
pg.init()
f = pg.display.set_mode(size=(WIND, WIND))
pg.display.set_caption("Pendulum")
fpsClock = pg.time.Clock()
font = pg.font.Font('../consolas.ttf', 30)  # police//roxane
b = 1
positions = []
Reves = []
coul=random.random()*360
couleur_boule=hsv_to_rgb(coul,1,255)
couleur_trait=hsv_to_rgb(360-coul,1,255)

class Pos:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.taille = WIND / 2

    def get_pos(self):
        return (self.x, self.y)


class Pendule:
    def __init__(self, x, y):
        self.pos = Pos(x, y)
        self.angle = random.random() * math.tau
        self.taille = WIND/2/NOMBRE
        self.coef = 50
        self.mouv = 0
        self.vitesse = (random.random() - 0.5) / 5
        self.boul = Pos(self.pos.x + math.cos(self.angle) * self.coef,
                        self.pos.y + math.sin(self.angle) * self.coef)

    def update(self):
        self.angle += self.vitesse

    def draw(self):
        self.boul.x = self.pos.x + math.cos(self.angle) * self.taille
        self.boul.y = self.pos.y + math.sin(self.angle) * self.taille
        pg.draw.line(f, (255, 255, 255), self.pos.get_pos(),
                     self.boul.get_pos())
        pg.draw.circle(f, couleur_boule, self.boul.get_pos(), 5)


def dist(a: Pos, b: Pos):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)


mouv_speed = 10
Reves.append(Pendule(WIND / 2, WIND / 2))

for i in range(NOMBRE - 1):
    Reves.append(Pendule(Reves[-1].boul.x, Reves[-1].boul.y))
try:
    while b:
        b += 1
        # Actualiser:
        pg.display.flip()
        # Appliquer les images de fond sur la fenetre
        s = pg.Surface((WIND, WIND))
        s.set_alpha(255)
        s.fill((0, 0, 0))
        f.blit(s, (0, 0))

        Reves[0].update()
        for i in range(NOMBRE - 1):
            Reves[i + 1].pos = Reves[i].boul
            Reves[i + 1].update()
        if not b%2:
            positions.append(Pos(Reves[-1].boul.x, Reves[-1].boul.y))
        ind = 0
        for ind,posz in enumerate(positions):
            if ind>0:
                pg.draw.line(f,couleur_trait,(posz.x, posz.y),(positions[ind-1].x, positions[ind-1].y))
##            pg.draw.rect(f, couleur_boule, (posz.x, posz.y, 5, 5))
            ind += 1
        if ind > 2000:
            positions.pop(0)
        for reve in Reves:
            reve.draw()

        pointer = pg.mouse
        pos = pointer.get_pos()

        for event in pg.event.get():  # QUAND la touche est appuyée
            if event.type == pg.QUIT:
                b = False
                print(" Fin du jeu  babe")
            elif event.type == pg.KEYUP:
                if event.dict['key'] == pg.K_SPACE:
                    coul=random.random()*360
                    couleur_boule=hsv_to_rgb(coul,1,255)
                    couleur_trait=hsv_to_rgb(360-coul,1,255)

                    Reves[0].__init__(WIND / 2, WIND / 2)
                    for i in range(NOMBRE - 1):
                        Reves[i + 1].__init__(Reves[i].boul.x,
                                              Reves[i].boul.y)
                    positions = []

                """if event.dict['key']==pg.K_a:"""

            elif event.type == pg.MOUSEBUTTONUP:
                """if event.button==1: #click gauche
                    pos=event.pos


                if event.button==3: #click droit

                elif event.button==4: #vers le haut
                    zoom+=0.01
                elif event.button==5: #vers le bas
                    zoom-=0.01"""

        #text = font.render(str(reve.angle), True, (255,255,255))
        #textRect = text.get_rect()
        #f.blit(text, (0,0))

        fpsClock.tick(FPS)
except:
    pg.quit()
    raise
finally:
    pg.quit()
