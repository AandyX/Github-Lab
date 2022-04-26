#Graphics and sounds not made by me
#Learned pygame by ClearCode via youtube

import pygame, sprites, random

#pre_init reduces sound delay
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()

def main():
    screen_size = (640, 480) #640,480
    screen = pygame.display.set_mode(screen_size)    
    pygame.display.set_caption("Space Defender")
    

    while game_intro(screen):
        if not game_loop(screen):
            break
    

    pygame.mouse.set_visible(True)    
    pygame.quit()     
    
def pause(screen):

    
    background = screen
    dark = pygame.Surface((background.get_width()-200, background.get_height()), 
                          flags=pygame.SRCALPHA)
    dark.fill((50, 50, 50, 0))
    background.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)    
    paused = pygame.image.load("images/paused.png").convert_alpha()
    background.blit(
        paused, ((screen.get_width()-330)/2, screen.get_height()-300))
    screen.blit(background, (0, 0))
    resume_button = sprites.Button(
        ((screen.get_width()-200)/2, screen.get_height()-200), "Resume", (255,255,255))
    menu_button = sprites.Button(
        ((screen.get_width()-200)/2, screen.get_height()-150), "Main Menu", (255,255,255))

    buttons = [resume_button, menu_button]

    all_sprites = pygame.sprite.Group(buttons)

   
    select_sound = pygame.mixer.Sound("sounds/select.ogg")
    ok = pygame.mixer.Sound("sounds/ok.ogg")
    select_sound.set_volume(0.3)
    ok.set_volume(0.3)
    
   
    clock = pygame.time.Clock()
    keep_going = True
    FPS = 30
  
    selected = [buttons[0]]    
     
   
    while keep_going:
     
     
        clock.tick(FPS)
     
   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
         
                return 2
           
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if selected != [resume_button]:
                        select_sound.play()
                        selected = [buttons[(buttons.index(selected[0])-1)]]
                if event.key == pygame.K_s:
                    if selected != [menu_button]:
                        select_sound.play()
                        selected = [buttons[(buttons.index(selected[0])+1)]]
                if event.key == pygame.K_SPACE:
                    keep_going = False
                    ok.play()
                    if selected == [resume_button]:
                  
                        return 1
                    elif selected == [menu_button]:
        
                        return 0                     
                                    
        
        for select in selected:
            select.set_select()
     
 
        all_sprites.clear(screen, background)
        all_sprites.update()
        all_sprites.draw(screen)       
        pygame.display.flip()        
        pygame.display.flip()       


def game_over(screen):


    background = screen
 
    dark = pygame.Surface((background.get_width()-200, background.get_height()), 
                          flags=pygame.SRCALPHA)
    dark.fill((50, 50, 50, 0))
    background.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)      
    game_over = pygame.image.load("images/game_over.png").convert_alpha()
    background.blit(
        game_over, ((screen.get_width()-400)/2, screen.get_height()-300))
    screen.blit(background, (0, 0))
    restart_button = sprites.Button(
        ((screen.get_width()-200)/2, screen.get_height()-200), "Restart", 
        (255,255,255))
    menu_button = sprites.Button(
        ((screen.get_width()-200)/2, screen.get_height()-150), "Main Menu", 
        (255,255,255))

    buttons = [restart_button, menu_button]
    all_sprites = pygame.sprite.Group(buttons)


    select_sound = pygame.mixer.Sound("sounds/select.ogg")
    ok = pygame.mixer.Sound("sounds/ok.ogg")
    select_sound.set_volume(0.3)
    ok.set_volume(0.3)

    clock = pygame.time.Clock()
    keep_going = True
    FPS = 30

    selected = [buttons[0]]    
     

    while keep_going:
     
   
        clock.tick(FPS)
     
  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
         
                return 2
          
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if selected != [restart_button]:
                        select_sound.play()
                        selected = [buttons[(buttons.index(selected[0])-1)]]
                if event.key == pygame.K_s:
                    if selected != [menu_button]:
                        select_sound.play()
                        selected = [buttons[(buttons.index(selected[0])+1)]]
                if event.key == pygame.K_SPACE:
                    keep_going = False
                    ok.play()
                    if selected == [restart_button]:
                      
                        return 1
                    elif selected == [menu_button]:
                  
                        return 0                     
                                    
     
        for select in selected:
            select.set_select()
     
    
        all_sprites.clear(screen, background)
        all_sprites.update()
        all_sprites.draw(screen)       
        pygame.display.flip()        
        pygame.display.flip()     
    
def game_intro(screen):
    

    background = pygame.image.load("images/bg1.png").convert()
    screen.blit(background, (0, 0))
    start_button = sprites.Button(
        (screen.get_width()/2, screen.get_height()-130), "Start", (0,0,0))
 
    quit_button = sprites.Button(
        (screen.get_width()/2, screen.get_height()-50), "Quit", (0,0,0))
   
    buttons = [start_button, quit_button]
  
    all_sprites = pygame.sprite.Group(buttons)
    
    #Sounds
    #Background music
    pygame.mixer.music.load("sounds/main_menu.ogg")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    #Sound effects
    select_sound = pygame.mixer.Sound("sounds/select.ogg")
    ok = pygame.mixer.Sound("sounds/ok.ogg")
    reset = pygame.mixer.Sound("sounds/reset.ogg")
    select_sound.set_volume(0.3)
    ok.set_volume(0.3)
    reset.set_volume(0.3)
    
    
    clock = pygame.time.Clock()
    keep_going = True
    FPS = 30
  
    selected = [buttons[0]]    
     
      
    while keep_going:
     
      
        clock.tick(FPS)
     
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
 
                return 0

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if selected != [start_button]:
                        select_sound.play()
                        selected = [buttons[(buttons.index(selected[0])-1)]]
                if event.key == pygame.K_s:
                    if selected != [quit_button]:
                        select_sound.play()
                        selected = [buttons[(buttons.index(selected[0])+1)]]
           
                if event.key == pygame.K_SPACE:
                    if selected == [start_button]:
                        pygame.mixer.music.stop()
                        ok.play()
                
                        return 1
                    elif selected == [quit_button]:
                  
                        return 0
                                      
                                    
     
        for select in selected:
            select.set_select()
     
   
        all_sprites.clear(screen, background)
        all_sprites.update()
        all_sprites.draw(screen)       
        pygame.display.flip()        
        pygame.display.flip()   

def game_loop(screen):
 
    background = sprites.Background()
    
    pygame.mixer.music.load("sounds/background.ogg")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    
    #Sound effects.
    paused = pygame.mixer.Sound("sounds/pause.ogg")
    player_death = pygame.mixer.Sound("sounds/player_death.ogg")
    player_shoot = pygame.mixer.Sound("sounds/player_shoot.ogg")
    graze = pygame.mixer.Sound("sounds/graze.ogg")
    point = pygame.mixer.Sound("sounds/point.ogg")
    enemy_death = pygame.mixer.Sound("sounds/enemy_death.ogg")
    life_drop = pygame.mixer.Sound("sounds/get_life.ogg")
    bomb_drop = pygame.mixer.Sound("sounds/get_bomb.ogg")
    bombing = pygame.mixer.Sound("sounds/bomb.ogg")
    bullet_sounds = []
    for sound in range(1,6):
        bullet_sounds.append(pygame.mixer.Sound("sounds/bullet"+
            str(sound)+".ogg"))
    paused.set_volume(0.3)
    player_death.set_volume(0.3)
    player_shoot.set_volume(0.1)
    graze.set_volume(0.3)
    point.set_volume(0.3)
    enemy_death.set_volume(0.4)
    life_drop.set_volume(0.4)
    bomb_drop.set_volume(0.4)
    bombing.set_volume(0.4)
    for bullet_sound in bullet_sounds:
        bullet_sound.set_volume(0.1)
        

    player = sprites.Player(screen)
    hitbox = sprites.Hitbox(screen, player)
    
 
    score_tab = sprites.Score_tab(screen)
    
        

    spawners = []
    for spawner_type in range(2):
        spawners.append(sprites.Spawner(screen, spawner_type))
    
   
    low_sprites = pygame.sprite.OrderedUpdates(spawners, background,
        player, hitbox)
    enemy_sprites = pygame.sprite.OrderedUpdates()
    player_bullet_sprites = pygame.sprite.OrderedUpdates()
    enemy_bullet_sprites = pygame.sprite.OrderedUpdates()
    bomb_sprites = pygame.sprite.OrderedUpdates()
    animation_sprites = pygame.sprite.OrderedUpdates()
    drop_sprites = pygame.sprite.OrderedUpdates()
    top_sprites = pygame.sprite.OrderedUpdates(score_tab)
    
 
    all_sprites = pygame.sprite.OrderedUpdates(low_sprites, enemy_sprites, \
    player_bullet_sprites, enemy_bullet_sprites, animation_sprites, \
    drop_sprites, top_sprites)

    clock = pygame.time.Clock()
    keep_going = True
    half_mode = False
    difficulty = 0
    limits = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6)]
    boss_limit, common_limit = limits[difficulty] 
    common_enemies = 0
    boss_enemies = 0
    FPS = 30
    frames_passed = 0
    window_exit = 0
    restart = 0
    game_over_frames = 30
     
  
    pygame.mouse.set_visible(False)
 
    
    while keep_going:
     
      
        clock.tick(FPS)
     
      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
                window_exit = 1

         
            keys_pressed = pygame.key.get_pressed()
   
            if keys_pressed[pygame.K_ESCAPE]:
                paused.play()
                pygame.mixer.music.pause()
                option = pause(screen)
                if option == 0 or option == 2:
                    keep_going = False
                if option == 2:
                    window_exit = 1
                pygame.mixer.music.unpause()
      
            player.change_direction((0,0))
            if keys_pressed[pygame.K_a]:
                player.change_direction((-1,0))
            if keys_pressed[pygame.K_d]:
                player.change_direction((1,0))
            if keys_pressed[pygame.K_w]:
                player.change_direction((0,-1))
            if keys_pressed[pygame.K_s]:
                player.change_direction((0,1))
   
            if keys_pressed[pygame.K_SPACE] and not player.get_lock():
                player.shoot_mode(1)
            elif not keys_pressed[pygame.K_SPACE]:
                player.shoot_mode(0)
        
            if keys_pressed[pygame.K_e] and not bomb_sprites and not \
               player.get_lock() and score_tab.get_bombs():
                bombing.play()
                player.set_invincible(2)
                bomb_sprites.add(sprites.Bomb(player.get_center()))
                score_tab.bomb_used()
       
            if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT] and not player.get_lock():
                player.focus_mode(1)
                hitbox.set_visible(1)
            elif not keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
                player.focus_mode(0)
                hitbox.set_visible(0)
                
 
        frames_passed += 1
        
  
        if frames_passed == FPS*30:
            difficulty = 1
        elif frames_passed == FPS*60:
            difficulty = 2
        elif frames_passed == FPS*60*2:
            difficulty = 3
        elif frames_passed == FPS*60*5:
            difficulty = 4

       
        boss_limit, common_limit = limits[difficulty] 
        
     
        for spawner in spawners:
            spawner.set_rate(difficulty)
            
      
        if player.get_shoot() and not player.get_cool_rate() and not \
        player.get_lock():
            player_shoot.play()
            player_bullet_sprites.add(player.spawn_bullet())        

    
        if not player.get_invincible(): 
     
            for hit in pygame.sprite.spritecollide(
                hitbox, enemy_bullet_sprites.sprites(), False):
             
                if hitbox.rect.inflate(-14,-14).colliderect(hit) and \
                   not player.get_invincible():
    
                    animation_sprites.add(sprites.Explosion(
                        player.get_center(), 0))
                    player_death.play()
                    player.reset()
                    score_tab.life_loss()
                    
        
            for enemy in pygame.sprite.spritecollide(
                hitbox, enemy_sprites.sprites(), False):   
            
                if hitbox.rect.inflate(-14,-14).colliderect(enemy) and \
                   not player.get_invincible():
             
                    animation_sprites.add(sprites.Explosion(
                        player.get_center(), 0))
                    player_death.play()
                    player.reset()
                    score_tab.life_loss()
            
       
            for bullet in pygame.sprite.spritecollide(
                player, enemy_bullet_sprites.sprites(), False):  
                if player.rect.inflate(-6,-12).colliderect(bullet) and \
                   not player.get_invincible():
     
                    if not bullet.get_grazed():
                        graze.play()
                        score_tab.add_points(0)
                        bullet.set_grazed(1)
                    
     
        for drop in  pygame.sprite.spritecollide(
                player, drop_sprites.sprites(), False): 
            drop_type = drop.get_type()

            if drop_type <= 1:
                point.play()  
            elif drop_type == 2:
                life_drop.play()
            elif drop_type == 3:
                bomb_drop.play()
 
            score_tab.add_points((drop_type)+6)
            drop.kill()
                 
        
        for enemy in enemy_sprites.sprites():  
          
            for bullet in pygame.sprite.spritecollide(
                enemy, player_bullet_sprites.sprites(), False):
     
                animation_sprites.add(
                    sprites.Explosion(bullet.get_center(), 1))
                enemy.damaged(1)
                bullet.kill()
             
                if enemy.get_hp() <= 0 and not enemy.get_killed():
                   
                    enemy_death.play()
                   
                    enemy.set_killed()
                    animation_sprites.add(sprites.Explosion(
                        enemy.get_center(), 0))
                  
                    if enemy.get_type() <= 3:
                        drops = 4
                    elif enemy.get_type() > 3:
                        drops = 2
                
                    for drop in range(drops):
                        random_num = random.randrange(15)
                      
                        if random_num == 3 or random_num == 7 or \
                           random_num == 12:
                            drop_type = 1
                    
                        elif random_num == 5 and drops == 4:
                  
                            random_special = random.randrange(3)
                            if random_special == 1:
                                drop_type = 2
                            else:
                                drop_type = 3
                   
                        else:
                            drop_type = 0
                   
                        drop_sprites.add(sprites.Pick_up(
                            screen, enemy, drop_type))
              
                    score_tab.add_points(enemy.get_type())
           
            if not enemy.get_cool_rate() and not enemy.get_down_frames() \
               and not enemy.get_lock():
            
                bullet_sounds[enemy.get_type()-1].play()
          
                enemy_bullet_sprites.add(enemy.spawn_bullet(player)) 
        
      
        for bomb in bomb_sprites.sprites():
            for bullet in pygame.sprite.spritecollide(
                bomb, enemy_bullet_sprites.sprites(), False):
               
                if bomb.get_side() <= 140 or not bomb.rect.inflate(
                    -bomb.get_side()/4,-bomb.get_side()/4).colliderect(bullet):
               
                    animation_sprites.add(
                        sprites.Explosion(bullet.get_center(), 0))
                    bullet.kill()    
    
       
        common_enemies = 0
        boss_enemies = 0        
        for enemy in enemy_sprites.sprites():
            enemy_type = enemy.get_type()
            if enemy_type <= 3:
                boss_enemies += 1
            else:
                common_enemies += 1
    
     
        for spawner in spawners:
            if (spawner.get_type() == 1 and boss_enemies < boss_limit) or\
               (spawner.get_type() == 0 and common_enemies < common_limit):    
                spawner.set_lock(0)
                if not spawner.get_spawn_frames():
                    enemy_sprites.add(spawner.spawn_enemy())
            if spawner.get_type() == 1 and boss_enemies == boss_limit:
                spawner.set_lock(1)
            elif spawner.get_type() == 0 and common_enemies == common_limit:
                spawner.set_lock(1)  
                
        if not score_tab.get_lives():
         
            if game_over_frames > 1:
                game_over_frames -= 1
   
            else:
                pygame.mixer.music.stop()
                restart = game_over(screen)
                keep_going = False
                

        all_sprites = pygame.sprite.OrderedUpdates(low_sprites, enemy_sprites,
            player_bullet_sprites, enemy_bullet_sprites,
            animation_sprites, bomb_sprites, drop_sprites, top_sprites)
                         
 
        all_sprites.clear(screen, background.get_surface())
        all_sprites.update()
        all_sprites.draw(screen)       
        pygame.display.flip()  
    
   
    save_data = open("data/highscore.txt", 'w')
    save_data.write(str(score_tab.get_highscore()))
    save_data.close()
 
    if restart == 1:
      
        game_value = game_loop(screen)
        
        if game_value != 2:
            return game_value
        else:
         
            window_exit = 1

    elif restart == 2:
        window_exit = 1

 
    if not window_exit:       
        return 1
  
    else:
        return 0
     

main()    
