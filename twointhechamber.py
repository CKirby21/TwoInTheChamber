import pygame, sys
from pygame.locals import *

class Player():

    def __init__(self, startX, startY, velocity, bullet):
        self.X = startX
        self.Y = startY
        self.velocity = velocity
        self.startX = startX
        self.startY = startY
        self.rightPressed = False
        self.leftPressed = False
        self.upPressed = False
        self.downPressed = False
        self.shootPressed = False
        self.bullet = bullet
        self.wasShot = False

class Bullet():

    def __init__(self, startX, startY, velocity, size):
        self.X = startX
        self.Y = startY
        self.velocity = velocity
        self.directions = {"East":False, "West":False, "North":False, "South":False}
        self.airborne = False
        self.owned = True
        self.size = size
        

def MovePlayer(player):
    if player.rightPressed:
        player.X += player.velocity
    if player.leftPressed:
        player.X -= player.velocity
    if player.upPressed:
        player.Y -= player.velocity
    if player.downPressed:
        player.Y += player.velocity
    
    # Handles teleporting to the other side of screen
    if player.Y + PIXEL > WINDOW_HEIGHT:
        player.Y = 0
    if player.X + PIXEL > WINDOW_WIDTH:
        player.X = 0
    if player.Y < 0:
        player.Y = WINDOW_HEIGHT - PIXEL
    if player.X < 0:
        player.X = WINDOW_WIDTH - PIXEL
    
    # Bullet starts in center of player
    if player.bullet:
        player.bullet.Y = player.Y + ((PIXEL // 2) - (player.bullet.size // 2))
        player.bullet.X = player.X + ((PIXEL // 2) - (player.bullet.size // 2))
    
def ShootBullet(player):
    if not player.bullet:
        return    
    if player.shootPressed and any(x for x in player.bullet.directions.values()):
        player.bullet.airborne = True
        player.bullet.owned = False
        player.bullet = None   

def AimBullet(player):
    
    if not player.bullet:
        return    

    bullet = player.bullet
    if player.rightPressed or player.leftPressed or player.upPressed or player.downPressed:
    
        bullet.directions["East"] = True if player.rightPressed else False 
            
        bullet.directions["West"] = True if player.leftPressed else False 
    
        bullet.directions["North"] = True if player.upPressed else False
            
        bullet.directions["South"] = True if player.downPressed else False

    # If oposite directions are pressed, remove those directions
    if bullet.directions["North"] and bullet.directions["South"]:
        bullet.directions["North"] = False
        bullet.directions["South"] = False
    if bullet.directions["East"] and bullet.directions["West"]:
        bullet.directions["West"] = False
        bullet.directions["East"] = False
    
    # Starts the bullet from outside the player's body
    if bullet.directions["North"]: bullet.Y = player.Y - bullet.size      
    if bullet.directions["South"]: bullet.Y = player.Y + PIXEL
    if bullet.directions["West"]: bullet.X = player.X - bullet.size
    if bullet.directions["East"]: bullet.X = player.X + PIXEL 

    ShootBullet(player)

def MoveBullet(bullet):
    if bullet.airborne:
        if bullet.directions["East"]:
            bullet.X += bullet.velocity
        if bullet.directions["West"]:
            bullet.X -= bullet.velocity
        if bullet.directions["North"]:
            bullet.Y -= bullet.velocity
        if bullet.directions["South"]:
            bullet.Y += bullet.velocity
    
        # Makes bullet stop when hitting the edge
        if bullet.Y + bullet.size > WINDOW_HEIGHT:
            bullet.Y = WINDOW_HEIGHT - bullet.size
            bullet.airborne = False
        if bullet.X + bullet.size > WINDOW_WIDTH:
            bullet.X = WINDOW_HEIGHT - bullet.size
            bullet.airborne = False
        if bullet.Y < 0:
            bullet.Y = 0
            bullet.airborne = False
        if bullet.X < 0:
            bullet.X = 0
            bullet.airborne = False
    
def CollideWithBullet(player, bullet):
    if ((player.X + PIXEL) > bullet.X and player.X < (bullet.X + bullet.size) and
                    (player.Y + PIXEL) > bullet.Y and player.Y < (bullet.Y + bullet.size)):          
        if bullet.airborne:
            # Collision means death
            player.wasShot = True
            return True
        elif not bullet.airborne and not bullet.owned and not player.bullet:
            # Collision means pick up bullet
            player.bullet = bullet
            bullet.owned = True
            return False
    else:
        return False

def CenterText(string, centerX, centerY, color):
    text = FONT.render(string, True, color)
    textRect = text.get_rect()
    textRect.center = (centerX, centerY)
    return text, textRect

def ResetPlayer(player, bullet):
    bullet = Bullet(player.startX, player.startY, VELOCITY*3, PIXEL // 2)
    player = Player(player.startX, player.startY, VELOCITY, bullet)
    return player, bullet

def Main(velocity, time, pixel, screen):
    # Setup
    global WINDOW_WIDTH, WINDOW_HEIGHT, PIXEL, FONT, PLAYING, COUNTING, VELOCITY
    BACKGROUND = (255, 255, 255)
    RED = (255, 30, 70)
    BLUE = (10, 20, 200)
    GREEN = (50, 230, 40)
    GRAY = (211,211,211)
    BLACK = (0,0,0)
    BROWN = (175, 155, 96)
    WINDOW_WIDTH = int(screen)
    WINDOW_HEIGHT = int(screen)
    PIXEL = int(pixel)
    VELOCITY = int(velocity)
    TIME = int(time)
    pygame.init()
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    FONT = pygame.font.Font('freesansbold.ttf', WINDOW_WIDTH // 15)
    pygame.display.set_caption('Two in the Chamber')
            
    # Main game loop
    bullet1 = Bullet(PIXEL + (PIXEL // 2), PIXEL + PIXEL // 2, VELOCITY*2, PIXEL // 2)
    bullet2 = Bullet((WINDOW_WIDTH-2*PIXEL) // 2, (WINDOW_HEIGHT-2*PIXEL) // 2, VELOCITY*2, PIXEL // 2)
    player1 = Player(PIXEL, PIXEL, VELOCITY, bullet1)
    player2 = Player(WINDOW_WIDTH-2*PIXEL, WINDOW_HEIGHT-2*PIXEL, VELOCITY, bullet2)
    startTicks = pygame.time.get_ticks()
    PLAYING = True
    # COUNTING = True
    while True:
        
        CLOCK.tick(60)
        # Get inputs
        for event in pygame.event.get() :
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == K_d:
                        player1.rightPressed = True
                    if event.key == K_a:
                        player1.leftPressed = True
                    if event.key == K_w:
                        player1.upPressed = True
                    if event.key == K_s:
                        player1.downPressed = True
                    if event.key == K_LCTRL:
                        player1.shootPressed = True

                    if event.key == K_RIGHT:
                        player2.rightPressed = True
                    if event.key == K_LEFT:
                        player2.leftPressed = True
                    if event.key == K_UP:
                        player2.upPressed = True
                    if event.key == K_DOWN:
                        player2.downPressed = True
                    if event.key == K_RCTRL:
                        player2.shootPressed = True
                elif event.type == pygame.KEYUP:
                    if event.key == K_d:
                        player1.rightPressed = False
                    if event.key == K_a:
                        player1.leftPressed = False
                    if event.key == K_w:
                        player1.upPressed = False
                    if event.key == K_s:
                        player1.downPressed = False
                    if event.key == K_LCTRL:
                        player1.shootPressed = False

                    if event.key == K_RIGHT:
                        player2.rightPressed = False
                    if event.key == K_LEFT:
                        player2.leftPressed = False
                    if event.key == K_UP:
                        player2.upPressed = False
                    if event.key == K_DOWN:
                        player2.downPressed = False
                    if event.key == K_RCTRL:
                        player2.shootPressed = False
                    
            else:
                # Check for game reset
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player1, bullet1 = ResetPlayer(player1, bullet1)
                        player2, bullet2 = ResetPlayer(player2, bullet2)
                        # startTicks = pygame.time.get_ticks()
                        PLAYING = True
                        # COUNTING = True
                
        if PLAYING:
            # Process game 
            MovePlayer(player1)
            MovePlayer(player2)
            AimBullet(player1)
            AimBullet(player2)
            MoveBullet(bullet1)
            MoveBullet(bullet2)
            player1Rect = pygame.Rect(player1.X, player1.Y, PIXEL, PIXEL)
            player2Rect = pygame.Rect(player2.X, player2.Y, PIXEL, PIXEL)
            bullet1Rect = pygame.Rect(bullet1.X, bullet1.Y, bullet1.size, bullet1.size)
            bullet2Rect = pygame.Rect(bullet2.X, bullet2.Y, bullet2.size, bullet2.size)
            # Check for game over
            # seconds = TIME - ((pygame.time.get_ticks()-startTicks) / 1000)
            # secondsText, secondsTextRect = CenterText('{0:.3f}'.format(seconds), WINDOW_WIDTH // 2, 20, GREEN)
            # if seconds < 0:
            #     secondsText, secondsTextRect = CenterText('0.000', WINDOW_WIDTH // 2, 20, GREEN)
            #     COUNTING = False
            #     PLAYING = False
            if CollideWithBullet(player1, bullet2) or CollideWithBullet(player1, bullet1):
                PLAYING = False
            if CollideWithBullet(player2, bullet1) or CollideWithBullet(player2, bullet2):
                PLAYING = False

            # Render game
            WINDOW.fill(BACKGROUND)
            # WINDOW.blit(secondsText, secondsTextRect)
            pygame.draw.rect(WINDOW, RED, player1Rect)
            pygame.draw.rect(WINDOW, BLUE, player2Rect)
            pygame.draw.rect(WINDOW, BROWN, bullet1Rect)
            pygame.draw.rect(WINDOW, BROWN, bullet2Rect)


        else:
            # Process game over
            # if COUNTING: sentence = 'Player 1 has caught Player 2!'
            if player1.wasShot and player2.wasShot:
                verdict = "Tie!"
            elif player1.wasShot:
                verdict = "Player 2 wins!"
            elif player2.wasShot:
                verdict = "Player 1 wins!"
            text, textRect = CenterText(verdict, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, GREEN)

            # Render game over
            WINDOW.blit(text, textRect)

        pygame.display.update()

if __name__ == '__main__':
    Main(4, 8, 30, 600)

# # Start screen loop
    # starting = True
    # while starting:
    #     for event in pygame.event.get() :
    #         if event.type == QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             starting = False
    #     text, textRect = CenterText("Click anywhere to start!", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    #     WINDOW.fill(BACKGROUND)
    #     WINDOW.blit(text, textRect)
    #     pygame.display.update()
    