from paddle import Paddle
from ball import Ball
import pygame
import button
import random
import math

pygame.init()

class Game:
    """
    Configurations:
    - Ball: Movement/Trajectory (Straight or Sinusoidal)
    - ScreenSaver Mode

    """
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    def __init__(self):
        self.window_width = 1200
        self.window_height = 750

        paddle_size=[20,100]
        self.paddle_type = "normal"

        self.left_paddle = Paddle(
            10, self.window_height // 2 - paddle_size[1]// 2, paddle_size[0], paddle_size[1])
        self.right_paddle = Paddle(
            self.window_width - 10 - paddle_size[0], self.window_height // 2 - paddle_size[1]//2)
        self.left_speed = 8
        self.right_speed = 8

        #Set Ball Position and Size
        self.ball = Ball(self.window_width // 2, self.window_height // 2)

        #Set scores
        self.left_score = 0
        self.right_score = 0

        #Solo-Player
        self.left_solo_player = False
        self.right_solo_player = False

        #Game Status
        self.paused = False
        self.menu_state = "main"
        self.run = True
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

    def _draw_score(self):
        left_score_text = self.SCORE_FONT.render(
            f"{self.left_score}", 1, self.WHITE)
        right_score_text = self.SCORE_FONT.render(
            f"{self.right_score}", 1, self.WHITE)
        self.window.blit(left_score_text, (self.window_width //
                                           4 - left_score_text.get_width()//2, 20))
        self.window.blit(right_score_text, (self.window_width * (3/4) -
                                            right_score_text.get_width()//2, 20))

    def _draw_divider(self):
        for i in range(10, self.window_height, self.window_height//20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(
                self.window, self.WHITE, (self.window_width//2 - 5, i, 10, self.window_height//20))

    def _handle_collision(self):
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        #If ball hits the top or bottom
        if ball.y + ball.radius >= self.window_height:
            ball.y_vel *= -1
        elif ball.y - ball.radius <= 0:
            ball.y_vel *= -1

        if (self.left_solo_player == False and self.right_solo_player == False):
            #Ball moving from the right to left
            if ball.x_vel < 0:

                #If ball is in within the paddle height 
                if ball.y >= left_paddle.y_pos and ball.y <= left_paddle.y_pos + left_paddle.height:

                    #And if ball hits the left paddle 
                    if ball.x - ball.radius <= left_paddle.x_pos + left_paddle.width:
                        
                        #Ball direction change from left to right 
                        ball.x_vel *= -1

                        #Changing ball velocity
                        middle_y = left_paddle.y_pos + left_paddle.height/ 2
                        difference_in_y = middle_y - ball.y
                        reduction_factor = (left_paddle.height / 2) / ball.velocity
                        y_vel = difference_in_y / reduction_factor
                        ball.y_vel = -1 * y_vel
            
            #Ball moving from the left to right
            else:
                #If ball is in within the paddle height
                if ball.y >= right_paddle.y_pos and ball.y <= right_paddle.y_pos + right_paddle.height:
                    #And if ball hits the left paddle
                    if ball.x + ball.radius >= right_paddle.x_pos:

                        #Ball direction change from right to left 
                        ball.x_vel *= -1

                        #Changing ball velocity
                        middle_y = right_paddle.y_pos + right_paddle.height / 2
                        difference_in_y = middle_y - ball.y
                        reduction_factor = (right_paddle.height / 2) / ball.velocity
                        y_vel = difference_in_y / reduction_factor
                        ball.y_vel = -1 * y_vel
        
        #For left solo player
        elif(self.left_solo_player == True and self.right_solo_player == False):
            
            if ball.x_vel < 0:
                if ball.y >= left_paddle.y_pos and ball.y <= left_paddle.y_pos + left_paddle.height:
                    if ball.x - ball.radius <= left_paddle.x_pos + left_paddle.width:
                        ball.x_vel *= -1
                        middle_y = left_paddle.y_pos + left_paddle.height / 2
                        difference_in_y = middle_y - ball.y
                        reduction_factor = (left_paddle.height / 2) / ball.velocity
                        y_vel = difference_in_y / reduction_factor
                        ball.y_vel = -1 * y_vel

            else:
                if ball.x > self.window_width:
                    ball.x_vel *= -1
        
        #For right solo player
        elif(self.left_solo_player == False and self.right_solo_player == True):
            
            if ball.x_vel < 0:
                if self.ball.x < 0:
                    ball.x_vel *= -1

            else:
                if ball.y >= right_paddle.y_pos and ball.y <= right_paddle.y_pos + right_paddle.height:
                    if ball.x + ball.radius >= right_paddle.x_pos:
                        ball.x_vel *= -1
                        middle_y = right_paddle.y_pos + right_paddle.height / 2
                        difference_in_y = middle_y - ball.y
                        reduction_factor = (right_paddle.height / 2) / ball.velocity
                        y_vel = difference_in_y / reduction_factor
                        ball.y_vel = -1 * y_vel
    

    def draw(self, draw_score=True):
        if self.paused == False:
            self.window.fill(self.BLACK)

            self._draw_divider()

            if draw_score:
                self._draw_score()
            
            if (self.left_solo_player == False and self.right_solo_player == False):
                if self.paddle_type == "normal":
                    for paddle in [self.left_paddle, self.right_paddle]:
                        paddle.draw(self.window)
                if self.paddle_type == "odd":
                    for paddle in [self.left_paddle, self.right_paddle]:
                        paddle.draw_Odd(self.window)
            elif (self.left_solo_player == True and self.right_solo_player == False):
                if self.paddle_type == "normal":
                    self.left_paddle.draw(self.window)
                if self.paddle_type == "odd":
                    self.left_paddle.draw_Odd(self.window)
            elif (self.left_solo_player == False and self.right_solo_player == True):
                if self.paddle_type == "normal":
                    self.right_paddle.draw(self.window)
                if self.paddle_type == "odd":
                    self.right_paddle.draw_Odd(self.window)

            self.ball.draw(self.window)
        else:
            pass

    def move_paddle(self, left=True, up=True):
        left_velocity = self.left_speed
        right_velocity = self.right_speed

        #For the left paddle... 
        if left:

            #If up is true and paddle has reached the top, stop moving 
            if up and self.left_paddle.y_pos - self.left_paddle.reaching_max < 0:
                return False
            #If going down, and paddle has reached the bottome, stop moving 
            if not up and self.left_paddle.y_pos + self.left_paddle.height > self.window_height:
                return False
            self.left_paddle.move(up, left_velocity)
        
        #For the right paddle...
        else:
            if up and self.right_paddle.y_pos - self.right_paddle.reaching_max < 0:
                return False
            if not up and self.right_paddle.y_pos + self.right_paddle.height > self.window_height:
                return False
            self.right_paddle.move(up, right_velocity)

        return True

    def loop(self):

        if self.paused == False:
            self.ball.move()
            self._handle_collision()

            #Automated paddle movement (Rule-Based)
            if self.left_paddle.y_pos + self.left_paddle.height//2 > self.ball.y:
                self.move_paddle(left=True, up=True)
            if self.left_paddle.y_pos + self.left_paddle.height//2 < self.ball.y:
                self.move_paddle(left=True, up=False)
            if self.right_paddle.y_pos + self.right_paddle.height//2 > self.ball.y:
                self.move_paddle(left=False, up=True)
            if self.right_paddle.y_pos + self.right_paddle.height//2 < self.ball.y:
                self.move_paddle(left=False, up=False)
            
            #For two player game
            if (self.left_solo_player == False and self.right_solo_player == False):
                #Recording the score 
                if self.ball.x < 0:
                    self.ball.reset()
                    self.right_score += 1
                elif self.ball.x > self.window_width:
                    self.ball.reset()
                    self.left_score += 1
            #For left solo player
            elif (self.left_solo_player == True and self.right_solo_player == False):
                if self.ball.x < 0:
                    self.ball.reset()
                    self.right_score += 1
            #For right solo player
            elif (self.left_solo_player == False and self.right_solo_player == True):
                if self.ball.x > self.window_width:
                    self.ball.reset()
                    self.left_score += 1
        else:
            self.game_paused(self.window)
    
    def game_paused(self, screen):
        screen.fill(self.BLACK)

        if self.menu_state == "main":
            resume_button = button.Button(50, 150, self.window, "Resume")
            configure_button = button.Button(50, 300, self.window, "Configure")
            quit_button = button.Button(50, 450, self.window, "Quit")
            
            if resume_button.draw(screen):
                self.paused = False
            if configure_button.draw(screen):
                self.menu_state = "main_configure"
            if quit_button.draw(screen):
                self.run = False
        
        if self.menu_state == "main_configure":
            configureBall_button = button.Button(250, 120, self.window, "Ball")
            configurePaddle_button = button.Button(250, 240, self.window, "Paddle")
            configurePlayer_button = button.Button(250, 360, self.window, "Player")
            back_button = button.Button(250, 480, self.window, "Back")

            if configureBall_button.draw(screen):
                self.menu_state = "configure_ball"
            if configurePaddle_button.draw(screen):
                self.menu_state = "configure_paddle"    
            if configurePlayer_button.draw(screen):
                self.menu_state = "configure_player"
            if back_button.draw(screen):
                self.menu_state = "main"
        
        if self.menu_state == "configure_ball":
            ball_radius_button = button.Button(400, 120, self.window, "Ball Radius")
            ball_speed_button = button.Button(400, 200, self.window, "Ball Speed")
            ball_trace_button = button.Button(400, 280, self.window, "Ball Trace")
            ball_color_button = button.Button(400, 360, self.window, "Ball Color", 150, 50)
            back_button = button.Button(400, 440, self.window, "Back")
            if ball_radius_button.draw(screen):
                self.menu_state = "ball_radius"
            if ball_speed_button.draw(screen):
                self.menu_state = "ball_speed"
            if ball_trace_button.draw(screen):
                self.menu_state = "ball_trace"
            if ball_color_button.draw(screen):
                self.menu_state = "ball_color"
            if back_button.draw(screen):
                self.menu_state = "main_configure"
        
        if self.menu_state == "configure_paddle":
            paddle_shape_button = button.Button(400, 120, self.window, "Paddle Shape", 150, 50)
            paddle_height_button = button.Button(400, 200, self.window, "Paddle Height", 150, 50)
            paddle_width_button = button.Button(400, 280, self.window, "Paddle Width", 150, 50)
            left_speed_button = button.Button(400, 360, self.window, "Left Speed", 150, 50)
            right_speed_button = button.Button(400, 440, self.window, "Right Speed", 150, 50)
            back_button = button.Button(400, 520, self.window, "Back")
            if paddle_shape_button.draw(screen):
                self.menu_state = "paddle_shape"
            if paddle_height_button.draw(screen):
                self.menu_state = "paddle_height"
            if paddle_width_button.draw(screen):
                self.menu_state = "paddle_width"
            if left_speed_button.draw(screen):
                self.menu_state = "left_paddle_speed"
            if right_speed_button.draw(screen):
                self.menu_state = "right_paddle_speed"
            if back_button.draw(screen):
                self.menu_state = "main_configure"
        
        if self.menu_state == "paddle_shape":
            normal_paddle_shape_button = button.Button(550, 120, self.window, "Normal Shape", 150, 50)
            odd_paddle_shape_button = button.Button(550, 200, self.window, "Odd Shape", 150, 50)
            back_button = button.Button(550, 280, self.window, "Back")
            if normal_paddle_shape_button.draw(screen):
                self.paddle_type = "normal"
                self.menu_state = "paddle_size"
            if odd_paddle_shape_button.draw(screen):
                self.paddle_type = "odd"
                self.menu_state = "configure_paddle"
            if back_button.draw(screen):
                self.menu_state = "configure_paddle"

        if self.menu_state == "paddle_height":
            height_50_button = button.Button(550, 120, self.window, "50px")
            height_100_button = button.Button(550, 200, self.window, "100px")
            height_150_button = button.Button(550, 280, self.window, "150px")
            height_200_button = button.Button(550, 360, self.window, "200px")
            back_button = button.Button(550, 440, self.window, "Back")
            if height_50_button.draw(screen):
                self.left_paddle.height = 50
                self.right_paddle.height = 50
                self.menu_state = "configure_paddle"
            if height_100_button.draw(screen):
                self.left_paddle.height = 100
                self.right_paddle.height = 100
                self.menu_state = "configure_paddle"
            if height_150_button.draw(screen):
                self.left_paddle.height = 150
                self.right_paddle.height = 150
                self.menu_state = "configure_paddle"
            if height_200_button.draw(screen):
                self.left_paddle.height = 200
                self.right_paddle.height = 200
                self.menu_state = "configure_paddle"
            if back_button.draw(screen):
                self.menu_state = "configure_paddle"
        
        if self.menu_state == "paddle_width":
            width_20_button = button.Button(550, 120, self.window, "20px")
            width_40_button = button.Button(550, 200, self.window, "40px")
            width_60_button = button.Button(550, 280, self.window, "60px")
            width_80_button = button.Button(550, 360, self.window, "80px")
            back_button = button.Button(550, 440, self.window, "Back")
            if width_20_button.draw(screen):
                self.left_paddle.width = 20
                self.right_paddle.width = 20
                self.menu_state = "configure_paddle"
            if width_40_button.draw(screen):
                self.left_paddle.width = 40
                self.right_paddle.width = 40
                self.menu_state = "configure_paddle"
            if width_60_button.draw(screen):
                self.left_paddle.width = 60
                self.right_paddle.width = 60
                self.menu_state = "configure_paddle"
            if width_80_button.draw(screen):
                self.left_paddle.width = 80
                self.right_paddle.width = 80
                self.menu_state = "configure_paddle"
            if back_button.draw(screen):
                self.menu_state = "configure_paddle"
        
        if self.menu_state == "left_paddle_speed":
            pdSpeed_5_button = button.Button(550, 120, self.window, "5px/s")
            pdSpeed_8_button = button.Button(550, 200, self.window, "8px/s")
            pdSpeed_10_button = button.Button(550, 280, self.window, "10px/s")
            pdSpeed_13_button = button.Button(550, 360, self.window, "13px/s")
            back_button = button.Button(550, 440, self.window, "Back")
            if pdSpeed_5_button.draw(screen):
                self.left_speed = 5
                self.menu_state = "configure_paddle"
            if pdSpeed_8_button.draw(screen):
                self.left_speed = 8
                self.menu_state = "configure_paddle"
            if pdSpeed_10_button.draw(screen):
                self.left_speed = 10
                self.menu_state = "configure_paddle"
            if pdSpeed_13_button.draw(screen):
                self.left_speed = 13
                self.menu_state = "configure_paddle"
            if back_button.draw(screen):
                self.menu_state = "configure_paddle"

        if self.menu_state == "right_paddle_speed":
            pdSpeed_5_button = button.Button(550, 120, self.window, "5px/s")
            pdSpeed_8_button = button.Button(550, 200, self.window, "8px/s")
            pdSpeed_10_button = button.Button(550, 280, self.window, "10px/s")
            pdSpeed_13_button = button.Button(550, 360, self.window, "13px/s")
            back_button = button.Button(550, 440, self.window, "Back")
            if pdSpeed_5_button.draw(screen):
                self.right_speed = 5
                self.menu_state = "configure_paddle"
            if pdSpeed_8_button.draw(screen):
                self.right_speed = 8
                self.menu_state = "configure_paddle"
            if pdSpeed_10_button.draw(screen):
                self.right_speed = 10
                self.menu_state = "configure_paddle"
            if pdSpeed_13_button.draw(screen):
                self.right_speed = 13
                self.menu_state = "configure_paddle"
            if back_button.draw(screen):
                self.menu_state = "configure_paddle"
        
        if self.menu_state == "configure_player":
            two_player_button = button.Button(400, 120, self.window, "Two Player")
            left_player_button = button.Button(400, 200, self.window, "Solo Left Player", 200, 50)
            right_player_button = button.Button(400, 280, self.window, "Solo Right Player", 200, 50)
            back_button = button.Button(400, 360, self.window, "Back")
            if two_player_button.draw(screen):
                self.left_solo_player = False
                self.right_solo_player = False
                self.menu_state = "main_configure"
            if left_player_button.draw(screen):
                self.left_solo_player = True
                self.right_solo_player = False
                self.menu_state = "main_configure"
            if right_player_button.draw(screen):
                self.left_solo_player = False
                self.right_solo_player = True
                self.menu_state = "main_configure"
            if back_button.draw(screen):
                self.menu_state = "main_configure"
        
        if self.menu_state == "ball_radius":
            ball_radius_7_button = button.Button(550, 100, self.window, "7 Pixel")
            ball_radius_10_button = button.Button(550, 200, self.window, "10 Pixel")
            ball_radius_13_button = button.Button(550, 300, self.window, "13 Pixel")
            back_button = button.Button(550, 400, self.window, "Back")
            if ball_radius_7_button.draw(screen):
                self.ball.radius=7
                self.menu_state = "configure_ball"
            if ball_radius_10_button.draw(screen):
                self.ball.radius=10
                self.menu_state = "configure_ball"
            if ball_radius_13_button.draw(screen):
                self.ball.radius=13
                self.menu_state = "configure_ball"
            if back_button.draw(screen):
                self.menu_state = "configure"
        
        if self.menu_state == "ball_speed":
            ball_speed_10_button = button.Button(550, 100, self.window, "10px/s")
            ball_speed_15_button = button.Button(550, 200, self.window, "15px/s")
            ball_speed_20_button = button.Button(550, 300, self.window, "20px/s")
            ball_speed_25_button = button.Button(550, 400, self.window, "25px/s")
            back_button = button.Button(550, 500, self.window, "Back")
            if ball_speed_10_button.draw(screen):
                self.changeVelocity(10)
                self.menu_state = "configure_ball"
            if ball_speed_15_button.draw(screen):
                self.changeVelocity(15)
                self.menu_state = "configure_ball"
            if ball_speed_20_button.draw(screen):
                self.changeVelocity(20)
                self.menu_state = "configure_ball"
            if ball_speed_25_button.draw(screen):
                self.changeVelocity(25)
                self.menu_state = "configure_ball"
            if back_button.draw(screen):
                self.menu_state = "configure_ball"
        
        if self.menu_state == "ball_trace":
            ball_trace_ON_button = button.Button(550, 100, self.window, "On")
            ball_trace_OFF_button = button.Button(550, 200, self.window, "Off")
            back_button = button.Button(550, 400, self.window, "Back")
            if ball_trace_ON_button.draw(screen):
                self.ball.ball_trace = True
                self.menu_state = "configure_ball"
            if ball_trace_OFF_button.draw(screen):
                self.ball.ball_trace = False
                self.menu_state = "configure_ball"
            if back_button.draw(screen):
                self.menu_state = "configure"
        
        if self.menu_state == "ball_color":
            ball_color_white_button = button.Button(550, 100, self.window, "White")
            ball_color_red_button = button.Button(550, 200, self.window, "Red")
            ball_color_blue_button = button.Button(550, 300, self.window, "Blue")
            back_button = button.Button(550, 400, self.window, "Back")
            if ball_color_white_button.draw(screen):
                self.ball.color = self.ball.white_color
                self.menu_state = "configure_ball"
            if ball_color_red_button.draw(screen):
                self.ball.color = self.ball.red_color
                self.menu_state = "configure_ball"
            if ball_color_blue_button.draw(screen):
                self.ball.color = self.ball.blue_color
                self.menu_state = "configure_ball"
            if back_button.draw(screen):
                self.menu_state = "configure_ball"
    
    def changeVelocity(self, velocity):
        angle = self._get_random_angle(-30, 30, [0])
        pos = 1 if random.random() < 0.5 else -1
        self.ball.x_vel = pos * abs(math.cos(angle) * velocity)
        self.ball.y_vel = math.sin(angle) * velocity

    def _get_random_angle(self, min_angle, max_angle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))

        return angle
    
    def reset(self):
        """Resets the entire game."""
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.left_score = 0
        self.right_score = 0