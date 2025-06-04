import pygame
import random
import math
from typing import Dict, List, Tuple

class ResourceInteraction:
    def __init__(self, resource1: str, resource2: str, effect: float):
        self.resource1 = resource1
        self.resource2 = resource2
        self.effect = effect  # Positive for synergy, negative for competition

class Technology:
    def __init__(self, name: str, level: int = 0):
        self.name = name
        self.level = level
        self.max_level = 5
        self.effects = {
            'food': 0.1,  # 10% increase per level
            'water': 0.1,
            'energy': 0.15,
            'materials': 0.1,
            'population': 0.05
        }
        
    def upgrade(self) -> bool:
        if self.level < self.max_level:
            self.level += 1
            return True
        return False
        
    def reduce(self) -> bool:
        if self.level > 0:
            self.level -= 1
            return True
        return False
        
    def get_effect(self, resource: str) -> float:
        return 1.0 + (self.effects.get(resource, 0.0) * self.level)

class ResourceEconomy:
    def __init__(self):
        self.resources = {
            'food': 100.0,
            'water': 100.0,
            'energy': 100.0,
            'materials': 100.0,
            'population': 10.0,
            'technology': 0.0
        }
        
        self.technologies = {
            'agriculture': Technology('Agriculture'),
            'irrigation': Technology('Irrigation'),
            'mining': Technology('Mining'),
            'energy': Technology('Energy'),
            'medicine': Technology('Medicine')
        }
        
        # Define resource interactions
        self.interactions = [
            ResourceInteraction('food', 'water', 0.2),  # Food production needs water
            ResourceInteraction('energy', 'materials', 0.15),  # Energy production needs materials
            ResourceInteraction('population', 'food', -0.1),  # Population consumes food
            ResourceInteraction('population', 'water', -0.1),  # Population consumes water
            ResourceInteraction('technology', 'materials', -0.05),  # Technology development needs materials
            ResourceInteraction('technology', 'energy', -0.05)  # Technology development needs energy
        ]
        
    def update(self, delta_time: float, climate_effects: Dict[str, float]):
        # Apply technology effects
        for resource in self.resources:
            tech_multiplier = 1.0
            for tech in self.technologies.values():
                tech_multiplier *= tech.get_effect(resource)
            self.resources[resource] *= tech_multiplier
        
        # Apply resource interactions
        for interaction in self.interactions:
            resource1 = self.resources[interaction.resource1]
            resource2 = self.resources[interaction.resource2]
            
            # Calculate interaction effect
            effect = interaction.effect * resource1 * resource2 * delta_time
            
            # Apply effect to both resources
            self.resources[interaction.resource1] += effect
            self.resources[interaction.resource2] += effect
        
        # Apply climate effects
        temperature = climate_effects.get('temperature', 0.0)
        season = climate_effects.get('season', 0)
        
        # Temperature effects
        temp_factor = 1.0 + (temperature * 0.2)  # ±20% effect based on temperature
        self.resources['food'] *= temp_factor
        self.resources['water'] *= (1.0 - abs(temperature) * 0.1)  # Less water in extreme temperatures
        
        # Seasonal effects
        season_factors = {
            0: {'food': 1.2, 'water': 1.1},  # Spring
            1: {'food': 1.5, 'water': 0.8},  # Summer
            2: {'food': 1.0, 'water': 1.0},  # Fall
            3: {'food': 0.5, 'water': 0.9}   # Winter
        }
        
        season_factor = season_factors.get(season, {'food': 1.0, 'water': 1.0})
        self.resources['food'] *= season_factor['food']
        self.resources['water'] *= season_factor['water']
        
        # Ensure resources don't go below 0
        for resource in self.resources:
            self.resources[resource] = max(0.0, self.resources[resource])
            
    def upgrade_technology(self, tech_name: str) -> bool:
        if tech_name in self.technologies:
            return self.technologies[tech_name].upgrade()
        return False
        
    def reduce_technology(self, tech_name: str) -> bool:
        if tech_name in self.technologies:
            return self.technologies[tech_name].reduce()
        return False
        
    def get_technology_level(self, tech_name: str) -> int:
        return self.technologies.get(tech_name, Technology(tech_name)).level
        
    def draw(self, screen: pygame.Surface, x: int, y: int):
        font = pygame.font.Font(None, 24)
        
        # Draw resources
        for i, (resource, value) in enumerate(self.resources.items()):
            text = f"{resource.capitalize()}: {value:.1f}"
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (x, y + i * 25))
            
        # Draw technologies
        tech_y = y + len(self.resources) * 25 + 10
        for i, (tech_name, tech) in enumerate(self.technologies.items()):
            text = f"{tech_name.capitalize()}: Level {tech.level}/{tech.max_level}"
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (x, tech_y + i * 25)) 