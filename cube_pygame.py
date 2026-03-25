import pygame
import math

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.Cubes = []
        self.size = 100
        for i in range(4):
            cube = Cube(i, 0, 0, 100, self.screen)
            self.Cubes.append(cube)


    def run(self):
        while True:
            for cube in self.Cubes:
                cube.update()
                cube.draw()
            pygame.display.flip()
            self.clock.tick(60)

class Cube:
    def __init__(self, x, y, z, size, screen):
        self.screen = screen
        self.size = size
        self.pos = [x, y, z]
        self.angle = [0, 0, 0]
        self.edge_mode = True
        self.center = pygame.display.get_surface().get_rect().center
        
        self.Corners = [
            [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
            [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1]
        ]
        
        self.Edges = [
            (0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
            (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)
        ]

        self.Faces = [
            (0, 1, 3, 2),
            (4, 5, 7, 6),
            (0, 1, 5, 4),
            (2, 3, 7, 6),
            (0, 2, 6, 4),
            (1, 3, 7, 5) 
        ]

    def update(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    self.edge_mode = not self.edge_mode

        # SIZE (E/A)
        zoom_speed = 5
        if keys[pygame.K_e]: 
            self.size += zoom_speed # Zoom in
        if keys[pygame.K_a]: 
            self.size -= zoom_speed # Zoom out
        
        # MOVEMENT (ZQSD)
        movement_speed = 5
        if keys[pygame.K_z]: 
            self.pos[1] -= movement_speed  # Up
        if keys[pygame.K_s]: 
            self.pos[1] += movement_speed  # Down
        if keys[pygame.K_q]: 
            self.pos[0] -= movement_speed  # Left
        if keys[pygame.K_d]: 
            self.pos[0] += movement_speed  # Right
        
        # DEPTH (W/C)
        if keys[pygame.K_w]: 
            self.pos[2] -= movement_speed  # Forward (Closer)
        if keys[pygame.K_c]: 
            self.pos[2] += movement_speed  # Backward (Further)

        # ROTATION (R/T, F/V, B/N)
        rotation_speed = 0.05
        if keys[pygame.K_r]: 
            self.angle[0] += rotation_speed # Rotate on X axis 
        if keys[pygame.K_t]: 
            self.angle[0] -= rotation_speed # Rotate on X axis
        if keys[pygame.K_f]: 
            self.angle[1] += rotation_speed # Rotate on Y axis
        if keys[pygame.K_v]: 
            self.angle[1] -= rotation_speed # Rotate on Y axis
        if keys[pygame.K_b]: 
            self.angle[2] += rotation_speed # Rotate on Z axis 
        if keys[pygame.K_n]: 
            self.angle[2] -= rotation_speed # Rotate on Z axis

        # AUTOMATIC ROTATION (Space)
        if keys[pygame.K_SPACE]:
            self.angle[0] += 0.05
            self.angle[1] += 0.05

        # RESET (X)
        if keys[pygame.K_x]:
            self.pos = [0, 0, 0]
            self.angle = [0, 0, 0]
            self.size = 100

    def rotate_point(self, x, y, z):
        # Rotate around X axis
        rad_x = self.angle[0]
        ny = y * math.cos(rad_x) - z * math.sin(rad_x)
        nz = y * math.sin(rad_x) + z * math.cos(rad_x)
        y, z = ny, nz

        # Rotate around Y axis
        rad_y = self.angle[1]
        nx = x * math.cos(rad_y) + z * math.sin(rad_y)
        nz = -x * math.sin(rad_y) + z * math.cos(rad_y)
        x, z = nx, nz

        # Rotate around Z axis
        rad_z = self.angle[2]
        nx = x * math.cos(rad_z) - y * math.sin(rad_z)
        ny = x * math.sin(rad_z) + y * math.cos(rad_z)
        x, y = nx, ny

        return x, y, z

    def convert_to_2d(self, x, y, z):
        x += self.pos[0]
        y += self.pos[1]
        z += self.pos[2]

        perspective = 600
        factor = perspective / (perspective + z + 200) 
        x2D = x * factor + self.center[0]
        y2D = y * factor + self.center[1]
        return (x2D, y2D)

    def draw(self):
        self.screen.fill((0, 0, 0))
        points_3D = []
        points_2D = []
        for corner in self.Corners:
            x, y, z = [c * self.size for c in corner]
            rotated_x, rotated_y, rotated_z = self.rotate_point(x, y, z)
            points_3D.append((rotated_x, rotated_y, rotated_z))
            points_2D.append(self.convert_to_2d(rotated_x, rotated_y, rotated_z))
        
        if self.edge_mode:
            for edge in self.Edges:
                pygame.draw.line(self.screen, (255, 255, 255), points_2D[edge[0]], points_2D[edge[1]], 2)
        else:
            face_depths = []
            for face in self.Faces:
                z_sum = sum(points_3D[i][2] for i in face)
                averageZ = z_sum / 4
                face_depths.append((averageZ, face))
            face_depths.sort(reverse=True)
            for depth, face in face_depths:
                points = [points_2D[i] for i in face]
                pygame.draw.polygon(self.screen, (255, 255, 255), points)
                pygame.draw.polygon(self.screen, (0, 0, 0), points, 2)


app = App()
app.run()
