from convert import *
import pygame as p

screen = p.display.set_mode((800, 600))

class Gamestate:
    def __init__(self):
        self.board = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], 
                      ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], 
                      ['-', '-', '-', '-', '-', '-', '-', '-'], 
                      ['-', '-', '-', '-', '-', '-', '-', '-'], 
                      ['-', '-', '-', '-', '-', '-', '-', '-'], 
                      ['-', '-', '-', '-', '-', '-', '-', '-'], 
                      ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
                      ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
        
        #self.board = [['-', '-', '-', '-', 'k', '-', '-', 'r'],
         #             ['-', '-', '-', '-', '-', '-', '-', '-'],
          #            ['-', '-', '-', '-', '-', '-', '-', '-'],
           #           ['-', '-', '-', '-', '-', '-', '-', '-'],
            #          ['r', '-', '-', '-', '-', '-', '-', '-'],
             #         ['-', '-', '-', '-', '-', '-', '-', '-'],
              #        ['-', '-', '-', '-', '-', '-', '-', '-'],
               #       ['R', '-', '-', '-', 'K', '-', '-', 'r']]

        def __hash__(self):
            return hash(self.content)

        def __eq__(self, other):
            if not isinstance(other, Gamestate):
                return False
            return self.content == other.content
    
        # should default to false
        self.ep_flag_array = [[False] * 8 for _ in range(2)]
        # once true should remain true
        self.wking_moved_flag = False
        self.wlrook_moved_flag = False
        self.wrrook_moved_flag = False
        self.bking_moved_flag = False
        self.blrook_moved_flag = False
        self.brrook_moved_flag = False
        # should swap every creation
        self.white_to_move_flag = True

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