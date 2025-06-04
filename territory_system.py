import pygame
import random
import math
from typing import Dict, List, Tuple, Optional

class Territory:
    def __init__(self, name: str, x: float, y: float, radius: float):
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.resources = {
            'food': random.uniform(0.1, 0.5),
            'water': random.uniform(0.1, 0.5),
            'energy': random.uniform(0.1, 0.3),
            'materials': random.uniform(0.1, 0.3),
            'technology': random.uniform(0.05, 0.2)
        }
        self.development = 0.0  # 0.0 to 1.0
        self.owner = None  # Name of the civilization that owns this territory
        self.is_hovered = False
        self.last_name_rect = None
        
    def update(self, delta_time: float, climate_effects: Dict[str, float]):
        # Update resource production based on climate effects
        for resource in self.resources:
            if resource in climate_effects:
                self.resources[resource] *= (1.0 + climate_effects[resource] * delta_time)
                
        # Update development based on resource production
        resource_factor = sum(self.resources.values()) / 5.0  # Average of all resources
        self.development = min(1.0, self.development + resource_factor * 0.001 * delta_time)
        
    def draw(self, screen: pygame.Surface, camera_x: float, camera_y: float, zoom: float, is_selected: bool = False):
        # Convert world coordinates to screen coordinates
        screen_x = int((self.x - camera_x) * zoom + screen.get_width() // 2)
        screen_y = int((self.y - camera_y) * zoom + screen.get_height() // 2)
        screen_radius = int(self.radius * zoom)
        
        # Draw territory circle
        color = (100, 100, 100)  # Default gray
        if self.owner:
            # Use owner's color
            if self.owner == "Western Alliance":
                color = (0, 100, 255)  # Blue
            elif self.owner == "Eastern Federation":
                color = (255, 50, 50)  # Red
            elif self.owner == "Southern Union":
                color = (50, 255, 50)  # Green
            elif self.owner == "Northern Coalition":
                color = (255, 255, 50)  # Yellow
                
        if is_selected:
            # Draw selection ring
            pygame.draw.circle(screen, (255, 255, 255), (screen_x, screen_y), screen_radius + 2)
            
        if self.is_hovered:
            # Draw hover ring
            pygame.draw.circle(screen, (200, 200, 200), (screen_x, screen_y), screen_radius + 1)
            
        pygame.draw.circle(screen, color, (screen_x, screen_y), screen_radius)
        
        # Draw territory name with background
        font = pygame.font.Font(None, 24)
        name_surface = font.render(self.name, True, (255, 255, 255))
        name_rect = name_surface.get_rect(center=(screen_x, screen_y - screen_radius - 15))
        
        # Draw semi-transparent background for better readability
        text_bg_rect = name_rect.inflate(10, 5)
        text_bg_surface = pygame.Surface((text_bg_rect.width, text_bg_rect.height), pygame.SRCALPHA)
        text_bg_surface.fill((0, 0, 0, 128))  # Semi-transparent black
        screen.blit(text_bg_surface, text_bg_rect)
        
        # Draw the text
        screen.blit(name_surface, name_rect)
        
        # Store the name rectangle for click detection
        self.last_name_rect = text_bg_rect
        
        return text_bg_rect

class TerritorySystem:
    def __init__(self):
        self.territories: List[Territory] = []
        self._initialize_territories()
        
    def _initialize_territories(self):
        # Create territories with different positions and sizes
        territory_data = [
            ("North America", 0.2, 0.3, 0.15),
            ("South America", 0.3, 0.6, 0.12),
            ("Europe", 0.5, 0.2, 0.1),
            ("Africa", 0.5, 0.5, 0.15),
            ("Asia", 0.7, 0.3, 0.2),
            ("Oceania", 0.8, 0.6, 0.1)
        ]
        
        for name, x, y, radius in territory_data:
            self.territories.append(Territory(name, x, y, radius))
            
    def update(self, delta_time: float, climate_effects: Dict[str, float]):
        for territory in self.territories:
            territory.update(delta_time, climate_effects)
            
    def draw(self, screen: pygame.Surface, camera_x: float, camera_y: float, zoom: float, selected_territory: Optional[Territory] = None) -> Dict[Tuple[int, int, int, int], Territory]:
        name_rect_map = {}
        for territory in self.territories:
            name_rect = territory.draw(screen, camera_x, camera_y, zoom, territory == selected_territory)
            if name_rect:
                # Store rectangle coordinates as tuple for click detection
                name_rect_map[(name_rect.left, name_rect.top, name_rect.right, name_rect.bottom)] = territory
        return name_rect_map
        
    def get_territory_at(self, x: float, y: float) -> Optional[Territory]:
        for territory in self.territories:
            dx = x - territory.x
            dy = y - territory.y
            distance = math.sqrt(dx * dx + dy * dy)
            if distance <= territory.radius:
                return territory
        return None
        
    def set_territory_owner(self, territory_name: str, owner: Optional[str]):
        for territory in self.territories:
            if territory.name == territory_name:
                territory.owner = owner
                break
    
    def get_territory_resources(self) -> Dict[str, Dict[str, float]]:
        return {territory.name: territory.resources for territory in self.territories}
    
    def get_territory_population(self) -> Dict[str, float]:
        return {territory.name: territory.population for territory in self.territories}
    
    def get_territory_development(self) -> Dict[str, float]:
        return {territory.name: territory.development for territory in self.territories} 