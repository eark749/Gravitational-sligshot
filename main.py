import pygame
import math

pygame.init()


#constant  definitions 
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Gravitational Slingshot Effect") 

Planet_Mass = 100
Ship_Mass = 5
G = 5
FPS = 60
Planet_Size = 50
Object_Size = 5
Vel_Scale = 100

BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
Planet = pygame.transform.scale(pygame.image.load("jupiter.png"), (Planet_Size * 2, Planet_Size * 2))

White = (255, 255, 255)
Red = (255, 0, 0)
Blue = (0, 0, 255)

class planet_class:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        win.blit(Planet, (self.x - Planet_Size, self.y - Planet_Size))

class spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    def move(self, planet = None):
        distance = math.sqrt((self.x - planet.x)**2 +(self.y - planet.y)**2)
        force = (G * self.mass * planet.mass) / distance ** 2
        
        acceleration = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self):
        pygame.draw.circle(win, Red, (int(self.x), int(self.y)), Object_Size)

def create_ship(location, mouse):
    t_x, t_y = location
    m_x, m_y = mouse
    vel_x = (m_x - t_x) / Vel_Scale
    vel_y = (m_y - t_y) / Vel_Scale
    obj = spacecraft(t_x, t_y, vel_x, vel_y, Ship_Mass)
    return obj


#pygame main loop
def main():
    running = True
    clock = pygame.time.Clock()

    Planet = planet_class(WIDTH // 2, HEIGHT // 2, Planet_Mass)
    objects = []
    temp_obj_pos = None

    while running:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = create_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos

        win.blit(BG, (0, 0))

        if temp_obj_pos:
            pygame.draw.line(win, White, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, Red, temp_obj_pos, Object_Size)

        for obj in objects[:]:
            obj.draw()
            obj.move(Planet)
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = math.sqrt((obj.x - Planet.x)**2  + (obj.y - Planet.y)**2) <= Planet_Size
            if off_screen or collided:
                objects.remove(obj)

        Planet.draw()


        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()