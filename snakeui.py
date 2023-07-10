import random
import numpy as np
import pygame
pygame.init()
font = pygame.font.SysFont('arial', 25)

WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 10

class SnakeGame():

    def __init__(self,player=None,grid_size=100):
        self.grid_size = grid_size
        self.head = (self.grid_size//2, self.grid_size//2)
        self.snake_body = [(self.grid_size//2, self.grid_size//2)]
        self.food = None
        self.place_food()
        self.score = 0
        self.dir = np.random.randint(0,4)

        self.display = pygame.display.set_mode((self.grid_size*BLOCK_SIZE, self.grid_size*BLOCK_SIZE))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()


    def place_food(self):
        while True:
            food = (np.random.randint(0, self.grid_size), np.random.randint(0, self.grid_size))
            if food not in self.snake_body:
                self.food = food
                break

    def is_full(self):
        return len(self.snake_body)==self.grid_size**2
    
    def evaluate(self):
        self.snake_body.insert(0, self.head)
        if (
            self.head[0] < 0
            or self.head[0] >= self.grid_size
            or self.head[1] < 0
            or self.head[1] >= self.grid_size
            or self.head in self.snake_body[1:]
        ):
            return -10,True
        
        
        if self.head == self.food:
            self.score += 1
            self.place_food()
            return 10, False
        else:
            self.snake_body.pop()
            return 0, False
        
    def move(self, action):
        if action == 0:  # Up
            self.head = (self.head[0], self.head[1]-1)
        elif action == 1:  # Down
            self.head = (self.head[0]-1, self.head[1])
        elif action == 2:  # Left
            self.head = (self.head[0] , self.head[1]+1)
        elif action == 3:  # Right
            self.head = (self.head[0]+1, self.head[1])
        
    def train(self,player):
        done = False
        while not done and len(player.state_action_reward)<10000:

            state = player.get_state(self)
            next_move = player.find_move(state)
            self.move(next_move)
            reward,done = self.evaluate()
            player.update_sa(state,next_move,reward)
        self.reset()

    def play_self(self,player):
        done = False
        i=0
        while not done:
            state = player.get_state(self)
            action = player.target_policy(state)
            self.move(action)
            rew,done = self.evaluate()
            i+=1
            if rew > 0:
                print(self.score)
        ans = self.score
        self.reset()
        return ans


    def reset(self):
        self.head = (self.grid_size // 2, self.grid_size // 2)
        self.snake_body = [(self.grid_size // 2, self.grid_size // 2)]
        self.place_food()
        self.score = 0
            
    def ui_play(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.dir = 1
                elif event.key == pygame.K_RIGHT:
                    self.dir = 3
                elif event.key == pygame.K_UP:
                    self.dir = 0
                elif event.key == pygame.K_DOWN:
                    self.dir = 2
        
        self.move(self.dir)
        _,done = self.evaluate()
        self.update_ui()
        self.clock.tick(SPEED)
        return done

    def update_ui(self):
        self.display.fill(BLACK)
        
        pygame.draw.rect(self.display,RED, pygame.Rect(self.head[0]*BLOCK_SIZE -2,self.head[1]*BLOCK_SIZE - 2,24,24))
        for pt in self.snake_body:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt[0]*BLOCK_SIZE, pt[1]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt[0]*BLOCK_SIZE+4, pt[1]*BLOCK_SIZE+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food[0]*BLOCK_SIZE, self.food[1]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        

if __name__ == '__main__':
    game = SnakeGame(20,30)
    
    # game loop
    game_over  = False
    while not game_over:
        game_over = game.ui_play()
        
    print('Final Score:', game.score)
    
    pygame.quit()