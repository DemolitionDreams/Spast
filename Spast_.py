import random
import pygame
import math
from pygame.locals import *

FPS = 40                    # frame per secondo
POWERUPTIME = 7000          # durata del power up speed
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# inizializzazione
pygame.init()
pygame.mixer.init()
random.seed()

window = pygame.display.set_mode((0, 0), FULLSCREEN)    # crea finestra di gioco
pygame.display.set_caption("Spast")
clock = pygame.time.Clock()                             # gestisce FPS del gioco
pygame.mixer.music.load("Music/menuTrack.ogg")          # carica la colonna sonora

#fonts = pygame.font.match_font("arial")

def updateScreen():
    # la funzione aggiorna le costanti modifiche allo schermo
    pygame.display.flip()
    clock.tick(FPS)

def updateGameScreen(background):
    """ la funzione ricostruisce l'intera finestra di gioco.
            - background: l'immagine di sfondo dell'area di gioco
    """
    window.blit(title, ((20, 20)))
    window.blit(border, ((window.get_width() - 820) /1.2, (window.get_height() - 620) /1.5))
    border.fill(YELLOW)
    border.blit(screen, (10, 10))
    title.blit(titleImg, (0, 0))
    screen.blit(background, (0, 0))

def drawLives(surface, x, y, lives, image):
    """ la funzione disegna sull'area di gioco le vite del giocatore.
        - surface: la finestra dove disegnare le vite
        - x, y: la posizione in cui incollare il background
        - lives: le vite del giocatore
    """
    for i in range(lives):
        image = pygame.transform.smoothscale(image, (30, 30))
        imageRect = image.get_rect()
        imageRect.right = x
        imageRect.bottom = y - 50 * i
        surface.blit(image, imageRect)

def drawText(surface, text, size, x, y, color, flag):           
    """ la funzione disegna il testo.
            - surface: la superficie in cui disegnare il testo
            - text: il testo da inserire
            - size: la dimensione del testo
            - x, y: la posizione in cui incollare il testo
            - color: il colore del testo
            - flag: posto a True posiziona il nome del boss facendo riferimento ad un diverso angolo del rect
    """
    font = pygame.font.SysFont("Arial", size, bold = True)
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    if flag:
        textRect.topright = (x, y)     
    else:
        textRect.topleft = (x, y)
    surface.blit(textSurface, textRect)

def drawTextLikeSprite(surface, group, text, size, x, y, color):
    """ la funzione disegna il testo implementandolo come uno sprite.
            - surface: la superficie in cui disegnare il testo
            - group: il gruppo di sprite a cui aggiungere lo sprite del testo
            - text: il testo da inserire
            - size: la dimensione del testo
            - x, y: la posizione del rect dell'immagine
            - color: il colore del testo

            - textSprite: la funzione ritorna lo sprite contenente il testo inserito
    """
    font = pygame.font.SysFont("Arial", size, bold = True)
    textSurface = font.render(text, True, color)
    textSprite = pygame.sprite.Sprite(group)
    textSprite.image = textSurface
    textSprite.rect = textSurface.get_rect()
    textSprite.rect.topleft = (x, y)

    return textSprite

def drawShield(surface, x, y, percentage, image, flag, maxLife, name = "none"):     
    """ la funzione disegna il valore scelto utilizzando due rettangoli, outlineRect e fillRect.
            - surface: la superficie in cui disegnare la barra
            - x, y: la posizione in cui disegnare la barra
            - percentage: la quantità da rappresentare
            - flag: posto a True scrive il nome del boss accanto alla barra, mentre posto a False disegna l'immagine dello scudo accanto alla barra
            - name: il nome del boss
            - maxLife: la vita massima del boss
    """
    if flag:                
        drawText(surface, name, 36, x - 20, y - 12, WHITE, True)
    else:
        image = pygame.transform.scale(image, (20, 20))
        surface.blit(image, (x - 30, y))

    if percentage < 0:                                                     
        percentage = 0
    length = 200
    height = 20
    fill = (percentage / maxLife) * length
    outlineRect = pygame.Rect(x, y, length, height)
    fillRect = pygame.Rect(x, y, fill, height)
    pygame.draw.rect(surface, RED, fillRect)
    pygame.draw.rect(surface, WHITE, outlineRect, 4)

def updateDex(list, entry):
    """ la funzione aggiorna la lista dei nemici sconfitti.
            - list: la lista contenente i nomi dei nemici
            - entry: l'istanze del nemico
    """
    
    window.fill(BLACK)

    diz = {"Invader" : 0, "Roller" : 1, "Rare" : 2, "Gorgodusa" : 3, "Golem" : 7, "Bidramon" : 11}

    list[diz[entry]] = entry

    drawText(window, "EnemyDex", 32, 100, 200, WHITE, False)    
    for i in range(12):
        drawText(window, list[i], 32, 160, 250 + i*40, WHITE, False)
    '''
        if entry == "Invader":
            drawText(window, list[0], 32, 160, 300, BLACK, False)
            list[0] = entry
            drawText(window, list[0], 32, 160, 300, WHITE, False)
        elif entry == "Roller":
            drawText(window, list[1], 32, 160, 350, BLACK, False)
            list[1] = entry
            drawText(window, list[1], 32, 160, 350, WHITE, False)
        elif entry == "Rare":
            drawText(window, list[2], 32, 160, 400, BLACK, False)
            list[2] = entry
            drawText(window, list[2], 32, 160, 400, WHITE, False)
        elif entry == "Gorgodusa" or entry == "Golem" or entry == "Bidramon":
            drawText(window, list[3], 32, 160, 450, BLACK, False)
            list[3] = entry
            drawText(window, list[3], 32, 160, 450, WHITE, False)
    '''
def usePowerUp(power, player):
    """ la funzione rappresenta l'effetto dei diversi power up.
            - power: il power up ottenuto dal giocatore
            - player: il giocatore a cui applicare le modifiche 
    """
    if power.type == "shield":          # rafforza lo scudo del giocatore
        if player.shield < 100:
            player.shield += 20
            if player.shield > 100:
                player.shield = 100

    elif power.type == "speed":         # aumenta la velocità del giocatore
        player.velx = 10
        player.faster = True
        player.speedTimer = pygame.time.get_ticks()

    elif power.type == "extra":         # aggiunge una vita al giocatore se queste sono in numero minore di 5
        if player.lives < 5:
            player.lives += 1

    elif power.type == "toxic":         # toglie una vita al giocatore se queste sono in numero maggiore di 1
        if player.lives > 1:
            player.lives -= 1

    elif power.type == "newGun":        # aumenta il numero dei proiettili sparati contemporaneamente dal giocatore
        player.numBull += 1

class Player(pygame.sprite.Sprite):
    """ la classe rappresenta il giocatore come uno sprite e ne determina:
            - image: immagine
            - rect: il rect e la sua posizione nella finestra di gioco
            - vel: la velocità di movimento sull'asse x e y
            - shield: lo scudo a disposizione del giocatore. Shield == 0 comporta la perdita di una vita
            - lives: le vite a disposizione del giocatore. Lives == 0 comporta la perdita della partita
            - maxLife: la vita massima del giocatore
            - numBull: il numero di proiettili contemporaneamente utilizzabili dal giocatore
            - maxNumBull: il numero massimo di proiettili contemporaneamente presenti a schermo
            - numTwoShot, numThreeShot: il numero disponibile di spari rispettivamente con numBull == 2 e numBull >= 3
            - shootDelay, lastShot: determinano quando è possibile creare un nuovo proiettile
            - hidden, hideTimer: l'effetto di scomparsa/comparsa che segue la perdita di una vita del giocatore
            - faster, speedTimer: determinano il tempo di utilizzo del power up speed
    """
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.midbottom = (400, 580)
        self.velx = 5
        self.vely = 0
        self.shield = 100
        self.lives = 3
        self.maxLife = 100
        self.numBull = 1
        self.maxNumBull = 5
        self.numTwoShot = 0
        self.numThreeShot = 0
        self.shootDelay = 400
        self.lastShot = pygame.time.get_ticks()
        self.hidden = False
        self.hideTimer = pygame.time.get_ticks()
        self.faster = False
        self.speedTimer = pygame.time.get_ticks()

    def update(self):
        """ la funzione aggiorna costantemente il giocatore sullo schermo:
                - il primo controllo regola il power up newGun, diminuendo numBull dopo 5 colpi potenziati
                - il secondo controllo regola l'effetto scomparsa/comparsa del giocatore
                - il terzo controllo regola il power up speed riportando la velocità del giocatore al valore originale
                - il quarto controllo regola il movimento del giocatore in base al tasto premuto
        """
        if self.numBull == 3 and self.numThreeShot > 5:
            self.numBull = 1
            self.numThreeShot = 0
        elif self.numBull == 2 and self.numTwoShot > 5:
            self.numBull = 1
            self.numTwoShot = 0
        
        if self.hidden and pygame.time.get_ticks() - self.hideTimer > 500:
            self.hidden = False
            self.rect.topleft = (320, 500)
            self.shield = 100

        if self.faster and pygame.time.get_ticks() - self.speedTimer > POWERUPTIME:
            self.faster = False
            self.velx = 5

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a] or keystate[pygame.K_LEFT]:
            if self.velx > 0:
                self.velx *= -1
            self.rect.x += self.velx
        elif keystate[pygame.K_d] or keystate[pygame.K_RIGHT]:
            if self.velx < 0:
                self.velx *= -1
            self.rect.x += self.velx
        if self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()
        elif self.rect.left < 0:
            self.rect.left = 0
    
    def hide(self):
        # la funzione regola l'effetto scomparsa/comparsa del giocatore
        self.hidden = True
        self.hideTimer = pygame.time.get_ticks()
        self.rect.center = (2000, 2000)

    def shoot(self, image):
        """ la funzione regola la creazione del proiettile successivo a quello appena generato e il numero di proiettili creati contemporaneamente
        """
        global allSprites, bullets
        
        now = pygame.time.get_ticks()
        if now - self.lastShot > self.shootDelay:
            self.lastShot = now
            if self.numBull == 1:
                self.shootDelay = 400
                bullet = Bullet(self.rect.centerx, self.rect.top, image)
                allSprites.add(bullet)
                bullets.add(bullet)
            if self.numBull == 2:
                self.shootDelay = 200
                bullet1 = Bullet(self.rect.left, self.rect.centery, image)
                bullet2 = Bullet(self.rect.right, self.rect.centery, image)
                allSprites.add(bullet1)
                allSprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                self.numTwoShot += 1
            if self.numBull >= 3:
                self.shootDelay = 100
                bullet1 = Bullet(self.rect.left, self.rect.centery, image)
                bullet2 = Bullet(self.rect.right, self.rect.centery, image)
                bullet3 = Bullet(self.rect.centerx, self.rect.top, image)
                allSprites.add(bullet1)
                allSprites.add(bullet2)
                allSprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                self.numThreeShot += 1

class Obstacles(pygame.sprite.Sprite):
    """ la classe rappresenta l'ostacolo generato dal boss durante il livello e ne determina:
        - image: immagine
        - rect: il rect e la sua posizione nella finestra di gioco
        - vely: la velocità sull'asse y
        - owner: il boss che ha generato l'ostacolo
        - dangerous: posto a False impedisce all'ostacolo di danneggiare il giocatore
        - damage: il danno inflitto dall'ostacolo al giocatore
        - damageDelay: il tempo tra un danno e il successivo dell'ostacolo
        - timeToNewDamage: il tempo necessario all'ostacolo per danneggiare nuovamente il giocatore
        - flag: posto a True indica che l'ostacolo sta tornando indietro
    """
    def __init__(self, position, image, vely, damage, damageDelay, owner):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.centerx = position[0]
        self.rect.top = position[1]
        self.vely = vely
        self.owner = owner
        self.dangerous = True
        self.damage = damage
        self.damageDelay = damageDelay
        self.timeToNewDamage = pygame.time.get_ticks()
        self.back = False

    def update(self):
        # la funzione aggiorna costantemente la posizione dell'ostacolo sullo schermo, eliminandolo quando esce dallo schermo

        if self.owner == "Gorgodusa":
            if self.rect.y <= 300:
                self.back = True
                self.vely = 1
            elif self.rect.top > screen.get_height() + 20:
                self.kill()

            if not self.back:
                self.rect.y -= self.vely
            else:
                self.rect.y += self.vely

        elif self.owner == "Golem" or self.owner == "Bidramon":
            self.rect.y += self.vely
            if self.rect.top > screen.get_height():
                self.kill()
    
    def hitPlayer(self):
        # la funzione gestisce il danno inflitto dall'ostacolo al giocatore. Dopo averne inflitto uno, l'ostacolo perde tale capacità per alcuni secondi.

        self.dangerous = False
        now = pygame.time.get_ticks()

        if now - self.timeToNewDamage > self.damageDelay:
            self.dangerous = True

class Bullet(pygame.sprite.Sprite):
    """ la classe rappresenta il proiettile come uno sprite e ne determina:
            - image: immagine
            - rect: il rect e la sua posizione nella finestra di gioco
            - vel: la velocità del proiettile sull'asse y
            - bossDamage: il danno inflitto dal proiettile ai boss
    """
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.vely = -10
        self.bossDamage = 40

    def update(self):
        # la funzione aggiorna costantemente la posizione del proiettile sullo schermo, eliminandolo quando esce dal lato superiore
        self.rect.y += self.vely
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    """ la classe rappresenta il proiettile nemico come uno sprite e ne determina:
            - vel: la velocità del proiettile
            - damage: il danno inflitto dal proiettile al giocatore
    """
    def __init__(self, x, y, image, vel, direction, damage):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.direction = direction
        self.velx = vel[0]
        self.vely = vel[1]
        self.damage = damage
        self.sinAxis = x
        self.gap = random.randrange(50, 150, 10)
        
    def update(self):        
        # la funzione aggiorna costantemente la posizione del proiettile sullo schermo, eliminandolo quando esce dal lato superiore
        if self.direction == "center":
            self.rect.y += self.vely
        elif self.direction == "right":
            self.rect.x += self.velx
            self.rect.y += self.vely
        elif self.direction == "left":
            self.rect.x += self.velx
            self.rect.y += self.vely
        elif self.direction == "sin":
            self.rect.y += self.vely
            self.rect.x = self.sinAxis + math.sin(self.rect.y*math.pi*screen.get_height()/100/(screen.get_height() - self.image.get_height()))*self.gap
            if self.rect.x < self.sinAxis + 5 and self.rect.x > self.sinAxis - 5:
                self.gap = random.randrange(50, 150, 10)

        if self.rect.bottom < 0:
            self.kill()

class Power(pygame.sprite.Sprite):
    """ la classe rappresenta il power up come uno sprite e ne determina:
            - image: immagine
            - rect: il rect e la sua posizione nella finestra di gioco
            - vel: la velocità del proiettile sull'asse y
            - type: il tipo di power up tra quelli presenti nella lista
    """     
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["shield", "speed", "extra", "toxic", "newGun"])
        self.image = pygame.transform.smoothscale(poweImage[self.type], (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.vely = 5

    def update(self):
        # la funzione aggiorna costantemente la posizione del power up sullo schermo, eliminandolo quando esce dal lato inferiore
        self.rect.y += self.vely
        if self.rect.top > screen.get_height():
            self.kill()

class Enemy(pygame.sprite.Sprite):
    """ la classe rappresenta il prototipo del nemico che verrà esteso in diverse tipologie e ne determina:
            - image: immagine
            - rect: il rect e la sua posizione nella finestra di gioco
            - name: il nome
            - vel: la velocità di movimento sull'asse x e y
            - dex: posto a False indica un nemico non ancora eliminato e quindi non ancora scoperto
            - lives: le vite. Lives == 0 comporta la scomparsa del nemico
            - damage: il danno inflitto allo scudo del giocatore dal nemico
            - score: il punteggio ottenuto dal giocatore all'eliminazione del nemico  
    """
    def __init__(self, image, position, name, lives, damage, score):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.bottomleft = position
        self.name = "none"
        self.velx = 0
        self.vely = 0
        self.lives = lives
        self.damage = damage
        self.score = score

    def update(self):
        # la funzione aggiorna costantemente la posizione del nemico sullo schermo, eliminandolo quando esce dal lato inferiore
        self.rect.x += self.velx
        self.rect.y += self.vely
        if self.rect.top > screen.get_height():
            self.kill()

class Invader(Enemy):
    """ la classe estende Enemy e rappresenta il nemico 1 del primo livello, determinandone:
            - vel: la velocità di movimento sull'asse x e y
            - position: la posizione del punto di spawn
            - name: il nome

        eredita da Enemy:
            - lives
            - damage
            - score
    """
    def __init__(self, image, position, vel, lives, damage, score, name = "none"):
        super().__init__(image, position, name, lives, damage, score)
        self.velx = vel[0]
        self.vely = vel[1]
        self.name = "Invader"
                
class Rollers(Enemy):
    """ la classe estende Enemy e rappresenta il nemico 2 del primo livello, determinandone:
            - vel: la velocità di movimento sull'asse x e y
            - position: la posizione del punto di spawn
            - name: il nome
            - offset: utilizzato per controllare il rimbalzo sul lato sinistro e destro

        eredita da Enemy:
            - lives
            - damage
            - score
    """
    def __init__(self, image, position, vel, lives, damage, score, offset, name = "none"):
        super().__init__(image, position, name, lives, damage, score)
        self.velx = vel[0]
        self.vely = vel[1]
        self.name = "Roller"
        self.offset = offset

    def update(self):
        # la funzione aggiorna costantemente la posizione del nemico sullo schermo, eliminandolo quando esce dal lato inferiore. I rollers si muovono in diagonale, da un lato all'altro dell'area di gioco, rimbalzando su tali lati
        if self.velx > 0:
            self.rect.x += self.velx
            self.rect.y = self.rect.x/4 + self.offset
            if self.rect.right > screen.get_width():
                self.velx *= -1
                self.offset += 355
        elif self.velx < 0:
            self.rect.x += self.velx
            self.rect.y = -self.rect.x/4 + self.offset
            if self.rect.left < 0:
                self.velx *= -1

        if self.rect.top > screen.get_height():
            self.kill()

class Rare(Enemy):
    """ la classe estende Enemy e rappresenta il nemico speciale del primo livello, determinandone:
            - vel: la velocità di movimento sull'asse x e y dipendente dalla posizione del suo punto di spawn
            - position: la posizione del punto di spawn
            - name: il nome

        eredita da Enemy:
            - lives
            - score
    """
    def __init__(self, image, position, lives, score, damage = 0, name = "none"):
        super().__init__(image, position, name, damage, lives, score)
        self.velx = position[1] / 10
        self.name = "Rare"

    def update(self):
        # la funzione aggiorna costantemente la posizione del nemico sullo schermo, eliminandolo quando esce dal lato destro e sinistro
        self.rect.x += self.velx
        if self.rect.left > screen.get_width() + 100 or self.rect.right < -100:
            self.kill()

class Boss(pygame.sprite.Sprite):
    """ la classe rappresenta il prototipo del boss di fine livello come uno sprite e ne determina:
            - image: immagine
            - rect: il rect e la sua posizione nella finestra di gioco
            - lives: la vita a disposizione del boss. Lives == 0 comporta il superamento del livello
            - damage: il danno inflitto dal boss al giocatore
            - score: il punteggio ottenuto dal giocatore all'eliminazione del boss
            - vel: la velocità di movimento sull'asse x e y
            - dex: posto a False indica un nemico non ancora eliminato e quindi non ancora scoperto
            - split: utilizzato da Bidramon per indicare la sua divisione
            - lastShot: il tick in cui il boss lancia il proiettile
            - lastObstacles: il tick in cui il boss lancia l'attacco secondario
            - existsObstacles: posto a True indica la presenza su schermo di un ostacolo
            - obstaclesDelay: il tempo trascorso tra un attacco secondario e il successivo
    """
    def __init__(self, image, position, name, lives, maxLife, damage, score, vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.midleft = position
        self.name = name
        self.lives = lives
        self.maxLife = maxLife
        self.damage = damage
        self.score = score
        self.velx = vel[0]
        self.vely = vel[1]
        self.split = False
        self.lastShot = pygame.time.get_ticks()
        self.lastObstacles = pygame.time.get_ticks()
        self.existsObstacles = False
        self.obstaclesDelay = 50000
        
    def update(self):
        # la funzione aggiorna costantemente la posizione del boss sullo schermo
        self.rect.x += self.velx
        self.rect.y += self.vely

    def hit(self):
        # la funzione gestiscce la reazione del boss ai colpi subiti
        pass

    def shoot(self):
        # la funzione gestisce il principale attacco del boss
        pass

    def obstaclesAtk(self):
        # la funzione gestisce l'attacco con cui il boss crea un ostacolo ambientale
        pass

class Gorgodusa(Boss):
    def __init__(self, image, position, lives, maxLife, damage, score, vel, name = "Gorgodusa"):
        super().__init__(image, position, name, lives, maxLife, damage, score, vel)
        self.name = name
        self.centerImg = pygame.transform.scale(self.image, (20, 20))
        self.leftImg = pygame.transform.rotate(self.centerImg, 45)
        self.rightImg = pygame.transform.rotate(self.centerImg, -45)
        self.shotDelay = 1500
        self.resistence = 10
        
    def update(self):
        global obstacles

        now = pygame.time.get_ticks()

        if now - self.lastShot > self.shotDelay:
            self.shoot()
        elif now - self.lastObstacles > self.obstaclesDelay and len(obstacles) == 0:
            self.obstaclesAtk()

        self.rect.x += self.velx
        self.rect.y += self.vely

        if self.rect.left < 0:
            self.rect.left = 0
            self.velx *= -1
        elif self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()
            self.velx *= -1
    
    def hit(self):
        # soft damage
        if self.lives == 310:
            self.shotDelay = 1500
        
        # hard damage
        elif self.lives == 220:
            self.obstaclesAtk()
            self.obstaclesDelay = 4000
        
        # critical damage
        elif self.lives == 100:
            self.shotDelay = 800
            player.velx = 2

    def shoot(self):        
        self.lastShot = pygame.time.get_ticks()

        centerBullet = EnemyBullet(self.rect.centerx, self.rect.bottom, self.centerImg, (0, 3), "center", 20)
        eBullets.add(centerBullet)
        rightBullet = EnemyBullet(self.rect.centerx, self.rect.bottom, self.rightImg, (1, 3), "right", 20)
        eBullets.add(rightBullet)
        leftBullet = EnemyBullet(self.rect.centerx, self.rect.bottom, self.leftImg, (-1, 3), "left", 20)
        eBullets.add(leftBullet)

    def obstaclesAtk(self):
        self.lastObstacles = pygame.time.get_ticks()

        climbImg = pygame.image.load("Image/Obstacles/climbing.png").convert_alpha()
        climb1 = Obstacles((random.randrange(0, screen.get_width()), screen.get_height() - 100), climbImg, 10, 20, 2000, "Gorgodusa")
        obstacles.add(climb1)
        climb2 = Obstacles((random.randrange(0, screen.get_width()), screen.get_height() - 100), climbImg, 10, 20, 2000, "Gorgodusa")
        obstacles.add(climb2)

class Golem(Boss):
    def __init__(self, image, position, lives, maxLife, damage, score, vel, name = "Golem"):
        super().__init__(image, position, name, lives, maxLife, damage, score, vel)
        self.name = name
        self.position = position
        self.set = self.position[1]
        self.inversion = 1
        self.right = True
        self.counter = 0        
        self.fall = 100
        self.molt = 2
        self.shotDelay = 1000
        self.resistence = 20
        self.numBull = 10
        self.rockImg = pygame.transform.scale(self.image, (20, 20))

    def update(self):
        global obstacles

        now = pygame.time.get_ticks()
        
        if now - self.lastShot > self.shotDelay:
            self.shoot()
        elif now - self.lastObstacles > self.obstaclesDelay and len(obstacles) == 0:
            self.obstaclesAtk()

        if self.rect.left < 0:
            self.rect.left = 0
            self.velx *= -1
            self.right = True
        elif self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()
            self.velx *= -1
            self.right = False

        self.rect.x += self.velx
        self.rect.y = self.set - self.molt * self.counter * self.inversion
        self.counter += self.velx

        if self.rect.y <= self.position[1] - 100:
            self.set = self.position[1] - 99
            if self.right:
                self.inversion = -1
            else:
                self.inversion = 1
            self.counter = 0
        elif self.rect.y >= self.position[1] + self.fall:
            self.set = self.position[1] + self.fall - 1
            if self.right:
                self.inversion = 1
            else:
                self.inversion = -1
            self.counter = 0
    
    def hit(self):

        # soft damage
        if self.lives == 400:
            self.numBull = 12

        # hard damage
        elif self.lives == 200:
            self.resistence = 30
            self.obstaclesAtk()
            self.obstaclesDelay = 5000
        
        # critical damage
        elif self.lives == 100:
            self.numBull = random.randrange(10, 16, 2)
            self.fall = 400
            self.molt = 4
    
    def shoot(self):
        global eBullets
        
        self.lastShot = pygame.time.get_ticks()
        self.shotDelay = 4000

        for i in range(self.numBull):
            rock = EnemyBullet(random.randrange(0, screen.get_width() - self.rockImg.get_width() + 1), -1, self.rockImg, (0, random.randrange(2, 6)), "center", 30)
            eBullets.add(rock)

    def obstaclesAtk(self):
        self.lastObstacles = pygame.time.get_ticks()

        meteorImg = pygame.image.load("Image/Obstacles/meteor.png").convert_alpha()
        meteor1 = Obstacles((random.randrange(0 + meteorImg.get_width(), screen.get_width() - meteorImg.get_width()), -meteorImg.get_height()), meteorImg, 5, 40, 1000, "Golem")
        obstacles.add(meteor1)

class Bidramon(Boss):
    def __init__(self, image, position, lives, maxLife, damage, score, vel, name = "Bidramon"):
        super().__init__(image, position, name, lives, maxLife, damage, score, vel)
        self.name = name
        self.position = position
        self.split = False
        self.shotDelay = 1500
        self.resistence = 20
        self.tornadoImg = pygame.transform.scale(self.image, (20, 20))

    def update(self):   
        now = pygame.time.get_ticks()

        if now - self.lastShot > self.shotDelay:
            self.shoot()
        elif now - self.lastObstacles > self.obstaclesDelay and len(obstacles) == 0:
            self.obstaclesAtk()

        if self.rect.left < 0 and self.velx < 0:
            self.rect.left = 0
            self.velx *= -1
        elif self.rect.right > screen.get_width() and self.velx > 0:
            self.rect.right = screen.get_width()
            self.velx *= -1

        self.rect.x += self.velx

        if self.velx > 0:
            self.rect.y = self.position[1] + math.sin(self.rect.x*math.pi*screen.get_width()/100/(screen.get_width() - self.image.get_width()))*50
        elif self.velx < 0:
            self.rect.y = self.position[1] - math.sin(self.rect.x*math.pi*screen.get_width()/100/(screen.get_width() - self.image.get_width()))*50
    
    def hit(self):

        # soft damage
        if self.lives == 500:
            self.shotDelay = 1400
        
        # medium damage
        elif self.lives == 400:
            self.shotDelay = 1200

        # hard damage
        elif self.lives == 300:
            self.obstaclesAtk()
            self.obstaclesDelay = 6000

        # critical damage
        elif self.lives == 200:
            self.kill()
            self.split = True
    
    def shoot(self):
        global eBullets
        
        self.lastShot = pygame.time.get_ticks()
        
        tornado = EnemyBullet(random.randrange(0, screen.get_width() - self.tornadoImg.get_width() + 1), self.rect.bottom, self.tornadoImg, (0, random.randrange(2, 8)), "sin", 30)
        eBullets.add(tornado)

    def obstaclesAtk(self):
        self.lastObstacles = pygame.time.get_ticks()

        iceImg = pygame.image.load("Image/Obstacles/ice.png").convert_alpha()
        space1 = 0
        spawnXList = [iceImg.get_width(), screen.get_width()/2, screen.get_width()]
        spawnX = random.choice(spawnXList)

        if spawnX == iceImg.get_width():
            spawnY = 1
        elif spawnX == screen.get_width():
            spawnY = -1
        elif spawnX == screen.get_width()/2:
            spawnYList = [-1, 1]
            spawnY = random.choice(spawnYList)

        for i in range(10):
            ice = Obstacles((spawnX + space1*spawnY, -100 -iceImg.get_height() - space1), iceImg, 3, 20, 2000, "Bidramon")
            obstacles.add(ice)
            space1 += 50
            
def saved(group, level, background):
    """ la funzione offre la possibilità di salvare in un file di testo i progressi ottenuti dal giocatore.
            - group: utilizzato per la funzione restart
            - level: il livello corrente che verrà riportato nel file di salvataggio
            - background: utilizzato dalla funzione updateGameScreen
    """       
    restart(group, player, True)
    updateGameScreen(background)
        
    drawText(window, "Save?", 32, 1020, 510, WHITE, False)
    yes = drawTextLikeSprite(window, text, "  Yes", 32, 1050, 570, WHITE)
    no = drawTextLikeSprite(window, text, "  No", 32, 1050, 620, WHITE)
    
    done = False
    while not done:                    # il ciclo avrà termine quando il giocatore avrà deciso se salvare o meno
                
        # ciclo degli eventi
        for ev in pygame.event.get():
            if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
                click = ev.pos
                if yes.rect.collidepoint(click):
                    level += 1
                    savedata = open("savedata.txt", "w")
                    savedata.write("Level: {}".format(level) + "\n" + "Score: {}".format(score))
                    savedata.close()
                elif no.rect.collidepoint(click):
                    level += 1
                win = False
                levels(level)

        group[4].draw(window)             # stampa nell'area di gioco i comandi di salvataggio
        updateScreen()

def restart(group, player, flag):
    """ la funzione reinizializza il livello permettendo così una nuova partita.
            - group: lista di group di sprites da svuotare
            - player: il giocatore da resettare riportando lives, shield e numBull ai valori iniziali
            - flag: posta a True indica il restart dopo il superamento di un livello
    """ 
    for list in group:
        for obj in list:
            if obj != player:
                obj.kill()
    
    player.velx = 5

    pygame.time.set_timer(USEREVENT + 1, 0)
    pygame.time.set_timer(USEREVENT + 2, 0)
    pygame.time.set_timer(USEREVENT + 3, 0)
    pygame.time.set_timer(USEREVENT + 4, 0)


    if not flag:
        player.lives = 3
        player.shield = 100
        player.numBull = 1

def showGOScreen(score, group, player, background):
    """ la funzione accede alla schermata di game over.
            - score: il punteggio raggiunto dal giocatore viene stampato nell'area di gioco
            - group, player: lista di group da svuotare
            - background: utilizzato dalla funzione updateGameScreen
    """  
    updateGameScreen(background)
    restart(group, player, False)

    drawText(window, "GAME OVER", 64, 660, 300, WHITE, False)
    drawText(window, "Premi un tasto per tornare al menu iniziale", 18, 670, 500, WHITE, False)
    drawText(window, "Score: {}".format(score), 48, 735, 400, WHITE, False)

    waiting = True
    while waiting:                      # il ciclo rimane in attesa della pressione di un tasto da parte del giocatore
        updateScreen()
        # ciclo degli eventi
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or ev.type == KEYDOWN and ev.key == K_ESCAPE:
                pygame.quit()
            if ev.type == pygame.KEYDOWN:
                waiting = False
                    
def mainMenu():
    """ la funzione accede al menu iniziale
    """ 
    global level, score

    background = pygame.image.load("Image/Background/desert.jpg").convert()
    pygame.mixer.music.play(-1)                                                 # avvia la colonna sonora

    game = True
    while game:

        # ciclo degli eventi
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or ev.type == KEYDOWN and ev.key == K_ESCAPE:
                pygame.quit()

            elif ev.type == MOUSEBUTTONDOWN and ev.button == 1:
                click = ev.pos                                      # coordinate del puntatore
                if newGame.rect.collidepoint(click):
                    score = 0
                    level = 1
                    levels(level)
                elif toContinue.rect.collidepoint(click):
                    str = ""
                    savedata = open("savedata.txt", "r")            # accede al file di salvataggio per ottenere livello e score del giocatore
                    capture = savedata.readline()
                    for char in range(len(capture)):
                        if capture[char].isdecimal() == True:
                            str = str + capture[char]
                    level = int(str)
                    str = ""
                    capture = savedata.readline()
                    for char in range(len(capture)):
                        if capture[char].isdecimal() == True:
                            str = str + capture[char]
                    score = int(str)
                    savedata.close()
                    levels(level)

        updateScreen()
        updateGameScreen(background)
        
        newGame = drawTextLikeSprite(screen, text, "New Game", 32, 1000, 570, WHITE)
        toContinue = drawTextLikeSprite(screen, text, "Continue", 32, 1000, 620, WHITE)
        text.draw(window)

def levels(level):

    global score
   
    window.fill(BLACK)
    pygame.display.flip()

    bulletImg = pygame.image.load("Image/Player/bullet.png").convert_alpha()
    ciao = pygame.image.load("Image/Enemies/enemyShip.png").convert_alpha()

    bossImg = pygame.image.load("Image/Boss/bear.png").convert_alpha()
    bossImg2 = pygame.image.load("Image/Boss/buffalo.png").convert_alpha()
    bossImg3 = pygame.image.load("Image/Boss/sloth.png").convert_alpha()

    win = None
    enemy1 = None
    enemy2 = None
    spEnemy = None
    boss = None
    bossImg = None
    done = False        # regola il ciclo di gioco
    existsBoss = False

    
    drawText(window, "EnemyDex", 32, 100, 200, WHITE, False)
    for i in range(12):
        drawText(window, enemyDex[i], 32, 160, 250 + i*40, WHITE, False)


    # contengono le istruzioni necessarie a generare il livello corrente
    if level == 1:
        numEnemy1 = 0
        numEnemy2 = 0
        numSpEnemy = 0
        background = pygame.image.load("Image/Background/space.png").convert()
        bossImg = pygame.image.load("Image/Boss/bear.png").convert_alpha()
        enemy1Img = pygame.image.load("Image/Enemies/enemyShip.png").convert_alpha()
        enemy2Img = pygame.image.load("Image/Enemies/enemyRoll.png").convert_alpha()
        spEnemyImg = pygame.image.load("Image/Enemies/enemyShip.png").convert_alpha() 

        pygame.time.set_timer(USEREVENT + 1, random.randrange(400, 1500))
        pygame.time.set_timer(USEREVENT + 5, random.randrange(15000, 25000))
    
    elif level == 2:
        numEnemy1 = 0
        numEnemy2 = 0
        numSpEnemy = 0
        background = pygame.image.load("Image/Background/space.png").convert()
        bossImg = pygame.image.load("Image/Boss/bear.png").convert_alpha()
        enemy1Img = pygame.image.load("Image/Enemies/enemyShip.png").convert_alpha()
        enemy2Img = pygame.image.load("Image/Enemies/enemyRoll.png").convert_alpha()
        spEnemyImg = pygame.image.load("Image/Enemies/enemyShip.png").convert_alpha()

        pygame.time.set_timer(USEREVENT + 1, random.randrange(400, 1500))

    elif level == 3:
        numEnemy1 = 0
        numEnemy2 = 0
        numSpEnemy = 0
        background = pygame.image.load("Image/Background/space.png").convert()
        bossImg = pygame.image.load("Image/Boss/bear.png").convert_alpha()
        enemy1Img = pygame.image.load("Image/Enemies/enemyShip.png").convert_alpha()
        enemy2Img = pygame.image.load("Image/Enemies/enemyRoll.png").convert_alpha()
        spEnemyImg = pygame.image.load("Image/Enemies/enemyShip.png").convert_alpha()

        pygame.time.set_timer(USEREVENT + 1, random.randrange(400, 1500))

    # ciclo di gioco
    while not done:
        # ciclo degli eventi
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or ev.type == KEYDOWN and ev.key == K_ESCAPE:
                pygame.quit()
            elif ev.type == pygame.KEYDOWN and ev.key == K_SPACE and len(bullets) < player.maxNumBull:
                player.shoot(bulletImg)
                
            # eventi dedicati alla generazione dei nemici in ogni livello
            elif ev.type == USEREVENT + 1:
                if level == 1:
                    if numEnemy1 < 10:
                        pygame.time.set_timer(USEREVENT + 1, random.randrange(700, 1000))
                        invader = Invader(enemy1Img, (random.randrange(0, screen.get_width() - 98 + 1), -1), (0, 4), 1, 10, 10)
                        allEnemies.add(invader)
                        numEnemy1 += 1
                
                    elif numEnemy1 == 10:
                        pygame.time.set_timer(USEREVENT + 1, 0)
                        pygame.time.set_timer(USEREVENT + 2, 1500)
                        numEnemy1 = 0

            elif ev.type == USEREVENT + 2:
                if level == 1:
                    if numEnemy2 < 14:
                        pygame.time.set_timer(USEREVENT + 2, random.randrange(2000, 3000))
                        rollers1 = Rollers(enemy2Img, (0, -1), (4, 0), 2, 20, 20, 0)
                        allEnemies.add(rollers1)
                        numEnemy2 += 1
                        rollers2 = Rollers(enemy2Img, (screen.get_width() - 98 + 1, -1), (4, 0), 2, 20, 20, -180)
                        allEnemies.add(rollers2)
                        numEnemy2 += 1
               
                    elif numEnemy2 == 14:
                        pygame.time.set_timer(USEREVENT + 2, 0)
                        pygame.time.set_timer(USEREVENT + 3, 8000)
                        numEnemy2 = 0

            elif ev.type == USEREVENT + 3:
                if level == 1:
                    if numEnemy1 < 10:
                        pygame.time.set_timer(USEREVENT + 3, random.randrange(900, 1200))
                        invader = Invader(enemy1Img, (random.randrange(0, screen.get_width() - 98 + 1), -1), (0, 4), 2, 30, 20)
                        allEnemies.add(invader)
                        numEnemy1 += 1
                
                    elif numEnemy1 == 10:
                        pygame.time.set_timer(USEREVENT + 3, 0)
                        pygame.time.set_timer(USEREVENT + 4, 7000)
           
            elif ev.type == USEREVENT + 4:
                if level == 1:
                    if not existsBoss:
                        boss = Gorgodusa(bossImg, (400, 75), 400, 400, 30, 150, (5, 0), "Gorgodusa")
                        bosses.add(boss)
                        existsBoss = True
                elif level == 2:
                    if not existsBoss:
                        boss = Golem(bossImg2, (400, 75), 500, 500, 30, 250, (3, 0), "Golem")
                        bosses.add(boss)
                        existsBoss = True
                elif level == 3:
                    if not existsBoss:
                        boss = Bidramon(bossImg3, (400, 75), 600, 600, 30, 400, (5, 0), "Bidramon")
                        bosses.add(boss)
                        existsBoss = True

            elif ev.type == USEREVENT + 5:
                if level == 1:
                    rare = Rare(pygame.image.load("Image/Enemies/enemyShip.png").convert_alpha(), (-1, random.randrange(ciao.get_height(), screen.get_width()/2, 10)), 1, 150)
                    allEnemies.add(rare)
                    pygame.time.set_timer(USEREVENT + 5, random.randrange(25000, 35000))

        # movimento e collisione dei nemici
        hits = pygame.sprite.groupcollide(allEnemies, bullets, False, True)
        for hit in hits:
            hit.lives -= 1
            if hit.lives <= 0:
                updateDex(enemyDex, hit.name)
                score += hit.score
                hit.kill()
                if random.random() > 0.1:
                    power = Power(hit.rect.center)
                    allSprites.add(power)
                    powers.add(power)

        hits = pygame.sprite.groupcollide(eBullets, bullets, False, True)
        for hit in hits:
            hit.kill()
        
        hits = pygame.sprite.spritecollide(player, allEnemies, False)
        for hit in hits:
            score += hit.score
            updateDex(enemyDex, hit.name)
            hit.kill()
            player.shield -= 20
            if player.shield <= 0:
                player.shield = 0
                player.lives -= 1
                if player.lives == 0:
                    done = True
                    win = False
                player.hide()

        hits = pygame.sprite.spritecollide(player, eBullets, False)
        for hit in hits:
            hit.kill()
            player.shield -= hit.damage
            if player.shield <= 0:
                player.shield = 0
                player.lives -= 1
                if player.lives == 0:
                    done = True
                    win = False
                player.hide()

        hits = pygame.sprite.spritecollide(player, powers, True)
        for hit in hits:
            usePowerUp(hit, player)
        
        hits = pygame.sprite.spritecollide(player, bosses, False)
        for hit in hits:
            player.shield -= hit.damage
            if player.shield <= 0:
                player.shield = 0
                player.lives -= 1
                if player.lives == 0:
                    done = True
                    win = False
                player.hide()

            hit.lives -= player.shield/2
            if hit.lives <= 0:
                hit.kill()
                done = True
                win = True

        hits = pygame.sprite.spritecollide(player, obstacles, False)
        for hit in hits:
            if hit.dangerous:
                hit.hitPlayer()
                player.shield -= hit.damage
                hit.timeToNewDamage = pygame.time.get_ticks()
                if player.shield <= 0:
                    player.shield = 0
                    player.lives -= 1
                    if player.lives == 0:
                        done = True
                        win = False
                    player.hide()

        pygame.sprite.groupcollide(bullets, obstacles, True, False)

        if existsBoss:
            space2 = 0
            if boss.split:
                bidramon1 = Bidramon(boss.image, (200, 75), 100, 100, 30, 200, (5, 0), "Bidramon1")
                bidramon1.resistence = 30
                bidramon1.shotDelay = 1000
                bosses.add(bidramon1)
                bidramon2 = Bidramon(boss.image, (600, 75), 100, 100, 30, 200, (5, 0), "Bidramon2")
                bidramon2.resistence = 30
                bidramon2.shotDelay = 1000
                bosses.add(bidramon2)

            for boss in bosses:
                hits = pygame.sprite.spritecollide(boss, bullets, True)
                for hit in hits:
                    boss.lives -= (hit.bossDamage - boss.resistence)
                    boss.hit()
                    if boss.lives <= 0:
                        score += boss.score
                        updateDex(enemyDex, boss.name)
                        boss.kill()
                        done = True
                        win = True
                
                drawShield(screen, 580, 40 + space2, boss.lives, pygame.image.load("Image/Enemies/enemyShip.png").convert_alpha(), True, boss.maxLife, boss.name)
                space2 += 50

        # aggiornamento schermo
        drawLives(screen, 780, 580, player.lives, playerImg)
        drawShield(screen, 40, 558, player.shield, pygame.image.load("Image/Player/shield.png").convert_alpha(), False, player.maxLife)
        drawText(screen, "Score: {}".format(score), 32, 50, 50, WHITE, False)
        allSprites.draw(screen)
        allEnemies.draw(screen)
        eBullets.draw(screen)
        bosses.draw(screen)
        obstacles.draw(screen)
        
        allSprites.update()
        allEnemies.update()
        obstacles.update()
        eBullets.update()
        bosses.update()
        updateGameScreen(background)
        updateScreen()

        if win == True:
            saved((allEnemies, allSprites, bosses, eBullets, text, obstacles), level, background)
        
        elif win == False:
            showGOScreen(score, (allEnemies, allSprites, eBullets, bosses, obstacles), player, background)

# SPAST

# risorse grafiche
titleImg = pygame.image.load("Image/Window/title.png").convert_alpha()      # titolo di gioco

playerImg = pygame.image.load("Image/Player/player.png").convert_alpha()

mainMenuImage = pygame.image.load("Image/Background/desert.jpg").convert()         # schermata del Main Menu

# risorse testuali
command = ["Controls:", "  D - Move to Right", "  A - Move to Left", "  SPACE - Fire!", "ESC - Quit"] # lista dei comandi di gioco
for i in range(5):
    drawText(window, command[i], 32, 20, 250 + i*50, WHITE, False)

enemyDex = ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"]
    
# variabili
level = 1                   # livello di gioco
score = 0                   # punteggio di gioco

# creazione della finestra di gioco    
screen = pygame.Surface((800, 600))     # area di gioco
border = pygame.Surface((820, 620))     # bordo
title = pygame.Surface((342, 128))      # area del titolo

# creazione dei contenitori per gli sprite
allSprites = pygame.sprite.Group()
allEnemies = pygame.sprite.Group()

text = pygame.sprite.Group()
bosses = pygame.sprite.Group()
powers = pygame.sprite.Group()
bullets = pygame.sprite.Group()
eBullets = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# creazione power up
poweImage = {}                                                                          
poweImage["speed"] = pygame.image.load("Image/Player/speed.png").convert_alpha()
poweImage["shield"] = pygame.image.load("Image/Player/shield.png").convert_alpha()
poweImage["extra"] = pygame.image.load("Image/Player/extraLife.png").convert_alpha()
poweImage["toxic"] = pygame.image.load("Image/Player/toxic.png").convert_alpha()
poweImage["newGun"] = pygame.image.load("Image/Player/newGun.png").convert_alpha()

# ciclo di gioco
updateGameScreen(mainMenuImage)

player = Player(playerImg)              # creazione giocatore
allSprites.add(player)

mainMenu()
