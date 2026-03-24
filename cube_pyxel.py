import pyxel
import math

class Cube:
    def __init__(self, x, y, z):
        WIDTH, HEIGHT = 1000, 1000
        pyxel.init(WIDTH, HEIGHT, "3D Cube", fps=30)
        self.center = [WIDTH//2, HEIGHT//2]
        self.size = 50
        self.pos = [x, y, z]
        self.angle = [0, 0, 0]
        self.edge_mode = True
        
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
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_K):
            self.edge_mode = not self.edge_mode

        # SIZE (E/A)
        zoom_speed = 5
        if pyxel.btn(pyxel.KEY_E): 
            self.size += zoom_speed # Zoom in
        if pyxel.btn(pyxel.KEY_A): 
            self.size -= zoom_speed # Zoom out
        
        # MOVEMENT (ZQSD)
        movement_speed = 5
        if pyxel.btn(pyxel.KEY_Z): 
            self.pos[1] -= movement_speed  # Up
        if pyxel.btn(pyxel.KEY_S): 
            self.pos[1] += movement_speed  # Down
        if pyxel.btn(pyxel.KEY_Q): 
            self.pos[0] -= movement_speed  # Left
        if pyxel.btn(pyxel.KEY_D): 
            self.pos[0] += movement_speed  # Right
        
        # DEPTH (W/C)
        if pyxel.btn(pyxel.KEY_W): 
            self.pos[2] -= movement_speed  # Forward (Closer)
        if pyxel.btn(pyxel.KEY_C): 
            self.pos[2] += movement_speed  # Backward (Further)

        # ROTATION (R/T, F/V, B/N)
        rotation_speed = 0.05
        if pyxel.btn(pyxel.KEY_R): 
            self.angle[0] += rotation_speed # Rotate on X axis 
        if pyxel.btn(pyxel.KEY_T): 
            self.angle[0] -= rotation_speed # Rotate on X axis
        if pyxel.btn(pyxel.KEY_F): 
            self.angle[1] += rotation_speed # Rotate on Y axis
        if pyxel.btn(pyxel.KEY_V): 
            self.angle[1] -= rotation_speed # Rotate on Y axis
        if pyxel.btn(pyxel.KEY_B): 
            self.angle[2] += rotation_speed # Rotate on Z axis 
        if pyxel.btn(pyxel.KEY_N): 
            self.angle[2] -= rotation_speed # Rotate on Z axis

        # AUTOMATIC ROTATION (Space)
        if pyxel.btn(pyxel.KEY_SPACE):
            self.angle[0] += 0.05
            self.angle[1] += 0.05

        # RESET (X)
        if pyxel.btnp(pyxel.KEY_X):
            self.pos = [0, 0, 0]
            self.angle = [0, 0, 0]

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
        pyxel.cls(0)
        points_3D = []
        points_2D = []
        for corner in self.Corners:
            x, y, z = [c * self.size for c in corner]
            rotated_x, rotated_y, rotated_z = self.rotate_point(x, y, z)
            points_3D.append((rotated_x, rotated_y, rotated_z))
            points_2D.append(self.convert_to_2d(rotated_x, rotated_y, rotated_z))
        
        if self.edge_mode:
            for edge in self.Edges:
                p1 = points_2D[edge[0]]
                p2 = points_2D[edge[1]]
                pyxel.line(p1[0], p1[1], p2[0], p2[1] , 7)
        """
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
        """

for i in range(5):
    Cube(i*50, 0, i*50)
