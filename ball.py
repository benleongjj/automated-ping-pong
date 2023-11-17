import pygame
import math
import random


class Ball:
    white_color = (255, 255, 255)
    red_color = (255, 0, 0)
    blue_color = (0, 191, 255)

    def __init__(self, given_x, given_y):
        self.original_x = given_x
        self.original_y = given_y
        self.x = given_x
        self.y = given_y
        self.radius = 7
        self.velocity = 17
        self.color = self.white_color
        self.ball_movement = "normal"

        self.ball_trace = True
        self.ball_trace_data = []
        
        #Launched at random y-vel and x-vel  
        angle = self._get_random_angle(-30, 30, [0])
        pos = 1 if random.random() < 0.5 else -1
        self.x_vel = pos * abs(math.cos(angle) * self.velocity)
        self.y_vel = math.sin(angle) * self.velocity

    def _get_random_angle(self, min_angle, max_angle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))

        return angle

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

        if self.ball_trace == True:
            for i in range(len(self.ball_trace_data) - 1):
                pygame.draw.line(win, self.color, self.ball_trace_data[i], self.ball_trace_data[i + 1], 2)

    def move(self):
        if self.ball_movement == "normal":
            self.x += self.x_vel
            self.y += self.y_vel

        if self.ball_movement == "odd":
            self.x += self.x_vel
            self.y += self.y_vel

        #Ball Tracing 
        if self.ball_trace == True:
            ball_pos = [self.x, self.y]
            self.ball_trace_data.append(ball_pos[:])
            if len(self.ball_trace_data) > 10:
                self.ball_trace_data.pop(0)
        
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

        angle = self._get_random_angle(-30, 30, [0])
        y_vel = math.sin(angle) * self.velocity

        self.y_vel = y_vel
        self.x_vel *= -1
