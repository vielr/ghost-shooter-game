import pygame as pg
import random
import math
from pygame import mixer
pg.init()

#SCREEN
game_screen = pg.display.set_mode((1280, 720))

#MUSIC
mixer.music.load("background.wav")
mixer.music.play(-10)

#BACKGROUND
background_image = pg.image.load("background.jpg")
background_image = pg.transform.smoothscale(background_image, (1280, 720))

#TITLE + ICON
pg.display.set_caption("game test")
game_icon = pg.image.load("game_icon.png")
pg.display.set_icon(game_icon)

#PLAYER
player_icon = pg.image.load("wizard.png")
player_icon = pg.transform.smoothscale(player_icon, (80, 80))
player_x = 590
player_y = 600
player_x_change = 0

def player(x,y):
    game_screen.blit(player_icon, (x, y))

#SCORE
score_value = 0
font = pg.font.Font("freesansbold.ttf", 32)

text_x = 10
text_y = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (38,20,42))
    game_screen.blit(score, (x, y))

#GM OVER
over_font = pg.font.Font("freesansbold.ttf", 64)

def game_over():
    game_over_text = over_font.render("GAME OVER", True, (38,20,42))
    game_screen.blit(game_over_text, (450, 200))
#GHOST
ghost_icon = []
ghost_x = []
ghost_y = []
ghost_x_change = []
ghost_y_change = []
ghosts = 6

for i in range(ghosts):
    ghost_icon.append(pg.image.load("ghost.png"))
    ghost_x.append(random.randint(0, 1200))
    ghost_y.append(random.randint(50, 100))
    ghost_x_change.append(0.5)
    ghost_y_change.append(70)

def ghost(x,y, i):
    game_screen.blit(ghost_icon[i], (x, y))

#MAGIC SPELL
spell_icon = pg.image.load("spell.png")
spell_icon = pg.transform.smoothscale(spell_icon, (80, 80))
spell_x = 0
spell_y = player_y
spell_x_change = 0
spell_y_change = 1.4
spell_state = "ready"

def use_spell(x,y):
    global spell_state
    spell_state = "use"
    game_screen.blit(spell_icon,(x+16, y+10)) 

#COLLISIONS
def isCollision(ghost_x, ghost_y, spell_x, spell_y):
    distance = math.sqrt(math.pow(ghost_x - spell_x, 2)) + (math.pow(ghost_y - spell_y, 2))
    if distance < 50:
        return True
    else:
        return False


#GAME LOOP
game_running = True
while game_running == True:

    #BACKGROUND IMAGE
    game_screen.fill((10, 0, 0))
    game_screen.blit(background_image,(0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                player_x_change = -1.2
            if event.key == pg.K_RIGHT:
                player_x_change = 1.2
            if event.key == pg.K_SPACE:
                if spell_state is "ready":
                    spell_Sound = mixer.Sound("fireball.wav")
                    spell_Sound.play()
                    spell_x = player_x
                    use_spell(spell_x, spell_y)


        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                player_x_change = 0

                
    #SCREEN WHILE GAME IS RUNNING
    #BOUNDARY CHECK
    player_x += player_x_change

    if player_x <= 0:
        player_x = 0
    if player_x >= 1200:
        player_x = 1200

    #GHOST MOVEMENT
    for i in range(ghosts):

        #GAME OVER
        if ghost_y[i] > 550:
            for j in range(ghosts):
                ghost_y[j] = 2000
            game_over()
            break

        ghost_x[i] += ghost_x_change[i]

        if ghost_x[i] <= 0:
            ghost_x_change[i] = 0.6
            ghost_y[i] += ghost_y_change[i]
        if ghost_x[i] >= 1218:
            ghost_x_change[i] = -0.6
            ghost_y[i] += ghost_y_change[i]

                #COLLISION
        collision = isCollision(ghost_x[i], ghost_y[i], spell_x, spell_y)
        if collision:
            explosion_Sound = mixer.Sound("explosion.mp3")
            explosion_Sound.play()
            spell_y = 480
            spell_state = "ready"
            score_value += 1  
            ghost_x[i] = random.randint(0, 1200)
            ghost_y[i] = random.randint(50, 100)

        ghost(ghost_x[i], ghost_y[i], i)

    #SPELL MOVEMENT
    if spell_y <= 0:
        spell_y = player_y
        spell_state = "ready"

    if spell_state is "use":
        use_spell(spell_x, spell_y)
        spell_y -= spell_y_change

    

    
    player(player_x, player_y)
    show_score(text_x, text_y)
    pg.display.update()