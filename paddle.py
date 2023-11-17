import pygame

class Paddle:

    def __init__(self, x, y, width=20, height=100):
        self.original_x = x
        self.original_y = y
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height
        self.reaching_max = 4

    def draw(self, win):
        pygame.draw.rect(
            win, (255, 255, 255), (self.x_pos, self.y_pos, self.width, self.height))
    
    def draw_Odd(self, win):
        points = [(self.x_pos, self.y_pos), (self.x_pos+30, self.y_pos), (self.x_pos+20, self.y_pos + 110), (self.x_pos + 10, self.y_pos + 110)]
        pygame.draw.polygon(
            win, (255, 255, 255), points)

    def move(self, up=True, velocity=0):
        if up:
            self.y_pos -= velocity
        else:
            self.y_pos += velocity

    def reset(self):
        self.x_pos = self.original_x
        self.y_pos = self.original_y