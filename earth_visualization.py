import pygame
import math
import random
from typing import List, Tuple

class EarthVisualization:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Earth properties
        self.earth_radius = 300
        self.earth_x = screen_width // 2
        self.earth_y = screen_height // 2
        self.rotation = 0
        self.rotation_speed = 0.1
        
        # Cloud properties
        self.clouds: List[Cloud] = []
        self.max_clouds = 20
        self.cloud_spawn_timer = 0
        self.cloud_spawn_delay = 1000  # milliseconds
        
        # Initialize clouds
        self._initialize_clouds()
        
    def _initialize_clouds(self):
        """Initialize random clouds around the Earth"""
        for _ in range(self.max_clouds):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(self.earth_radius * 1.1, self.earth_radius * 1.3)
            speed = random.uniform(0.001, 0.005)  # Extremely slow clouds
            size = random.uniform(20, 40)
            self.clouds.append(Cloud(angle, distance, speed, size))
    
    def update(self, delta_time: float):
        # Update Earth rotation
        self.rotation += self.rotation_speed * delta_time
        if self.rotation >= 360:
            self.rotation = 0
            
        # Update clouds
        for cloud in self.clouds:
            cloud.update(delta_time, self.rotation)
            
        # Spawn new clouds
        self.cloud_spawn_timer += delta_time * 1000
        if self.cloud_spawn_timer >= self.cloud_spawn_delay:
            self.cloud_spawn_timer = 0
            if len(self.clouds) < self.max_clouds:
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(self.earth_radius * 1.1, self.earth_radius * 1.3)
                speed = random.uniform(0.2, 0.5)
                size = random.uniform(20, 40)
                self.clouds.append(Cloud(angle, distance, speed, size))
    
    def draw(self, screen: pygame.Surface, camera_x: float, camera_y: float, zoom: float):
        # Draw Earth
        pygame.draw.circle(
            screen,
            (0, 100, 255),  # Ocean blue
            (self.earth_x + camera_x, self.earth_y + camera_y),
            int(self.earth_radius * zoom)
        )
        
        # Draw continents (simplified for now)
        self._draw_continents(screen, camera_x, camera_y, zoom)
        
        # Draw clouds
        for cloud in self.clouds:
            cloud.draw(screen, self.earth_x + camera_x, self.earth_y + camera_y, zoom)
    
    def _draw_continents(self, screen: pygame.Surface, camera_x: float, camera_y: float, zoom: float):
        # Highly detailed continent shapes based on actual world map
        continent_points = [
            # North America (more detailed shape)
            [(0.12, 0.25), (0.10, 0.22), (0.08, 0.18), (0.10, 0.15), (0.12, 0.12),
             (0.15, 0.10), (0.18, 0.12), (0.20, 0.15), (0.22, 0.18), (0.25, 0.20),
             (0.28, 0.22), (0.30, 0.25), (0.32, 0.28), (0.35, 0.30), (0.38, 0.32),
             (0.40, 0.35), (0.38, 0.38), (0.35, 0.40), (0.32, 0.38), (0.30, 0.35),
             (0.28, 0.32), (0.25, 0.30), (0.22, 0.28), (0.20, 0.25), (0.18, 0.22),
             (0.15, 0.20)],
            
            # South America (more accurate shape)
            [(0.30, 0.55), (0.32, 0.58), (0.35, 0.62), (0.38, 0.65), (0.40, 0.68),
             (0.42, 0.72), (0.40, 0.75), (0.38, 0.78), (0.35, 0.82), (0.32, 0.85),
             (0.30, 0.88), (0.28, 0.85), (0.25, 0.82), (0.22, 0.78), (0.20, 0.75),
             (0.18, 0.72), (0.20, 0.68), (0.22, 0.65), (0.25, 0.62), (0.28, 0.58)],
            
            # Europe (more detailed shape)
            [(0.48, 0.25), (0.50, 0.22), (0.52, 0.20), (0.55, 0.18), (0.58, 0.20),
             (0.60, 0.22), (0.62, 0.25), (0.65, 0.28), (0.68, 0.30), (0.70, 0.32),
             (0.68, 0.35), (0.65, 0.38), (0.62, 0.40), (0.58, 0.38), (0.55, 0.35),
             (0.52, 0.32), (0.50, 0.28)],
            
            # Africa (more accurate shape)
            [(0.48, 0.45), (0.50, 0.42), (0.52, 0.45), (0.55, 0.48), (0.58, 0.52),
             (0.60, 0.55), (0.62, 0.58), (0.65, 0.62), (0.62, 0.65), (0.60, 0.68),
             (0.58, 0.72), (0.55, 0.75), (0.52, 0.78), (0.50, 0.75), (0.48, 0.72),
             (0.45, 0.68), (0.42, 0.65), (0.40, 0.62), (0.38, 0.58), (0.40, 0.55),
             (0.42, 0.52), (0.45, 0.48)],
            
            # Asia (more detailed shape)
            [(0.65, 0.25), (0.68, 0.22), (0.70, 0.25), (0.72, 0.28), (0.75, 0.32),
             (0.78, 0.35), (0.80, 0.38), (0.82, 0.42), (0.85, 0.45), (0.88, 0.48),
             (0.85, 0.52), (0.82, 0.55), (0.80, 0.58), (0.78, 0.62), (0.75, 0.65),
             (0.72, 0.62), (0.70, 0.58), (0.68, 0.55), (0.65, 0.52), (0.62, 0.48),
             (0.60, 0.45), (0.62, 0.42), (0.65, 0.38), (0.68, 0.35), (0.70, 0.32),
             (0.72, 0.28)],
            
            # Australia (more accurate shape)
            [(0.72, 0.72), (0.75, 0.68), (0.78, 0.72), (0.80, 0.75), (0.82, 0.78),
             (0.85, 0.82), (0.82, 0.85), (0.80, 0.88), (0.78, 0.85), (0.75, 0.82),
             (0.72, 0.78), (0.70, 0.75)],
            
            # Greenland (more accurate shape)
            [(0.35, 0.12), (0.38, 0.10), (0.40, 0.08), (0.42, 0.10), (0.45, 0.12),
             (0.48, 0.15), (0.45, 0.18), (0.42, 0.20), (0.40, 0.18), (0.38, 0.15),
             (0.35, 0.12)],
            
            # Antarctica (more detailed shape)
            [(0.1, 0.92), (0.2, 0.90), (0.3, 0.92), (0.4, 0.95), (0.5, 0.98),
             (0.6, 0.95), (0.7, 0.92), (0.8, 0.90), (0.9, 0.92), (0.95, 0.95),
             (0.9, 0.98), (0.8, 0.99), (0.7, 0.98), (0.6, 0.97), (0.5, 0.96),
             (0.4, 0.97), (0.3, 0.98), (0.2, 0.97), (0.1, 0.96), (0.05, 0.95)],
            
            # Middle East (more detailed shape)
            [(0.55, 0.45), (0.58, 0.42), (0.60, 0.45), (0.62, 0.48), (0.65, 0.52),
             (0.62, 0.55), (0.60, 0.58), (0.58, 0.55), (0.55, 0.52)],
            
            # India (more accurate shape)
            [(0.62, 0.58), (0.65, 0.55), (0.68, 0.58), (0.70, 0.62), (0.68, 0.65),
             (0.65, 0.68), (0.62, 0.65)],
            
            # Central America (more detailed shape)
            [(0.25, 0.38), (0.28, 0.35), (0.30, 0.38), (0.32, 0.42), (0.35, 0.45),
             (0.32, 0.48), (0.30, 0.52), (0.28, 0.48), (0.25, 0.45)],
            
            # Southeast Asia (more detailed shape)
            [(0.72, 0.55), (0.75, 0.52), (0.78, 0.55), (0.80, 0.58), (0.82, 0.62),
             (0.80, 0.65), (0.78, 0.68), (0.75, 0.65), (0.72, 0.62)],
            
            # Madagascar (more accurate shape)
            [(0.55, 0.72), (0.58, 0.68), (0.60, 0.72), (0.58, 0.75), (0.55, 0.78)],
            
            # Japan (more detailed shape)
            [(0.78, 0.35), (0.80, 0.32), (0.82, 0.35), (0.84, 0.38), (0.82, 0.42),
             (0.80, 0.38), (0.78, 0.35)],
            
            # British Isles (more detailed shape)
            [(0.45, 0.22), (0.48, 0.20), (0.50, 0.22), (0.52, 0.25), (0.50, 0.28),
             (0.48, 0.25), (0.45, 0.22)],
            
            # Indonesia (more detailed shape)
            [(0.72, 0.65), (0.75, 0.62), (0.78, 0.65), (0.80, 0.68), (0.78, 0.72),
             (0.75, 0.68), (0.72, 0.65)],
            
            # Philippines (more detailed shape)
            [(0.76, 0.58), (0.78, 0.55), (0.80, 0.58), (0.82, 0.62), (0.80, 0.65),
             (0.78, 0.62), (0.76, 0.58)],
            
            # New Zealand (more detailed shape)
            [(0.80, 0.82), (0.82, 0.78), (0.84, 0.82), (0.86, 0.85), (0.84, 0.88),
             (0.82, 0.85), (0.80, 0.82)]
        ]
        
        for continent in continent_points:
            points = []
            for x, y in continent:
                # Convert relative coordinates to screen coordinates
                angle = x * 2 * math.pi
                distance = y * self.earth_radius
                point_x = self.earth_x + camera_x + math.cos(angle + math.radians(self.rotation)) * distance * zoom
                point_y = self.earth_y + camera_y + math.sin(angle + math.radians(self.rotation)) * distance * zoom
                points.append((point_x, point_y))
            
            if len(points) >= 3:
                pygame.draw.polygon(screen, (0, 200, 0), points)  # Green for land

class Cloud:
    def __init__(self, angle: float, distance: float, speed: float, size: float):
        self.angle = angle
        self.distance = distance
        self.speed = speed
        self.size = size
        self.opacity = random.randint(100, 200)
        self.rotation = random.uniform(0, 360)  # Individual cloud rotation
        self.rotation_speed = random.uniform(-0.5, 0.5)  # Random rotation speed
        
    def update(self, delta_time: float, earth_rotation: float):
        # Update cloud position
        self.angle += self.speed * delta_time
        if self.angle >= 2 * math.pi:
            self.angle = 0
            
        # Update cloud's own rotation
        self.rotation += self.rotation_speed * delta_time
        if self.rotation >= 360:
            self.rotation = 0
            
        # Randomly change opacity
        self.opacity += random.uniform(-1, 1)
        self.opacity = max(50, min(200, self.opacity))
        
    def draw(self, screen: pygame.Surface, center_x: float, center_y: float, zoom: float):
        # Calculate cloud position
        x = center_x + math.cos(self.angle) * self.distance * zoom
        y = center_y + math.sin(self.angle) * self.distance * zoom
        
        # Create cloud surface with transparency
        cloud_surface = pygame.Surface((int(self.size * 2 * zoom), int(self.size * zoom)), pygame.SRCALPHA)
        
        # Draw cloud as a series of circles with rotation
        for i in range(3):
            # Calculate rotated offset
            offset_angle = math.radians(self.rotation + (i * 120))  # Space circles evenly
            offset_x = math.cos(offset_angle) * (self.size/2)
            offset_y = math.sin(offset_angle) * (self.size/2)
            
            pygame.draw.circle(
                cloud_surface,
                (255, 255, 255, int(self.opacity)),
                (int(self.size * zoom + offset_x), int(self.size/2 * zoom + offset_y)),
                int(self.size/2 * zoom)
            )
        
        # Draw the cloud surface
        screen.blit(cloud_surface, (x - self.size * zoom, y - self.size/2 * zoom)) 