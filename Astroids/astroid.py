import pygame
from pygame.draw import circle
from pygame.version import PygameVersion
import os
from random import randint


class Settings:
    window_width = 600    #fenster breite
    window_height = 800   #fenster höhe
    path_file = os.path.dirname(os.path.abspath(__file__)) #dateien pfad
    path_image = os.path.join(path_file, "images")  #bilder pfad
    fps = 60 #wie viele bilder in einer sekunde
    caption = "Space invader" # Titel
    score = 0  #score ist am anfang auf null sinnvollerweise
    nof_astroids= 10  # am anfang werden 10 asteroiden gespawnt
    leben = 3  # 3 leben am anfang 
    modus = "mask" 

class Background(object):  # kalsse background
    def __init__(self, filename="background03.png") -> None: # background bild auswählen
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))

    def draw(self, screen): #malt den background
        screen.blit(self.image, (0, 0))

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.height = 80
        self.width = 50
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, "spacecraft.png")).convert_alpha()
        self.image = self.image_orig
        self.image = pygame.transform.scale(self.image, (self.width, self.height)) #stellt die größe des sprites ein
        self.rect = self.image.get_rect()
        self.radius = self.rect.width //2
        #self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = 10
        self.rect.centery = 10
        self.rect.centerx = Settings.window_width / 2
        self.rect.bottom = Settings.window_height
        
        
        self.smoothstop_v()
        self.smoothstop_h()
        
    
    def update(self):
        self.rand()
        self.rect.move_ip((self.speed_h, self.speed_v))

        
    def rand(self):     #funktion sorgt dafür das der spieler den bildschrim nicht verlassen kann
        if self.rect.bottom + self.speed_v > Settings.window_height:
            self.smoothstop_v()
        if self.rect.right + self.speed_h > Settings.window_width:
            self.smoothstop_h()
        if self.rect.left + self.speed_h < 0:
            self.smoothstop_h()
        if self.rect.top + self.speed_v < 0:
            self.smoothstop_v()
            

   
        
    
    def place_at_start(self):  # plaziert den spieler am start
        self.rect.centerx = Settings.window_width / 2
        self.rect.bottom = Settings.window_height

    def draw(self, screen):
        
        screen.blit(self.image, self.rect)

    def smoothstop_v(self):   # stellt eine in welche richtung mit welcher geschwindigkeit 
        self.speed_v = 0

    def smoothstop_h(self):
        self.speed_h = 0


    def down(self):
        self.speed_v = 4
        
    def up(self):
        self.speed_v = -4

    def left(self):
        self.speed_h = -4

    def right(self):
        self.speed_h = 4

    




class Astroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, "asteroid.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image,(30, 50)) #passt dei größe des sprites an 
        self.rect = self.image.get_rect()
        self.rect.left = randint(0, Settings.window_width - 20)         
        self.rect.top = 0
        self.speed_v = randint( 1,3)  #stellt die geschwindigkeit random zwischen 1 und 3 ein
        self.score = 0
        self.centery = Settings.window_height// 2
        self.counterspeed = 0
        
    
    def update(self):
        if self.rect.bottom + self.speed_v > Settings.window_height:
            self.count_hit()
        self.rect.move_ip(0, self.speed_v)
        
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def count_hit(self):
        self.kill()
        Settings.score += 1
        if self.speed_v <= 10:
            self.counterspeed += 1

   

    

class Game(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "50,30"
        pygame.init()
        pygame.display.set_caption(Settings.caption)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.screen = pygame.display.set_mode((Settings.window_width,Settings.window_height))
        self.clock = pygame.time.Clock()
        self.running = False
        self.players = pygame.sprite.GroupSingle() # erstellt die einzel gruppe players
        
        self.player = Player()
        self.astroids = pygame.sprite.Group() # erstellt die gruppe astroids
        self.astroid = Astroid()
        

    def run(self):
        
        self.running = True
        self.start()
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()
            
            
    
            
        pygame.quit()

    def watch_for_events(self): #hier wird festgellegt was bei welchen tasten druck passiert
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_DOWN:
                    self.player.down()
                elif event.key == pygame.K_UP:
                    self.player.up()
                elif event.key == pygame.K_LEFT:
                    self.player.left()
                elif event.key== pygame.K_RIGHT:
                    self.player.right()
                
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.player.smoothstop_v()
                elif event.key == pygame.K_UP:
                    self.player.smoothstop_v()
                elif event.key == pygame.K_LEFT:
                    self.player.smoothstop_h()
                elif event.key == pygame.K_RIGHT:
                    self.player.smoothstop_h()
                
                
    
       
           
           


    

    
        

    def update(self):
        #self.collision()
        self.player.update()
        self.astroids.update()
        if len(self.astroids.sprites()) < 10:             
            self.astroids.add(Astroid())

    def draw(self): #erstellt die einzeln objekte auf dem bildschirm
            self.background.draw(self.screen)
            self.player.draw(self.screen)
            self.astroids.draw(self.screen)
            text_surface_score = self.font.render("score: {0}".format(Settings.score), True, (255, 0, 0))
            self.screen.blit(text_surface_score, dest=(10, 10))
            pygame.display.flip()

    def start(self):
        self.background = Background()
        self.spawn()
        
        for f in range(Settings.nof_astroids):  # wenn weniger als 10 asteroiden auf den bildschirm sind spawnt es mehr
            self.astroids.add(Astroid())

    def spawn(self):# spawnt den spieler 
        self.players.add(Player())
        self.player.place_at_start()

    def leben(self):
        if Settings.leben <= 0:
            self.tod()

    def tod(self):
        self.running = False


    def collision(self):  # sollte funktioniern tut es aber leider nicht weshalb ich es auf auskommentiert habe in def update
    
        self.player.hit = pygame.sprite.groupcollide(self.players, self.astroids, True, False, pygame.sprite.collide_mask)
        if self.player.hit:
            Settings.leben -=1
            self.spawn()
            if Settings.leben <= 0:
                self.tod()
    
            




  




if __name__ == "__main__":
    
    game = Game()
    game.run()