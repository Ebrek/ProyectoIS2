import pygame
import sys
import Resources.pygame_textinput
 
pygame.init()

# Create TextInput-object
textinput = Resources.pygame_textinput.TextInput(text_color=(255,255,255))

screen = pygame.display.set_mode((1000, 200))
clock = pygame.time.Clock()

while True:
    screen.fill((0, 0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    # Feed it with events every frame
    textinput.update(events)
    # Blit its surface onto the screen
    screen.blit(textinput.get_surface(), (500, 100))

    pygame.display.update()
    clock.tick(30)