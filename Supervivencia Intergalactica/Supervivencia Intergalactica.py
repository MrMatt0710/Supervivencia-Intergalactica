from tkinter import CENTER
from turtle import pos
import pygame, os, random
import json
from datetime import datetime

pygame.init()
clock=pygame.time.Clock()
directory = os.path.dirname(os.path.realpath(__file__))
pygame.font.init()

########## VENTANA ########## 

ANCHO=800
ALTO=500
size = (ANCHO, ALTO)
pantalla = pygame.display.set_mode(size)
pygame.display.set_caption("Supervivencia Intergalactica")

                   
########## COLORES ########## 

RED = (255, 0, 0)
BLUE = (100, 100, 255)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

########## FONDOS ########## 

menuBg = pygame.image.load("menuBg.png").convert_alpha()
fondo = pygame.image.load('fondo.png').convert_alpha()

########## FONTS ########## 

myfont = pygame.font.Font('Minecraft.ttf', 20)

########## VARIABLES  GLOBALES ########## 

userName = str
energy = 100
points = 0
date = str
speed = 5
first = True

########## SONIDOS ########## 

sonidochoque = pygame.mixer.Sound(directory + "/crash.wav")
sonidoPoints = pygame.mixer.Sound(directory + "/points.wav")
sonidoGameOver = pygame.mixer.Sound(directory + "/gameOver.wav")

########## Clases, Instancias, Grupos ########## 

class enemyCar(pygame.sprite.Sprite):

    def __init__(self, kind, lane):
        super().__init__()

        global speed
        
        self.size = (50, 50)

        self.kind = kind
        self.lane = lane

        if self.kind == 1:
            self.image = pygame.image.load(directory + "/satelite.1.2.png").convert_alpha()
        elif self.kind == 2:
            self.image = pygame.image.load(directory + "/Planeta -1.2.png").convert_alpha()
        elif self.kind == 3:
            self.image = pygame.image.load(directory + "/Galaxia-1.1.png").convert_alpha()
        elif self.kind == 4:
            self.image = pygame.image.load(directory + "/disco-1.2.png").convert_alpha()
        elif self.kind == 5:
            self.image = pygame.image.load(directory + "/Rokita.png").convert_alpha()
        elif self.kind == 6:
            self.image = pygame.image.load(directory + "/disco-1.3.png").convert_alpha()
            
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = self.lane
        self.rect.y = -100
        
    def moveForward(self):
        
        if self.rect.y < 650:
            self.rect.y += speed
        else:
            self.kill()

enemyCar1 = enemyCar(1, 200)
enemyCarGroup = pygame.sprite.Group()
enemyCarGroup.add(enemyCar1)

class thing(pygame.sprite.Sprite):

    def __init__(self, lane):
        super().__init__()
          
        self.image = pygame.image.load(directory + "/Rayo.1.2.png").convert_alpha()
        self.rect = self.image.get_rect()
        
        self.rect.y = -100
        self.rect.x = lane
    def moveForward(self):
    
        if self.rect.y < 800:
            self.rect.y += speed
        else:
           self.kill()

thing1 = thing(-200) 
thingGroup = pygame.sprite.Group()
thingGroup.add(thing1)
         
class kar(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
        self.image = pygame.image.load(directory + "/Nave.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 400
        self.shotlist = []
        
    def derecha(self, pixels):
        if self.rect.x < 700:
            self.rect.x += pixels
 
    def izquierda(self, pixels):
        if self.rect.x > 50 :
            self.rect.x -= pixels

    def shot (self,pos_x,pos_y,speed):
        laser = Laser(pos_x,pos_y,speed)
        self.shotlist.append(laser)

playerKar = kar() 
kar_group = pygame.sprite.Group() 
kar_group.add(playerKar)


class Laser(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y,speed):
        self.image = pygame.image.load(directory + "/laser.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = pos_x + 30
        self.rect.y = pos_y
        self.speed = speed + 5
        self.height_y_constraint = 500
            
    def draw(self,surface):
        surface.blit(self.image,self.rect)

    def updatePosition(self):
            
	    self.rect.y -= self.speed
        
    



class landscape(pygame.sprite.Sprite):
    
    global speed
    
    def __init__(self, y):
        super().__init__()
       
        self.image = pygame.image.load(directory + "/Espacio.png").convert_alpha()
        self.rect = self.image.get_rect() 
        self.rect.y = y
        
    def play(self):
        if self.rect.y < 500:
            self.rect.y += speed
        else:
            self.rect.y = -500
            
lands01 = landscape(-500) 
lands02 = landscape(0) 
lands_group = pygame.sprite.Group() 
lands_group.add(lands01) 
lands_group.add(lands02)

class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            text = myfont.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

        pos = pygame.mouse.get_pos()
        if self.isOver(pos):
            self.color = WHITE
        else:
            self.color = GREY

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
                
        return False    

okBtn = button(RED, 250, 300, 200, 25, "ok")

class InputBox:
    
    COLOR_INACTIVE = BLACK
    COLOR_ACTIVE = WHITE

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = InputBox.COLOR_INACTIVE
        self.text = text
        self.txt_surface = myfont.render(text, True, BLACK)
        self.active = False

    def handle_event(self, event):
    ###Color recuadros o botones###
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = InputBox.COLOR_ACTIVE if self.active else InputBox.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    if len(self.text) < 10:
                        self.text += event.unicode
                self.txt_surface = myfont.render(self.text, True, self.color)
                
    def update(self):
        ######Reajustar tamaño de recuadro por si el texto esta muy largo#####
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, pantalla):#blit
        pantalla.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(pantalla, self.color, self.rect, 2) 
    
input_box1 = InputBox(300, 300, 140, 32)  

##### FUNCIONES #####

#Cambiar Escena

def changescn(scn, text="", btnfnc=""):
    
    # ~ continuar haciendo lo mismo que abajo
    global menu_s, enterName_s, mainLoop_s, instructions_s, creditos_s, msg_s, scores_s
    menu_s = enterName_s = mainLoop_s = instructions_s = creditos_s = msg_s = scores_s = False
    
    if scn == "menu":
        menu_s = True
        menu()
    
    elif scn == "enterName":
        enterName_s = True
        enterName()
        
    elif scn == "mainLoop":
        mainLoop_s = True
        mainLoop()
        
    elif scn == "instructions":
        instructions_s = True
        instructions()

    elif scn == "creditos":
        creditos_s = True
        creditos()    
        
    elif scn == "msg":
        msg_s = True
        msg(text,btnfnc)
   
    elif scn == "scores":
        scores_s = True
        scores()


msg_s = True
def msg(text,btnfnc):
    
    global msg_s, first

    msgOkBtn = button(RED, ANCHO/2 - 100, ALTO/2, 200, 25, "OK")
    label = pygame.font.Font('Minecraft.ttf', 30).render(text, 1, WHITE)
    
    if text == "Game Over!":
        Musica("stop")
        resetGame()
        first = True
        sonidoGameOver.play()
        
    while msg_s:    
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(label, (ANCHO/2 - label.get_width()/2, ALTO/2 - label.get_height()/2 - 50))
        msgOkBtn.draw(pantalla, BLACK)
        
        ##### UPDATE #####
        
        pygame.display.flip()  
      
        ##### EVENTS #####
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            
            if event.type==pygame.QUIT:
                msg_s = False
                        
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if msgOkBtn.isOver(pos):
                    if text == "Game Over!":
                        Musica("main")
                    changescn(btnfnc)
                 
            if event.type == pygame.KEYDOWN:
                                
                if event.key==pygame.K_ESCAPE:
                    changescn(btnfnc)       

            
##### Cambiar musica

def Musica(music):

    if music == "main":
        pygame.mixer.music.load(directory + "/music.wav")
        pygame.mixer.music.play(-1)
        
    elif music == "engine":
        pygame.mixer.music.load(directory + "/music.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        
    elif music == "stop":
        pygame.mixer.music.stop()
        

            
##### Guardar puntaje /UTILIZACION JSON

sortedData = []
data = {}
def saveGame():
    
    global sortedData, data, date, points, userName
    
    with open(directory + "\\save\\" + "scores.txt", "r") as f:
        data = json.load(f)

    # Añadir informacion del juego
    data.update({date:{"name":userName, "points":points, "energy":energy}} )
    
    # Ordenar la Informacion y Limpiarla
    sortedData = sorted(data.items(), key=lambda x: x[1]['points'], reverse=True) # ordenar diccionario de diccionarios
    try:
        del data[sortedData[10][0]]

    except IndexError:
        pass

    # Dictar lo de la carpeta del JSON
    with open(directory + "\\save\\" + "scores.txt", "w") as f:
        json.dump(data, f)

def things():
    
    global points, speed
     
    points += 1
    sonidoPoints.play()
    thing1.rect.y = 600
    thingGroup.add(thing1)
    speed += 1


def informacion():

    global energy, userName, points
    
    label0 = myfont.render("Nick: " + str(userName), 1, WHITE)
    pantalla.blit(label0, (45, 20))     

    label2 = myfont.render("Puntos: " + str(points), 1, WHITE)
    pantalla.blit(label2, (650, 20))

    label3 = myfont.render('Vida:' + str(energy), 1, WHITE)
    pantalla.blit(label3, (385, 480))

carsOut = 0
def launch():
    
    global carsOut
    kind = random.randint(1,6)
    laneRand = random.randint(1,8)
    lane = 0
    ###Division de "carriles"
    if laneRand == 1:
        lane = 50
    elif laneRand == 2:
        lane = 142
    elif laneRand == 3:
        lane = 234  
    elif laneRand == 4:
        lane = 326
    elif laneRand == 5:
        lane = 418
    elif laneRand == 6:
        lane = 510
    elif laneRand == 7:
        lane = 602
    elif laneRand == 8:
        lane = 700
        
    if carsOut < 5:

        enemyCar1 = enemyCar(kind, lane)
        enemyCarGroup.add(enemyCar1)
        carsOut += 1
        
    else: 
        
        thing1 = thing(lane)
        thingGroup.add(thing1)
        carsOut = 0
        
##### choque

aux = False
def choque(value):
    
    global aux
    global energy

    if value == True and aux == False:
        energy -= 20
        sonidochoque.play()

        aux = True
        
    if value == False and aux == True:
        aux = False

    if energy < 1:
        saveGame()
        changescn("msg", text="Game Over!", btnfnc="menu")
        
##### Resetear el juego

def resetGame():
    global userName, energy, first, points, date, speed
    
    for i in enemyCarGroup:
        i.kill()
  
    for i in thingGroup:
        i.kill()
    
    userName = input_box1.text
    input_box1.text = "" # clear input_box
    input_box1.txt_surface = myfont.render("", True, input_box1.color) # clear input_box 

    input_box1.update
    energy = 100
    points = 0
    speed = 5
   
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")
        
########## ESCENAS ########## 

##### menu

menu_s = bool
def menu():
    
    global data, sortedData, menu_s, firts

    playBtn = button(RED, 300, 270, 200, 25, "JUGAR")
    scoresBtn = button(RED, 300, 300, 200, 25, "PUNTAJES")
    instBtn = button(RED, 300, 330, 200, 25, "INSTRUCCIONES")
    exitBtn = button(RED, 300, 360, 200, 25, "SALIR")
    creditosBtn = button(RED, 550, 450, 200, 25, "Creditos")
    backBtn = button(RED, 550, 450, 200, 25, "Atrás")


    with open(directory + "\\save\\" + "scores.txt", "r") as f:
        data = json.load(f)
    sortedData = sorted(data.items(), key=lambda x: x[1]['points'], reverse=True) # ordenar diccionario de diccionarios

    while menu_s:
    
        
        ##### RENDER #####
        
        pantalla.blit(menuBg, (0, 0))
        playBtn.draw(pantalla, (0,0,0))
        scoresBtn.draw(pantalla, (0,0,0))
        instBtn.draw(pantalla, (0,0,0))
        exitBtn.draw(pantalla, (0,0,0))
        creditosBtn.draw(pantalla,(0,0,0))

        if first == False:
        
            backBtn.draw(pantalla, (0,0,0))

        ##### EVENTOS #####
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() # toma la posicion del mouse
 
            if event.type == pygame.QUIT:
                menu_s = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                ############ control de los botones
                
                if playBtn.isOver(pos):         
                    changescn("enterName")
      
                if instBtn.isOver(pos):
                    changescn("instructions")

                if creditosBtn.isOver(pos):
                    changescn("creditos")    
                
                if exitBtn.isOver(pos):
                    menu_s = False
                    
                if backBtn.isOver(pos):
                    changescn("mainLoop")
                    
                if scoresBtn.isOver(pos):
                    changescn("scores")

                    
                    
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    menu_s = False
                    


        # Refrescar la Pantalla
        pygame.display.flip()
       
##### Puntaje
   
scores_s = bool
def scores():

    global data

    tag = "NICK".ljust(22) + "PUNTOS".center(6) + "FECHA".rjust(40)

    if len(sortedData) > 0:
        place0 = str(data[(sortedData[0][0])]["name"].ljust(20) + str(data[(sortedData[0][0])]["points"]).center(20) + str(sortedData[0][0]).rjust(35))
    else:
        place0 = "Empty"
        
    if len(sortedData) > 1:
        place1 = str(data[(sortedData[1][0])]["name"].ljust(20) + str(data[(sortedData[1][0])]["points"]).center(20) + str(sortedData[1][0]).rjust(35))
    else:
        place1 = "Empty"
        
    if len(sortedData) > 2:
        place2 = str(data[(sortedData[2][0])]["name"].ljust(20) + str(data[(sortedData[2][0])]["points"]).center(20) + str(sortedData[2][0]).rjust(35))
    else:
        place2 = "Empty"
        
    if len(sortedData) > 3:
        place3 = str(data[(sortedData[3][0])]["name"].ljust(20) + str(data[(sortedData[3][0])]["points"]).center(20) + str(sortedData[3][0]).rjust(35))
    else:
        place3 = "Empty"
        
    if len(sortedData) > 4:
        place4 = str(data[(sortedData[4][0])]["name"].ljust(20) + str(data[(sortedData[4][0])]["points"]).center(20) + str(sortedData[4][0]).rjust(35))
    else:
        place4 = "Empty"
        
    if len(sortedData) > 5:
        place5 = str(data[(sortedData[5][0])]["name"].ljust(20) + str(data[(sortedData[5][0])]["points"]).center(20) + str(sortedData[5][0]).rjust(35))
    else:
        place5 = "Empty"
        
    if len(sortedData) > 6:
        place6 = str(data[(sortedData[6][0])]["name"].ljust(20) + str(data[(sortedData[6][0])]["points"]).center(20) + str(sortedData[6][0]).rjust(35))
    else:
        place6 = "Empty"  

    if len(sortedData) > 7:
        place7 = str(data[(sortedData[7][0])]["name"].ljust(20) + str(data[(sortedData[7][0])]["points"]).center(20) + str(sortedData[7][0]).rjust(35))
    else:
        place7 = "Empty"
        
    if len(sortedData) > 8:
        place8 = str(data[(sortedData[8][0])]["name"].ljust(20) + str(data[(sortedData[8][0])]["points"]).center(20) + str(sortedData[8][0]).rjust(35))
    else:
        place8 = "Empty"
        
    if len(sortedData) > 9:
        place9 = str(data[(sortedData[9][0])]["name"].ljust(20) + str(data[(sortedData[9][0])]["points"]).center(20) + str(sortedData[9][0]).rjust(35))
    else:
        place9 = "Empty"

    scoresOk = button(BLACK, 150, 450, 200, 25, "Atrás")
    scoresClear = button(RED, 450, 450, 200, 25, "Limpiar Puntaje")
    scoresTitle = myfont.render("PUNTAJE - TOP10", 1, WHITE)
    tag2 = myfont.render(tag, 1, WHITE)
    score0 = myfont.render(place0, 1, WHITE)
    score1 = myfont.render(place1, 1, WHITE)
    score2 = myfont.render(place2, 1, WHITE)
    score3 = myfont.render(place3, 1, WHITE)
    score4 = myfont.render(place4, 1, WHITE)
    score5 = myfont.render(place5, 1, WHITE)
    score6 = myfont.render(place6, 1, WHITE)
    score7 = myfont.render(place7, 1, WHITE)
    score8 = myfont.render(place8, 1, WHITE)
    score9 = myfont.render(place9, 1, WHITE)

    global scores_s
    while scores_s:
        
           
        ##### RENDER #####
        
        pantalla.blit(fondo, (0, 0))
        
        pantalla.blit(scoresTitle, (300, 30))
        pantalla.blit(tag2, (150, 80))
        pantalla.blit(score0, (150, 120))
        pantalla.blit(score1, (150, 150))
        pantalla.blit(score2, (150, 180))
        pantalla.blit(score3, (150, 210))
        pantalla.blit(score4, (150, 240))
        pantalla.blit(score5, (150, 270))
        pantalla.blit(score6, (150, 300))
        pantalla.blit(score7, (150, 330))
        pantalla.blit(score8, (150, 360))
        pantalla.blit(score9, (150, 390))
        
        scoresOk.draw(pantalla, (0,0,0))
        scoresClear.draw(pantalla, (0,0,0))

        ##### EVENTS #####
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
 
            if event.type == pygame.QUIT:
                scores_s = False
                
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    changescn("menu")

            if event.type == pygame.MOUSEBUTTONDOWN:          
                if scoresOk.isOver(pos):
                    changescn("menu")
                    
                elif scoresClear.isOver(pos):
                    clearScores()

        # Refresh Screen
        pygame.display.flip()
        
def clearScores():
    
    global data, sortedData
    data.clear()
    sortedData.clear()
    
    with open(directory + "\\save\\" + "scores.txt", "w") as f:
        json.dump(data, f)

    changescn("scores")
    
creditos_s = bool
def creditos():
    
    global creditos_s
    
    backBtn = button(RED, 550, 450, 200, 25, "Atrás")

    labelCr0 = myfont.render("CREDITOS:", 1, WHITE)
    labelCr1 = myfont.render(" Juan Esteban Matallana Sanchez", 1, WHITE)
    labelCr2 = myfont.render(" Laura Natalia Lemus Ibañez", 1, WHITE)
    labelCr3 = myfont.render(" Karen Elizabeth Bravo Daza", 1, WHITE)
    labelCr4 = myfont.render(" Presentado a : Jhon Alexander Lopez Fajardo", 1, WHITE)
    
    while creditos_s:
            
        pantalla.blit(fondo, (0, 0))
        
        pantalla.blit(labelCr0, (360, 30))
        pantalla.blit(labelCr1, (200, 150))
        pantalla.blit(labelCr2, (220, 200))
        pantalla.blit(labelCr3, (220, 250))
        pantalla.blit(labelCr4, (130, 400))

        backBtn.draw(pantalla, (0,0,0))
        
        ##### ACTUALIZACION #####
        
        pygame.display.flip()
        
        ##### EVENTOS #####
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if backBtn.isOver(pos):
                    changescn("menu")
                    
            if event.type == pygame.QUIT:
                creditos_s = False
                
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: #Pressing the esc Key will quit the game
                    changescn("menu")

instructions_s = bool
def instructions():
    
    global instructions_s
    
    backBtn = button(RED, 550, 450, 200, 25, "Atrás")

    label0 = myfont.render("INSTRUCCIONES", 1, WHITE)
    label1 = myfont.render("Maneja la nave y no choques con los obstaculos", 1, WHITE)
    label2 = myfont.render("Usa A y D para mover la nave", 1, WHITE)
    label3 = myfont.render("Para disparar usa ESPACIO", 1, WHITE)
    label4 = myfont.render("Cada rayo te proporciona velocidad y te suma puntos", 1, WHITE)
    
    while instructions_s:
            
        pantalla.blit(fondo, (0, 0))
        
    
        
        pantalla.blit(label0, (330, 40))
        pantalla.blit(label1, (130, 150))
        pantalla.blit(label2, (225, 210))
        pantalla.blit(label3, (230, 270))
        pantalla.blit(label4, (110, 330))

  
        backBtn.draw(pantalla, (0,0,0))
        
        ##### ACTUALIZACION #####
        
        pygame.display.flip()
        
        ##### EVENTOS #####
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if backBtn.isOver(pos):
                    changescn("menu")
                    
            if event.type == pygame.QUIT:
                instructions_s = False
                
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: #ESC para salir del juego
                    changescn("menu")

##### Ingresar el Nick

enterName_s = False
def enterName():

    global enterName_s, user_text, first
    
    enterOkBtn = button(RED, 300, 350, 200, 25, "OK")
    enterBackBtn = button(RED, 550, 450, 200, 25, "Atrás")

    labelEnterName = myfont.render("Ingresa tu Nick:", 1, WHITE)

    while enterName_s:
        
        pantalla.blit(menuBg, (0, 0)) 
        enterOkBtn.draw(pantalla, (0,0,0)) 
        enterBackBtn.draw(pantalla, (0,0,0))

        pantalla.blit(labelEnterName, (300, 270))  
        
        input_box1.update()
        input_box1.draw(pantalla) 

        ##### EVENTOS #####
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
            input_box1.handle_event(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                ############ control de los botones
                
                if enterOkBtn.isOver(pos):
                    pantalla.blit(fondo, (0, 0))
                    if input_box1.text == "":
                        changescn("msg", text="Tienes que poner un Nick", btnfnc="enterName")
                            
                    else:
                        first = False
                        resetGame()
                        changescn("mainLoop")
         
                if enterBackBtn.isOver(pos):
                    changescn("menu")
            
            if event.type==pygame.QUIT:
                enterName_s = False
                
            if event.type == pygame.KEYDOWN:                
                if event.key==pygame.K_ESCAPE:
                    changescn("menu")
      
        ###########################

        # Refrescar Pantalla
        pygame.display.flip()

 
##### MAIN LOOP  ###################### AVERIGUAR PLEASE

count = 0
canShot = True
mainLoop_s = bool
def mainLoop():

    global mainLoop_s, first, count, size, speed, canShot
    
    Musica("engine")
    
    while mainLoop_s:
        
              
        ##### Reloj
        count += 1
        if count > 10:
            count = 0
            launch()

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                mainLoop_s = False

        ##### Controles
 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            playerKar.izquierda(5)
        if keys[pygame.K_RIGHT]:
            playerKar.derecha(5)  
            
        if keys[pygame.K_ESCAPE]:
            saveGame()
            Musica("main")
            changescn("menu")
        
        if keys[pygame.K_SPACE] and canShot == True:
            if count==1:
                pos_x,pos_y = playerKar.rect.x,playerKar.rect.y
                playerKar.shot(pos_x,pos_y,speed)
        
        lands_group.draw(pantalla)
        enemyCarGroup.draw(pantalla)
        kar_group.draw(pantalla)        
        thingGroup.draw(pantalla)

        informacion()
        
        lands01.play()
        lands02.play()
        
        ##### Funcionamiento del Juego

        for car in enemyCarGroup:
            car.moveForward()
            
        for thing in thingGroup:
           thing.moveForward() 

        ##### Coliciones #####
        
        # Enemigos
        car_collision_list = pygame.sprite.spritecollide(playerKar,enemyCarGroup,False,pygame.sprite.collide_mask)
        
        if car_collision_list:
            choque(True)
        else:
            choque(False)

        # Enemigos y Ayudas
        thing_collision = pygame.sprite.spritecollide(playerKar,thingGroup,True,pygame.sprite.collide_mask)
        
        if thing_collision:
            things()



        if len(playerKar.shotlist) > 0:
            for shot in playerKar.shotlist:
                shot.draw(pantalla)
                shot.updatePosition()
                canShot = False
                collision_shot = pygame.sprite.spritecollide(shot,enemyCarGroup,True,pygame.sprite.collide_mask)
                if collision_shot:
                    try:
                        playerKar.shotlist.remove(shot)
                        enemyCar1.kill()
                    except:
                        pass
                if shot.rect.y <= -40:
                    try:
                        playerKar.shotlist.remove(shot)
                    except:
                        pass
            canShot=True


        #Refrescar Pantalla
        
        pygame.display.flip()
        clock.tick(60) # Fotogramas por segundo FPS
        


#################################################################

Musica("main")
menu()
pygame.quit()
