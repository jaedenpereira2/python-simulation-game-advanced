import pygame
import random
import math
from typing import List, Dict, Tuple

class ClimateZone:
    def __init__(self, name: str, temperature: float, rainfall: float, fertility: float):
        self.name = name
        self.temperature = temperature  # -1.0 to 1.0 (cold to hot)
        self.rainfall = rainfall  # 0.0 to 1.0 (dry to wet)
        self.fertility = fertility  # 0.0 to 1.0 (poor to rich soil)
        self.population = 0.0
        self.resources = {
            'food': 0.0,
            'water': 0.0,
            'materials': 0.0
        }

class ClimateSystem:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.climate_zones: List[ClimateZone] = []
        self.global_temperature = 0.0  # -1.0 to 1.0
        self.season = 0  # 0-3 (Spring, Summer, Fall, Winter)
        self.season_progress = 0.0  # 0.0 to 1.0
        
        # Initialize climate zones
        self._initialize_climate_zones()
        
    def _initialize_climate_zones(self):
        # Create different climate zones
        self.climate_zones = [
            ClimateZone("Arctic", -0.8, 0.3, 0.2),  # Cold, low rainfall, poor soil
            ClimateZone("Tundra", -0.6, 0.4, 0.3),
            ClimateZone("Taiga", -0.4, 0.5, 0.4),
            ClimateZone("Temperate", 0.0, 0.6, 0.7),  # Moderate temperature, good rainfall, fertile
            ClimateZone("Mediterranean", 0.3, 0.5, 0.6),
            ClimateZone("Desert", 0.8, 0.1, 0.2),  # Hot, very dry, poor soil
            ClimateZone("Savanna", 0.6, 0.4, 0.5),
            ClimateZone("Tropical", 0.7, 0.9, 0.8),  # Hot, very wet, very fertile
            ClimateZone("Mountain", -0.2, 0.7, 0.4)
        ]
        
    def update(self, delta_time: float):
        # Update season progress
        self.season_progress += delta_time * 0.1  # Adjust speed of seasons
        if self.season_progress >= 1.0:
            self.season_progress = 0.0
            self.season = (self.season + 1) % 4
            
        # Update global temperature based on season
        season_temperatures = [-0.3, 0.3, 0.0, -0.3]  # Spring, Summer, Fall, Winter
        target_temp = season_temperatures[self.season]
        self.global_temperature += (target_temp - self.global_temperature) * delta_time
        
        # Update climate zones
        for zone in self.climate_zones:
            # Adjust zone temperature based on global temperature
            zone.temperature = max(-1.0, min(1.0, zone.temperature + self.global_temperature * 0.1))
            
            # Update resources based on climate
            self._update_zone_resources(zone, delta_time)
            
    def _update_zone_resources(self, zone: ClimateZone, delta_time: float):
        # Food production based on temperature, rainfall, and fertility
        food_production = (zone.temperature + 1) * 0.5  # Temperature factor
        food_production *= zone.rainfall  # Rainfall factor
        food_production *= zone.fertility  # Soil fertility factor
        food_production *= (1 + zone.population * 0.001)  # Population factor
        
        # Water availability based on rainfall
        water_production = zone.rainfall * (1 + zone.temperature * 0.5)
        
        # Materials based on population and climate
        materials_production = zone.population * 0.001 * (1 + zone.temperature * 0.3)
        
        # Update resources
        zone.resources['food'] += food_production * delta_time
        zone.resources['water'] += water_production * delta_time
        zone.resources['materials'] += materials_production * delta_time
        
    def get_climate_effects(self) -> Dict[str, float]:
        """Get the current climate effects on resources"""
        return {
            'temperature': self.global_temperature,
            'season': self.season,
            'season_progress': self.season_progress
        }
        
    def draw(self, screen: pygame.Surface, camera_x: float, camera_y: float, zoom: float):
        # Draw climate information in the UI
        font = pygame.font.Font(None, 24)
        
        # Draw season
        seasons = ["Spring", "Summer", "Fall", "Winter"]
        season_text = f"Season: {seasons[self.season]}"
        season_surface = font.render(season_text, True, (255, 255, 255))
        screen.blit(season_surface, (20, 200))
        
        # Draw temperature
        temp_text = f"Global Temperature: {self.global_temperature:.2f}"
        temp_surface = font.render(temp_text, True, (255, 255, 255))
        screen.blit(temp_surface, (20, 230))
        
        # Draw climate zones
        for i, zone in enumerate(self.climate_zones):
            zone_text = f"{zone.name}: Temp={zone.temperature:.2f}, Rain={zone.rainfall:.2f}"
            zone_surface = font.render(zone_text, True, (255, 255, 255))
            screen.blit(zone_surface, (20, 260 + i * 25)) 