import pygame
from constants import *

# Pygame button creator
class Button:
    def __init__(self, x, y, width, height, color, text, action):
        """
        Creates a button with given specifications
        :param x: x coordinate of the button
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                   self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
# Define button actions
def speedx1_action():
    return 1

def speedx2_action():
    return 2

def speedx4_action():
    return 4

def speedx8_action():
    return 8

def get_buttons():
    button1 = Button(WIDTH + 50, HEIGHT - 40, 20, 20, WHITE, "x1", speedx1_action)
    button2 = Button(WIDTH + 80, HEIGHT - 40, 20, 20, WHITE, "x2", speedx2_action)
    button3 = Button(WIDTH + 110, HEIGHT - 40, 20, 20, WHITE, "x4", speedx4_action)
    button4 = Button(WIDTH + 140, HEIGHT - 40, 20, 20, WHITE, "x8", speedx8_action)
    buttons = [button1, button2, button3, button4]
    return buttons
