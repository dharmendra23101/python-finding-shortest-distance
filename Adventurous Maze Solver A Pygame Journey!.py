import pygame
from queue import Queue
from collections import deque
import random


WIDTH = 800
HEIGHT = 600
FPS = 30
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PLAYER_COLOR = (255, 255, 0)  
PATH_COLOR = (255, 165, 0)    


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rescue Mission Game")
clock = pygame.time.Clock()



class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []

    def add_neighbors(self, grid):
      
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x = self.x + dx
                new_y = self.y + dy
                if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                    if isinstance(grid[new_x][new_y], Node):  
                        self.neighbors.append(grid[new_x][new_y])

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y



def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))


def draw_node(x, y, color):
    pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def generate_random_map():
    grid = [[Node(x, y) for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
    
    for _ in range(GRID_WIDTH * GRID_HEIGHT // 5):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        
        grid[x][y] = None
    return grid


def bfs(start, goal, grid):
    frontier = Queue()
    frontier.put(start)
    came_from = {start: None}  

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next_node in current.neighbors:
            if next_node not in came_from:
                frontier.put(next_node)
                came_from[next_node] = current


    current = goal
    path = []
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    path.reverse()
    return path


def dfs(start, goal, grid):
    frontier = deque()
    frontier.append(start)
    came_from = {start: None}  

    while frontier:
        current = frontier.pop()

        if current == goal:
            break

        for next_node in current.neighbors:
            if next_node not in came_from:
                frontier.append(next_node)
                came_from[next_node] = current

  
    current = goal
    path = []
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    path.reverse()
    return path


def main():
    start = Node(0, 0)
    goal = Node(GRID_WIDTH - 1, GRID_HEIGHT - 1)
    grid = generate_random_map()

   
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if isinstance(grid[x][y], Node):
                grid[x][y].add_neighbors(grid)

    player_position = start
    running = True

    while running:
        screen.fill(WHITE)
        draw_grid()

       
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if grid[x][y] is None: 
                    draw_node(x, y, BLACK)

       
        bfs_path = bfs(player_position, goal, grid)

       
        for node in bfs_path:
            draw_node(node.x, node.y, PATH_COLOR) 

        
        draw_node(player_position.x, player_position.y, PLAYER_COLOR)  

      
        draw_node(start.x, start.y, BLUE)
        draw_node(goal.x, goal.y, BLUE)

        if player_position == goal: 
            running = False 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    new_x = player_position.x
                    new_y = max(player_position.y - 1, 0)
                    if isinstance(grid[new_x][new_y], Node):
                        player_position = grid[new_x][new_y]
                elif event.key == pygame.K_DOWN:
                    new_x = player_position.x
                    new_y = min(player_position.y + 1, GRID_HEIGHT - 1)
                    if isinstance(grid[new_x][new_y], Node):
                        player_position = grid[new_x][new_y]
                elif event.key == pygame.K_LEFT:
                    new_x = max(player_position.x - 1, 0)
                    new_y = player_position.y
                    if isinstance(grid[new_x][new_y], Node):
                        player_position = grid[new_x][new_y]
                elif event.key == pygame.K_RIGHT:
                    new_x = min(player_position.x + 1, GRID_WIDTH - 1)
                    new_y = player_position.y
                    if isinstance(grid[new_x][new_y], Node):
                        player_position = grid[new_x][new_y]

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
