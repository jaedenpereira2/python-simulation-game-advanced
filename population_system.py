import pygame
import random
import math
from typing import Dict, List, Tuple

class PopulationZone:
    def __init__(self, name: str, base_growth_rate: float, climate_factor: float):
        self.name = name
        self.population = 0.0
        self.base_growth_rate = base_growth_rate
        self.climate_factor = climate_factor
        self.resources = {
            'food': 0.0,
            'water': 0.0,
            'shelter': 0.0
        }
        self.development_level = 0.0  # 0.0 to 1.0
        self.happiness = 0.5  # 0.0 to 1.0
        
    def update(self, delta_time: float, climate_effects: Dict[str, float], resources: Dict[str, float]):
        # Update development level based on resources
        self.development_level = min(1.0, self.development_level + 
            (resources.get('materials', 0) * 0.001 + resources.get('technology', 0) * 0.002) * delta_time)
        
        # Calculate growth rate based on various factors
        growth_rate = self.base_growth_rate
        
        # Climate effects
        temperature = climate_effects.get('temperature', 0.0)
        season = climate_effects.get('season', 0)
        
        # Temperature affects growth rate
        temp_factor = 1.0 - abs(temperature) * 0.5  # Extreme temperatures reduce growth
        growth_rate *= temp_factor
        
        # Seasonal effects
        season_factors = {
            0: 1.2,  # Spring - good for growth
            1: 1.0,  # Summer - normal
            2: 0.8,  # Fall - slower growth
            3: 0.6   # Winter - slowest growth
        }
        growth_rate *= season_factors.get(season, 1.0)
        
        # Resource effects
        food_factor = min(1.0, resources.get('food', 0) / (self.population + 1))
        water_factor = min(1.0, resources.get('water', 0) / (self.population + 1))
        growth_rate *= (food_factor + water_factor) / 2
        
        # Development level affects growth
        growth_rate *= (1.0 + self.development_level * 0.5)
        
        # Update population
        self.population += self.population * growth_rate * delta_time
        
        # Update happiness
        self.happiness = (food_factor + water_factor + self.development_level) / 3
        
        # Ensure population doesn't go below 0
        self.population = max(0.0, self.population)

class PopulationSystem:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.population_zones: List[PopulationZone] = []
        
        # Initialize population zones
        self._initialize_zones()
        
    def _initialize_zones(self):
        # Create different population zones with varying base growth rates and climate factors
        self.population_zones = [
            PopulationZone("Urban", 0.1, 0.8),  # High growth, less climate dependent
            PopulationZone("Suburban", 0.08, 0.6),
            PopulationZone("Rural", 0.05, 0.4),
            PopulationZone("Coastal", 0.07, 0.5),
            PopulationZone("Mountain", 0.03, 0.3),  # Low growth, more climate dependent
            PopulationZone("Desert", 0.02, 0.2),
            PopulationZone("Tropical", 0.09, 0.7),
            PopulationZone("Arctic", 0.01, 0.1)
        ]
        
    def update(self, delta_time: float, climate_effects: Dict[str, float], resources: Dict[str, float]):
        total_population = 0.0
        
        # Update each zone
        for zone in self.population_zones:
            zone.update(delta_time, climate_effects, resources)
            total_population += zone.population
            
        return total_population
        
    def get_population_distribution(self) -> Dict[str, float]:
        """Get the current population distribution across zones"""
        total = sum(zone.population for zone in self.population_zones)
        if total == 0:
            return {zone.name: 0.0 for zone in self.population_zones}
            
        return {zone.name: zone.population / total for zone in self.population_zones}
        
    def get_zone_happiness(self) -> Dict[str, float]:
        """Get the happiness level for each zone"""
        return {zone.name: zone.happiness for zone in self.population_zones}
        
    def draw(self, screen: pygame.Surface, x: int, y: int):
        font = pygame.font.Font(None, 24)
        
        # Draw population information
        title = "Population Distribution"
        title_surface = font.render(title, True, (255, 255, 255))
        screen.blit(title_surface, (x, y))
        
        # Draw each zone's population and happiness
        for i, zone in enumerate(self.population_zones):
            # Population text
            pop_text = f"{zone.name}: {zone.population:.1f}"
            pop_surface = font.render(pop_text, True, (255, 255, 255))
            screen.blit(pop_surface, (x, y + 30 + i * 25))
            
            # Happiness text and bar in a more compact layout
            happiness_text = f"H: {zone.happiness:.2f}"
            happiness_surface = font.render(happiness_text, True, (255, 255, 255))
            screen.blit(happiness_surface, (x + 120, y + 30 + i * 25))
            
            # Draw happiness bar
            bar_width = 80
            bar_height = 10
            bar_x = x + 180
            bar_y = y + 35 + i * 25
            
            # Background
            pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            # Happiness level
            happiness_width = int(bar_width * zone.happiness)
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, happiness_width, bar_height)) 