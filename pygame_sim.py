import pygame as pg
import numpy as np

GRAVITY_CONSTANT = 1

dt = 0.0001

to_remove = []

class Body:
    def __init__(self, mass, x, y):
        self.mass = mass

        self.size = 20

        self.x = x
        self.y = y

        self.dx = 0
        self.dy = 0

        self.velocity = np.array([self.dx, self.dy], dtype=float)
        self.position = np.array([self.x, self.y], dtype=float)

    def calculatePosition(self):
        self.force = np.array([0.0, 0.0])

        for body in bodies:
            if body == self:
                continue

            body_mass = body.mass
            body_position = body.position

            r = body_position - self.position
            epsilon = 0.1
            distance = np.sqrt(np.linalg.norm(r)**2 + epsilon**2)

            direction = r / distance
            gravity = self.calculateForce(distance, body_mass)

            force = direction * gravity       

            if self.mass * body.mass > 0:
               force = direction * gravity * -1
            else:
               force = direction * gravity

            if distance < (self.size + body.size):
               if self not in to_remove:
                  total_mass = self.mass + body.mass

                  if total_mass == 0:
                     self.mass = 0

                     self.velocity = self.velocity + body.velocity
                  else:

                    self.velocity = (
                      self.mass * self.velocity +
                      body.mass * body.velocity
                    ) / total_mass

                  

                  self.mass = total_mass
                  to_remove.append(body)
                  continue

            self.force += force
    
    def calculateForce(self, distance, body_mass):
        return (GRAVITY_CONSTANT * abs(body_mass) * abs(self.mass) / distance ** 2)
    
    def updatePos(self):
        self.position += self.velocity * dt

    def updateVel(self):
        if self.mass != 0:
            acceleration = self.force / abs(self.mass)
            self.velocity += acceleration * dt
        else:
            self.velocity = self.velocity


bodies = []

def askBodies():
    time = int(input("How many seconds: "))
    bodies_num = int(input("How many bodies: "))

    for i in range(bodies_num):
        mass = float(input("Enter the magnitude  of body: "))
        x = int(input("Enter the x of body: "))
        y = int(input("Enter the y of body: "))

        bodies.append(Body(mass, x, y))

    return time

def main():
    time = askBodies()
    running = True  

    pg.font.init()
    font = pg.font.SysFont("Arial", 20)

    window = pg.display.set_mode((500, 500))
    pg.display.set_caption("SIMULATION") 

    pause = False

    clock = pg.time.Clock()
    elapsed = 0 
    while running and elapsed < time:

          dt_real = clock.tick(240) / 1000

          for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                  pause = False if pause == True else True

          window.fill((0,0,0))

          time_text = font.render(f"Time: {elapsed:.2f}s", True, (255,255,255))
          window.blit(time_text, (10, 10))

          if not pause:
           elapsed += dt_real
           steps_per_frame = 500
           for i in range(int(steps_per_frame)):

            for body in bodies:
              body.calculatePosition()

            for body in to_remove:
              if body in bodies:
                bodies.remove(body)

            to_remove.clear()
    
            for body in bodies:
              body.updateVel()
            
            for body in bodies:
                  body.updatePos()

          for body in bodies:
            colour = (0,0,0)
            charge = ""

            if body.mass > 0:
               colour = (255, 0, 0)
               charge = "+"
            elif body.mass < 0:
               colour = (0, 0, 255)
               charge = "-"
            else:
               colour = (100,100,100)
               charge = "0"

            pg.draw.circle(window, colour, body.position.astype(int), body.size)
            pos_int = body.position.astype(int)

            text_surf = font.render(charge, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(int(body.position[0]), int(body.position[1])))

            mag_text = f"{int(body.mass)}" 
            mag_surf = font.render(mag_text, True, (200, 200, 200))
            mag_rect = mag_surf.get_rect(midtop=(pos_int[0], pos_int[1] + body.size + 5))

            window.blit(mag_surf, mag_rect)
            window.blit(text_surf, text_rect)

          pg.display.update()

main()