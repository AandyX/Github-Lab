import pygame, math, random

class Button(pygame.sprite.Sprite):
    #Used in main menu
    
    def __init__(self, xy_pos, message, colour):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.__message = message
        self.__font = pygame.font.Font("fonts/arcade.ttf", 25)
        self.__select = 0
        self.__colours = [colour, (255,99,71)]
        self.image = self.__font.render(message, 1, (self.__colours[self.__select]))
        self.rect = self.image.get_rect()
        self.rect.center = xy_pos
    
    def set_select(self):
        
        self.__select = 1
    
    def update(self):
        
        #Reset color of button
        self.image = self.__font.render(self.__message, 1, (self.__colours[self.__select]))
        
        self.__select = 0
        
class Player(pygame.sprite.Sprite):

    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        
        self.__temp = pygame.image.load("images/player.png").convert_alpha()

        self.image = pygame.image.load('images/player.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = ((screen.get_width()-200)/2, 
                            screen.get_height()- 2*self.rect.height)  
        self.__screen = screen
        self.__dx = 0
        self.__dy = 0
        self.__diagonal = 1
        self.__focus = 1
        self.__invincible_frames = 110
        self.__lock = 0
        self.__shoot = 0
        self.__cool_rate = 3
        self.__focus_cool_rate = 9
        self.__temp_cool_rate = self.__cool_rate
        self.__temp_invincible = 0
        
        self.reset()
      
    def change_direction(self, xy_change):
        
        if xy_change[0] != 0:
            self.__dx = xy_change[0]*8
        elif xy_change[1] != 0:
            self.__dy = xy_change[1]*8
        else:
            self.__dx = 0
            self.__dy = 0
        
        if self.__dx != 0 and self.__dy != 0:
            self.diagonal_mode(1)
        else:
            self.diagonal_mode(0)
        
    def diagonal_mode(self, mode):
    
        if mode:
            self.__diagonal = ((2.0**0.5)/2.0)
        else:
            self.__diagonal = 1
            
    def focus_mode(self, mode):
        '''SHIFT is used to toggle between different speeds and
        fire types.'''
        
        if mode:
            self.__focus = 1.75
        else:
            self.__focus = 1
    
    def shoot_mode(self, mode):   
    
        self.__shoot = mode

    def spawn_bullet(self):
        
        #If focused, shoot line of bullet
        if not self.__focus == 1:
            self.__temp_cool_rate = self.__cool_rate
            return Bullet(self.__screen, self, 0)
        #Unfocused shoots muti-bullets.
        else:
            self.__temp_cool_rate = self.__focus_cool_rate
            return [Bullet(self.__screen, self, 1, 60),
                    Bullet(self.__screen, self, 1, 75),
                    Bullet(self.__screen, self, 1, 90),
                    Bullet(self.__screen, self, 1, 105),
                    Bullet(self.__screen, self, 1, 120)]
        
    def reset(self):
        #Respawn
        
        self.rect.center = ((self.__screen.get_width()-200)/2,
                            self.__screen.get_height() + 4*self.rect.height)    
        
        self.__temp_invincible = self.__invincible_frames
        
        self.__shoot = 0
        self.__focus = 1
        
    def set_invincible(self, frames):

        self.__temp_invincible = frames
        
    def get_cool_rate(self):

        return self.__temp_cool_rate
    
    def get_invincible(self):

        return self.__temp_invincible
    
    def get_lock(self):

        return self.__lock
        
    def get_shoot(self):

        return self.__shoot
    
    def get_center(self):

        return self.rect.center
        
    def update(self):
        if self.__temp_invincible > 0:

            if self.__temp_invincible >= self.__invincible_frames-50:
                self.__lock = 1
                self.__dx, self.__dy = 0,0
              
                self.__dy = -5
        
            else:
                self.__lock = 0
            
          
            if not self.__lock and self.__dy == -5:
                self.__dy = 0
              
            

        if self.__temp_invincible > 0:
            self.__temp_invincible -= 1
            if self.__temp_invincible % 15 <= 6 and \
               self.__temp_invincible % 15 > 2:
                self.image = self.__temp               
                
        #Update sprite position using boundaries.
        if ((self.rect.left > 0) and (self.__dx < 0)) or\
           ((self.rect.right < self.__screen.get_width()-200) and\
            (self.__dx > 0)):
            self.rect.centerx += self.__dx/self.__focus*self.__diagonal
        if ((self.rect.top > 0) and (self.__dy < 0)) or\
                  ((self.rect.bottom < self.__screen.get_height()) and\
                   (self.__dy > 0)):
            self.rect.centery += self.__dy/self.__focus*self.__diagonal
            
        if self.__temp_cool_rate > 0 :
            self.__temp_cool_rate -= 1
        
class Hitbox(pygame.sprite.Sprite):
    
    def __init__(self, screen, player):
        pygame.sprite.Sprite.__init__(self)
        
        #Image loading
        self.__hitbox = pygame.image.load("images/player.png")\
            .convert_alpha()
        self.__temp = pygame.image.load("images/player.png").convert_alpha()
        
        #Instance value setting.
        self.image = self.__hitbox
        self.rect = self.image.get_rect()
        self.__player = player
        self.__screen = screen
    
    def position(self, player):
 
        self.rect.center = player.rect.center
        
    def set_visible(self, visible):
 
        if visible:
            self.image = self.__hitbox
        else:
            self.image = self.__temp

    def update(self):
        
        self.position(self.__player)
        
        if self.rect.top > self.__screen.get_height():
            self.set_visible(0)
        
        
class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, xy_position):

        pygame.sprite.Sprite.__init__(self)        
        
        self.__side = 20
        self.image = pygame.Surface((self.__side,self.__side))
        self.rect = self.image.get_rect()
        self.__start = xy_position
        self.rect.center = xy_position
        self.__finish_raidus = 700
        self.__expand = 30
        self.__width = 3
        
    def get_side(self):
        return self.__side

    def update(self):
        ''''Animate bomb'''
        
        if self.__side/2 < self.__finish_raidus:
            self.__side += self.__expand
            self.__width += 1
            
            self.image = pygame.Surface((self.__side,self.__side))
            
            self.image.set_colorkey((0,0,0))
            
            pygame.draw.circle(self.image, (255,255,255), (self.__side//2
                                , self.__side//2), self.__side//2, self.__width)
            
            self.rect = self.image.get_rect()
            self.rect.center = self.__start
            
        else:
            self.kill()
              
class Enemy(pygame.sprite.Sprite):
    '''Contains multiple enemies'''
    
    def __init__(self, screen, enemy_type = 1):
        pygame.sprite.Sprite.__init__(self)
     
        self.image = pygame.image.load("images/enemy" +str(enemy_type)+ ".png").convert_alpha()
        self.__down_frames = 0
        self.__active_frames = 0
        self.__cool_rate = 0
        self.__dx = 0
        self.__dy = 0
        self.__hp = 0
        self.__degs_change = 0     
        self.rect = self.image.get_rect()
        self.rect.center = (400-50*enemy_type, 340-50*enemy_type)
        self.__screen = screen        
        self.__target_degs = None
        self.__target_y = screen.get_height()+self.rect.height
        self.__enemy_type = enemy_type
        self.__lock = 0
        self.__killed  = 0
        
        if enemy_type == 1:
            self.__down_frames = 60
            self.__active_frames = 60
            self.__cool_rate = 5
            self.__hp = 35
        elif enemy_type == 2:
            self.__down_frames = 30
            self.__active_frames = 40
            self.__cool_rate = 10
            self.__hp = 40  
        elif enemy_type == 3:
            self.__down_frames = 0
            self.__active_frames = 12
            self.__cool_rate = 4
            self.__hp = 45
            self.__degs_change = 6
        elif enemy_type == 4:
            self.__down_frames = 60
            self.__active_frames = 15
            self.__cool_rate = 3
            self.__hp = 10 
        elif enemy_type == 5:
            self.__down_frames = 30
            self.__active_frames = 30
            self.__cool_rate = 15
            self.__hp = 15              
        
        self.setup()
        
        self.__temp_down_frames = self.__down_frames
        self.__temp_active_frames = self.__active_frames
        self.__temp_cool_rate = self.__cool_rate
        
    def setup(self):
        '''Decides 
        where the sprite spawns, and where it goes.'''

        x_pos = random.randrange(self.rect.width,
            self.__screen.get_width()-201-self.rect.width)
        y_pos = 0-self.rect.height
        self.rect.center = (x_pos, y_pos)
        
        if self.__enemy_type < 4:
            target_x = random.randrange(100, 
                self.__screen.get_width()-201-self.rect.width, 100)
            target_y = random.randrange(100, 
                self.__screen.get_height()-229, 50)
            

            degs = self.calc_degs(target_x,target_y)
            self.__dx = math.cos(math.radians(degs)) * 5
            self.__dy = -(math.sin(math.radians(degs)) * 5)   
            
            self.__target_y = target_y
            
            self.__lock = 1 
            
        elif self.__enemy_type >= 4:
            self.__dx = 1
            self.__dy = 2
            if x_pos > (self.__screen.get_width()-200)/2:
                self.__dx = -self.__dx
        
    def spawn_bullet(self, target):

        degs = self.calc_degs(target.rect.centerx, target.rect.centery) 
        

        if self.__enemy_type == 1:
            self.__target_degs = degs
            vary = random.randrange(-10, 26, 4)
            self.__target_degs += vary
            self.__temp_cool_rate = self.__cool_rate
            return Bullet(self.__screen, self, self.__enemy_type+1,
                          self.__target_degs) 
        
        elif self.__enemy_type == 2:
            if self.__target_degs == None:
                self.__target_degs = degs
                vary = random.randrange(-2, 12, 4)
                self.__target_degs += vary                 
            self.__temp_cool_rate = self.__cool_rate              
            return [Bullet(self.__screen, self, self.__enemy_type+1, 
                           self.__target_degs-50), 
                    Bullet(self.__screen, self, 
                           self.__enemy_type+1, self.__target_degs-25),
                    Bullet(self.__screen, self, self.__enemy_type+1,
                           self.__target_degs),
                    Bullet(self.__screen, self, self.__enemy_type+1,
                                               self.__target_degs+25),
                    Bullet(self.__screen, self, self.__enemy_type+1,
                                               self.__target_degs+55)]
        
        elif self.__enemy_type == 3:
            if self.__target_degs == None:
                self.__target_degs = 0
            factor = random.randrange(1,4,4)
            if self.__target_degs < 0 and self.__degs_change < 0:
                self.__degs_change = 9 * factor
            elif self.__target_degs > 180 and self.__degs_change > 0:
                self.__degs_change = -9 * factor
            self.__target_degs += self.__degs_change
            self.__temp_cool_rate = self.__cool_rate              
            return [Bullet(self.__screen, self, self.__enemy_type+1,
                           self.__target_degs),
                   Bullet(self.__screen, self, self.__enemy_type+1,
                          self.__target_degs+90),
                   Bullet(self.__screen, self, self.__enemy_type+1,
                          self.__target_degs+180),
                   Bullet(self.__screen, self, self.__enemy_type+1,
                          self.__target_degs+270)]
        
        elif self.__enemy_type == 4:
            self.__target_degs = degs
            vary = random.randrange(-16, 30, 2)
            self.__target_degs += vary                 
            self.__temp_cool_rate = self.__cool_rate              
            return Bullet(self.__screen, self, self.__enemy_type+1, 
                           self.__target_degs)     
        
        elif self.__enemy_type == 5:
            self.__target_degs = random.randrange(0, 360, 30)
            bullets = []
            for extra_degs in range(0, 360, 60):
                bullets.append(Bullet(self.__screen, self, self.__enemy_type+1, 
                    self.__target_degs+extra_degs))             
            self.__temp_cool_rate = self.__cool_rate     
            return bullets
            
    def calc_degs(self, target_x, target_y):

        delta_x = float(target_x - self.rect.centerx)
        delta_y = float(target_y - self.rect.centery)
        
        rads = math.atan2(-delta_y, delta_x)
        
        rads %= 2 * math.pi
        
        return math.degrees(rads)                
        
    def damaged(self, damage):

        self.__hp -= damage    
        
    def set_killed(self):

        self.__killed = 1
        
    def get_killed(self):
 
        return self.__killed    
            
    def get_cool_rate(self):

        return self.__temp_cool_rate
    
    def get_down_frames(self):

        return self.__temp_down_frames
    
    def get_lock(self):

        return self.__lock
        
    def get_hp(self):

        return self.__hp
    
    def get_center(self):

        return self.rect.center
    
    def get_type(self):

        return self.__enemy_type
    
    def update(self):

        if self.__killed or self.rect.top > self.__screen.get_height():
            self.kill()
        
        if self.__temp_cool_rate > 0 and self.__lock != 1:
            self.__temp_cool_rate -= 1
        
        if self.__temp_active_frames == 0 == self.__temp_down_frames:
            self.__temp_down_frames = self.__down_frames
            self.__temp_active_frames = self.__active_frames
            
 
            if self.__enemy_type == 2:
                self.__target_degs = None
   
        if self.__temp_down_frames > 0 and self.__lock != 1: 
            self.__temp_down_frames -= 1
        if self.__temp_active_frames > 0 and self.__temp_down_frames == 0:
            self.__temp_active_frames -= 1

        if self.rect.left <= 0 and self.__dx < 0:
            self.__dx = abs(self.__dx)
        elif self.rect.right >= self.__screen.get_width()-200 and self.__dx > 0:
            self.__dx = -self.__dx
            
        self.rect.centerx += self.__dx
        
        if not self.rect.centery >= self.__target_y:
            self.rect.centery += self.__dy
        else:
            self.__dx = 0
            self.__dy = 0
            self.__lock = 0
        
class Explosion(pygame.sprite.Sprite):
    
    def __init__(self, xy_position, explosion_type):
        pygame.sprite.Sprite.__init__(self)    
        
        self.__frames = []
        if explosion_type == 0:
            for num in range(4):
                self.__frames.append(pygame.image.load("images/death"
                                            +str(num)+".png").convert_alpha())
        elif explosion_type == 1:
            for num in range(3):
                self.__frames.append(pygame.image.load("images/burst"
                                            +str(num)+".png").convert_alpha())
                
        self.image = self.__frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = xy_position
        self.__frame_refresh = 1 
        self.__temp_refresh = self.__frame_refresh
        self.__index = 0
    
    def update(self):
 
        if self.__temp_refresh > 0:
            self.__temp_refresh -= 1

        else:
            if self.__index >= len(self.__frames)-1:
                self.kill()
            else:
                self.__index += 1
                self.image = self.__frames[self.__index]
            self.__temp_refresh = self.__frame_refresh
            
class Bullet(pygame.sprite.Sprite):

    
    def __init__(self, screen, shooter, shoot_type, degs = None):
   
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("images/bullet"
                                       +str(shoot_type)+".png").convert_alpha()
        
        self.rect = self.image.get_rect()
        self.rect.center = shooter.rect.center
        self.__screen = screen
        self.__dx = 0
        self.__dy = 0
        self.__grazed = 0
        self.__graze_frames = 10
        self.__shoot_type = shoot_type
        self.__temp_graze = self.__graze_frames
        
  
        if shoot_type == 0:
            self.__dy = -20
        elif shoot_type ==1:
            self.__dx = math.cos(math.radians(degs)) * 20
            self.__dy = -(math.sin(math.radians(degs)) * 20)            
        elif shoot_type == 2:
            self.__dx = math.cos(math.radians(degs)) * 6
            self.__dy = -(math.sin(math.radians(degs)) * 6)
        elif shoot_type ==3:         
            self.__dx = math.cos(math.radians(degs)) * 6
            self.__dy = -(math.sin(math.radians(degs)) * 6)    
        elif shoot_type ==4:
            self.__dx = math.cos(math.radians(degs)) * 6
            self.__dy = -(math.sin(math.radians(degs)) * 6)  
        elif shoot_type == 5:
            self.__dx = math.cos(math.radians(degs)) * 4
            self.__dy = -(math.sin(math.radians(degs)) * 4)           
        elif shoot_type == 6:
            self.__dx = math.cos(math.radians(degs)) * 4
            self.__dy = -(math.sin(math.radians(degs)) * 4)
            
    def set_grazed(self, mode):
 
        self.__grazed = mode
            
    def get_center(self):

        return self.rect.center
    
    def get_grazed(self):

        return self.__grazed
        
    def update(self):

        self.rect.centery += self.__dy  
        self.rect.centerx += self.__dx
        
        if self.__grazed == 1:
            self.__temp_graze -= 1
            if self.__temp_graze == 0:
                self.__grazed = 0
                self.__temp_graze = self.__graze_frames
            
        if (0 >= self.rect.bottom or self.rect.top >= 
            self.__screen.get_height()) or (0 >= self.rect.right or
                self.rect.left >= self.__screen.get_width()-200):
            
            self.kill()
            

class Spawner(pygame.sprite.Sprite):

    def __init__(self, screen, spawner_type):

            pygame.sprite.Sprite.__init__(self)
     
            self.image = pygame.Surface((0,0))
            self.rect = self.image.get_rect()
            self.__type = spawner_type
            self.__screen = screen
            self.__lock = 0
            self.__spawn_types = []
            
            if self.__type == 0:
                self.__spawn_frames = 150
                self.__spawn_range = [4, 6]
            elif self.__type == 1:
                self.__spawn_frames = 300
                self.__spawn_range = [1, 4]
                
            self.__temp_frames = self.__spawn_frames
    
    def spawn_enemy(self):
        '''Spawn enemy if appropriate.'''
        
        self.__temp_frames = self.__spawn_frames
        
        enemy_type = random.randrange(self.__spawn_range[0], 
                                      self.__spawn_range[1])
        return Enemy(self.__screen, enemy_type)       
  
    def set_lock(self, mode):

        self.__lock = mode
        
    def set_rate(self, difficulty):
        
        if self.__type == 0:
            self.__spawn_frames = 150 - (difficulty*15)
            if difficulty == 0 or difficulty == 1:
                self.__spawn_range = [4,5]
            elif difficulty == 2:
                self.__spawn_range = [4,6]
        elif self.__type == 1:
            self.__spawn_frames = 300 - (difficulty*30)    
            if difficulty == 0:
                self.__spawn_range = [1,2]
            elif difficulty == 1:
                self.__spawn_range = [1,3]
            elif difficulty == 3:
                self.__spawn_range = [1,4]
    
    def get_spawn_frames(self):
 
        return self.__temp_frames
    
    def get_type(self):

        return self.__type
    
    def update(self):
        
        if not self.__lock:
            if self.__temp_frames >= 0:
                self.__temp_frames -= 1
                
class Pick_up(pygame.sprite.Sprite):
    '''The pick up class is used to spawn points, live and bomb drops.'''
    
    def __init__(self, screen, enemy, drop_type):

            pygame.sprite.Sprite.__init__(self)
            
            self.__screen = screen
            self.__type = drop_type
            self.__speed_frames = 5
            self.__temp_speed = self.__speed_frames
            
  
            self.image = pygame.image.load("images/drop"
                +str(self.__type)+".png").convert_alpha()
            self.rect = self.image.get_rect()
            
  
            self.rect = self.image.get_rect()
            self.rect.center = enemy.rect.center
            

            self.__dx = random.randrange(-3,4)
            self.__dy = random.randrange(-2,3)            
            
    
    def get_type(self):

        return self.__type
    
    def update(self):

        if (self.rect.top >= self.__screen.get_height()):
            self.kill()        
        

        if self.__temp_speed == 0:

            if self.__dx != 0:
                self.__dx -= (self.__dx / abs(self.__dx))

            if self.__dy < 3:
                self.__dy += 1
            elif self.__dy > 3:
                self.__dy -= 1
                    
            self.__temp_speed = self.__speed_frames
            
        else:
            self.__temp_speed -= 1
            

        self.rect.centerx += self.__dx
        self.rect.centery += self.__dy
        
        
class Score_tab(pygame.sprite.Sprite):
    
    def __init__(self, screen):
        
        pygame.sprite.Sprite.__init__(self)
        
        try:
            load_data = open("data/highscore.txt", 'r')
            self.__highscore = int(load_data.read())
            load_data.close()            
        
        #If file error, just set highscore to 0.
        except IOError and ValueError: 
            self.__highscore = 0
            
        self.image = pygame.image.load("images/score_tab.png").convert()     

        self.__life_frames = []
        for frame in range(2):
            self.__life_frames.append(pygame.image.load(
                "images/life"+str(frame)+".png").convert_alpha())         

        self.__bomb_frames = []
        for frame in range(2):
            self.__bomb_frames.append(pygame.image.load(
                "images/bomb"+str(frame)+".png").convert_alpha())         
        
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()-self.rect.width/2,\
                            screen.get_height()/2)
        self.__screen = screen
        self.__font = pygame.font.Font("fonts/arcade.ttf", 25)
        self.__score = 0
        self.__scores = ["HIGHSCORE", ("%10s" %(str(self.__highscore))).replace(
            " ", "0"),
                        "SCORE",("%10s" %(str(self.__score))).replace(" ", "0")] 
        self.__score_labels = []
        self.__lives = 3 
        self.__bombs = 1
        self.__stats = ["LIVES", "BOMBS"]
        self.__stat_labels = []
        self.__score_colour = (255,255,255)
        self.__stat_colour = (255,255,255)
        self.__colour_frames = 15
        self.__temp_colour_frames = self.__colour_frames
        
    def add_points(self, point_type):
        
        if point_type == 0:
            self.__score += 1
        elif point_type == 1:
            self.__score += 30
        elif point_type == 2:
            self.__score += 35
        elif point_type == 3:
            self.__score += 50
        elif point_type == 4:
            self.__score += 10
        elif point_type == 5:
            self.__score += 15
        elif point_type == 6:
            self.__score += 5
        elif point_type == 7:
            self.__score += 10
        elif point_type == 8:
            if self.__lives < 3:
                self.__lives += 1
            else:
                self.__score += 100
        elif point_type == 9:
            if self.__bombs < 3:
                self.__bombs += 1
            else:
                self.__score += 50
            
    def life_loss(self):
  

        self.__lives -= 1   
        self.reset()
    
    def reset(self):
 
        if self.__lives != 0:
            self.__bombs = 1
    
    def bomb_used(self):
        self.__bombs -= 1     
            
    def get_highscore(self):

        return self.__highscore
    
    def get_lives(self):

        return self.__lives
    
    def get_bombs(self):

        return self.__bombs
            
    def update(self):
        
        self.__scores = ["HIGHSCORE", ("%10s" %(str(self.__highscore))).replace(
            " ", "0"),
                        "SCORE",("%10s" %(str(self.__score))).replace(" ", "0")]        
        
        self.__score_labels = []   
        self.__stat_labels = []  
        
        for score in self.__scores:
            label = self.__font.render(score, 1, (self.__score_colour)) 
            self.__score_labels.append(label)
            
        for stat in self.__stats:
            label = self.__font.render(stat, 1, (self.__stat_colour)) 
            self.__stat_labels.append(label)        
                       
        self.image = pygame.image.load("images/score_tab.png").convert()
        
        y_pos = -20
        for label_num in range(len(self.__score_labels)):
            if label_num %2 == 0:
                y_pos += 50
            else:
                y_pos += 25
            self.image.blit(self.__score_labels[label_num], (10,y_pos))   
        
        y_pos = 235
        for label_num in range(len(self.__stat_labels)):
            y_pos += 75          
            self.image.blit(self.__stat_labels[label_num], (10,y_pos))  
        
        x_pos = 0
        for num in range(1, 4):
            if self.__lives >= num: 
                self.image.blit(self.__life_frames[1], (10+x_pos, 345))
            else:
                self.image.blit(self.__life_frames[0], (10+x_pos, 345))
            x_pos += 40
        x_pos = 0
        for num in range(1, 4):
            if self.__bombs >= num: 
                self.image.blit(self.__bomb_frames[1], (10+x_pos, 420))
            else:
                self.image.blit(self.__bomb_frames[0], (10+x_pos, 420))
            x_pos += 40        
   
class Background(pygame.sprite.Sprite):

        
    def __init__(self):
 
        pygame.sprite.Sprite.__init__(self)
 
        self.image = pygame.Surface((640, 480))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (0,0)
        
        #Load image and initialize other instances.
        self.__background = pygame.image.load("images/bg1.png").convert()
        self.__background_y = -480
        self.__dy = 1
        
    def get_surface(self):

        return self.image
        
    def update(self):
 
 
        self.__background_y += self.__dy

        self.image.blit(self.__background, (0, self.__background_y))

        if self.__background_y >= 0:
            self.__background_y = -480
