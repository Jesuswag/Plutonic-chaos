from pygame import *
from random import *
import time as tm
xwin = 800
ywin = 800
window = display.set_mode((xwin,ywin))

listaovni = ["ovni1.png","ovni2.png"]
fondo = transform.scale(image.load("fondo.png"),(xwin,ywin)).convert() #CONVERT MEJORA MUCHO EL RENDIMIENTO

bala = image.load("bala.png")
icono = image.load("ovni1.png")
display.set_icon(icono)
display.set_caption("Tercer Juego")

mixer.init()
disparo = mixer.Sound("Disparo.wav")
disparo2 = mixer.Sound("rayo.wav")
disparo2.set_volume(0.5)
explosion = mixer.Sound("explosion.wav")
explosion2 = mixer.Sound("muerte.wav")

class Atributos(sprite.Sprite):
    def __init__(self,x,y,w,h,imagen,velocity):
        sprite.Sprite.__init__(self)
        self.w = w
        self.h = h
        self.imagen = imagen
        self.image = transform.scale(image.load(imagen),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = velocity
        self.multiplier = 1
        self.derecha = True
        self.cont = 0
        self.cont2 = 0
    
class Personaje(Atributos):
    def update(self):
        keys = key.get_pressed()
        if keys[K_RIGHT]:
            self.rect.x += self.velocity * self.multiplier
        if keys[K_LEFT]:
            self.rect.x -= self.velocity *self.multiplier
    def disparo(self):
        if len(grupo_balas) <2: #solo hay 2 en pantalla a la vez
            mixer.Sound.play(disparo)
            bala = Proyectil(self.rect.x +28,self.rect.y +16 + 4,8,8,"bala.png",20)
            bala.add(grupo_balas)

class Enemigo(Atributos):
    def update(self):
        if self.rect.x > xwin-96 and self.derecha == True:
            self.rect.y += 64
            self.derecha = False
        if self.rect.x <32 and self.derecha == False:
            self.rect.y += 64
            self.derecha = True

        if self.derecha == True:
            self.rect.x += self.velocity * self.multiplier
        else:
            self.rect.x -= self.velocity * self.multiplier
        
        if self.rect.y > ywin/3:
            self.multiplier = 3
        if self.rect.y >ywin /2:
            self.multiplier = 4
        #Cambiar de imagen cutre
        self.image = transform.scale(image.load(listaovni[self.cont]),(self.w,self.h))
        self.cont2 += 1
        if self.cont2 > 13:
            self.cont = 0
        else:
            self.cont = 1
        if self.cont2 > 26:
            self.cont2 = 0
        
class Proyectil(Atributos):
    def update(self):
        global vivir
        self.rect.y -= self.velocity * self.multiplier
        if self.rect.y < 0 or self.rect.y > ywin:
            self.kill()
        #colisiones
        muerte_disparos = sprite.groupcollide(grupo_balas,grupo_rayos,True,True)
        muerte_jugador = sprite.groupcollide(grupo_ovni,grupo_pers,True,True)
        muerte_jugador2 = sprite.groupcollide(grupo_rayos,grupo_pers,True,True)
        muerte_ovni = sprite.groupcollide(grupo_balas,grupo_ovni,True,True)
        for i in muerte_ovni: #por si hay mas de una colision en un solo frame aunq no va muy bien
            mixer.Sound.play(explosion)
            ovni = Enemigo(randrange(32,704),-64,64,64,"ovni.png",7)
            tanque.cont += 1
        if len(muerte_jugador)>0 or len(muerte_jugador2)>0:
            mixer.Sound.play(explosion2)
            vivir = False

       
            
grupo_pers = sprite.Group()
grupo_balas = sprite.Group()
grupo_ovni = sprite.Group()
grupo_rayos = sprite.Group()

tanque = Personaje(300,710,64,64,"canon2.png",8)
tanque.add(grupo_pers)

def horda():
    #Que se ordenen bien los enemigos
    if len(grupo_ovni) < 10:
        ovni = Enemigo(randrange(32,704,10),-64,64,64,"ovni.png",10) #step 10 para separarlos
        grupo_ovni.add(ovni)
        for i in grupo_ovni:
            for j in grupo_ovni:
                if sprite.collide_rect(i,j) == True and i!=j:
                    i.kill()
 
def disparoenemigo():
    for i in grupo_ovni:
        if randrange(0,100) == 0:
            mixer.Sound.play(disparo2)
            rayo = Proyectil(i.rect.x+16,i.rect.y+65,8,8,"rayo.png",-25,)
            rayo.add(grupo_rayos)
    
font.init()
def puntospantalla(tamano):
    if tanque.cont >=10 and tanque.cont <100:
        tamano -= 200
    fuente = font.SysFont("consolas",tamano)
    puntuacion = Surface((xwin,ywin))
    puntuacion.fill((255,255,255))
    puntuacion.set_alpha(32)
    texto = fuente.render(str(tanque.cont),1,(38,205,205))
    if tanque.cont <10:
        puntuacion.blit(texto,Rect(xwin/6,0,xwin,ywin))
    else:
        puntuacion.blit(texto,Rect(0,0,xwin,ywin))
    window.blit(puntuacion,Rect(0,0,10,10))

clock = time.Clock() #es para los fps
vivir = True
run = True
while run:
    clock.tick(30) #irá a 30 fps
    print(clock)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and vivir:
                tanque.disparo()
    if vivir and tanque.cont <100:
        grupo_balas.draw(window)
        grupo_balas.update()
        grupo_rayos.draw(window)
        grupo_rayos.update()
        grupo_pers.draw(window)
        grupo_pers.update()
        grupo_ovni.draw(window)
        grupo_ovni.update()
        puntospantalla(900)
        disparoenemigo()
        horda()
        display.update()
        window.blit(fondo,(0,0))
    else:
    
        fuentefinal = font.SysFont("consolas",20)
        pantallafinal = Surface((xwin,ywin))
        pantallafinal.fill((0,0,0))
        if tanque.cont <100:
            textofinal = fuentefinal.render("Has muerto... Tu puntuación: " + str(tanque.cont)+" pts.",1,(255,255,255))
            pantallafinal.blit(textofinal,Rect(xwin-600,ywin/2,0,0))
        else:
            textofinal = fuentefinal.render("¡Has ganado!",1,(255,255,255))
            pantallafinal.blit(textofinal,Rect(xwin-600,ywin/2,0,0))
        window.blit(pantallafinal,(0,0))
        display.update()