#no se usa


froggy_width = 64
#falta imagen de froggy
froggyImg =pygame.image.load('img/froggy.png')

def frog(x,y):
    gameDisplay.blit(froggyImg,(x,y))


def text_objects(text,font):
    textSurface = font.render(text,True, black)
    return textSurface,textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',60)
    TextSurf, TextRect = text_objects(text,largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf,TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()

def dead():
    message_display('Game Over')

def game_loop():

    x=(display_width*0.15)
    y=(display_height*0.8)

    x_change = 0

    gameExit = False

    while not gameExit:



    #movimiento
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5

                elif event.type ==pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key ==pygame.K_RIGHT:
                    x_change = 0

        x += x_change

        frog(x,y)

        #no salirse del cuadro
        if x > display_width - froggy_width  or x < 0:
            dead()



        pygame.display.update()





game_loop()
pygame.quit()
quit()
