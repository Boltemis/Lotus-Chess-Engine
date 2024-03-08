from utils import *
import pygame as p
screen = p.display.set_mode((800, 600))

class Button:
    def __init__(self, x, y, width, height, color, text):
        self.rect = p.Rect(x, y, width, height)
        self.color = color
        self.text = text

    def draw(self):
        p.draw.rect(screen, self.color, self.rect)
        font = p.font.Font(None, 36)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
    
        mouse_pos = p.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            p.draw.rect(screen, (255, 255, 255), self.rect, 2)

    def click(self):
        self.action()