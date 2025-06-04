import pygame
import random
import math
from typing import Dict, List, Tuple, Optional

class Civilization:
    def __init__(self, name: str, color: Tuple[int, int, int]):
        self.name = name
        self.color = color
        self.territories: List[str] = []  # List of territory names
        self.resources = {
            'food': 100.0,
            'water': 100.0,
            'energy': 50.0,
            'materials': 50.0,
            'technology': 0.0
        }
        self.population = 0.0
        self.happiness = 0.5  # 0.0 to 1.0
        self.development = 0.0  # 0.0 to 1.0
        self.technology_levels = {
            'agriculture': 0,
            'industry': 0,
            'science': 0,
            'medicine': 0,
            'energy': 0
        }
        
    def update(self, delta_time: float, territory_resources: Dict[str, Dict[str, float]]):
        # Collect resources from territories
        for territory_name in self.territories:
            if territory_name in territory_resources:
                territory = territory_resources[territory_name]
                for resource in self.resources:
                    if resource in territory:
                        self.resources[resource] += territory[resource] * delta_time
        
        # Update technology effects
        tech_multipliers = {
            'agriculture': 1.0 + self.technology_levels['agriculture'] * 0.2,
            'industry': 1.0 + self.technology_levels['industry'] * 0.2,
            'science': 1.0 + self.technology_levels['science'] * 0.2,
            'medicine': 1.0 + self.technology_levels['medicine'] * 0.2,
            'energy': 1.0 + self.technology_levels['energy'] * 0.2
        }
        
        # Apply technology effects to resource production
        self.resources['food'] *= tech_multipliers['agriculture']
        self.resources['materials'] *= tech_multipliers['industry']
        self.resources['technology'] += self.technology_levels['science'] * 0.1 * delta_time
        self.resources['energy'] *= tech_multipliers['energy']
        
        # Update development based on resources and technology
        resource_factor = (self.resources['materials'] + self.resources['energy']) / 100.0
        tech_factor = sum(self.technology_levels.values()) / 25.0  # Max tech level is 5 per category
        self.development = min(1.0, self.development + (resource_factor + tech_factor) * 0.001 * delta_time)
        
        # Update happiness based on resources and development
        resource_happiness = min(1.0, (self.resources['food'] + self.resources['water']) / 200.0)
        self.happiness = (resource_happiness + self.development) / 2
        
    def can_claim_territory(self, territory_name: str, territory_development: float) -> bool:
        # Check if civilization has enough resources and development to claim territory
        required_development = 0.3  # Minimum development level needed
        required_resources = {
            'materials': 50.0,
            'energy': 30.0
        }
        
        if self.development < required_development:
            return False
            
        for resource, amount in required_resources.items():
            if self.resources[resource] < amount:
                return False
                
        return True
        
    def claim_territory(self, territory_name: str):
        if territory_name not in self.territories:
            self.territories.append(territory_name)
            # Deduct resources for claiming
            self.resources['materials'] -= 50.0
            self.resources['energy'] -= 30.0
            
    def upgrade_technology(self, tech_name: str) -> bool:
        if tech_name in self.technology_levels:
            current_level = self.technology_levels[tech_name]
            if current_level < 5:  # Max level is 5
                cost = (current_level + 1) * 50.0  # Increasing cost per level
                if self.resources['technology'] >= cost:
                    self.resources['technology'] -= cost
                    self.technology_levels[tech_name] += 1
                    return True
        return False
        
    def draw(self, screen: pygame.Surface, x: int, y: int):
        font = pygame.font.Font(None, 24)
        
        # Draw civilization name
        name_surface = font.render(self.name, True, self.color)
        screen.blit(name_surface, (x, y))
        
        # Draw resources
        resource_y = y + 30
        for resource, amount in self.resources.items():
            text = f"{resource.capitalize()}: {amount:.1f}"
            surface = font.render(text, True, (255, 255, 255))
            screen.blit(surface, (x, resource_y))
            resource_y += 25
            
        # Draw technology levels
        tech_y = resource_y + 10
        for tech, level in self.technology_levels.items():
            text = f"{tech.capitalize()}: Level {level}/5"
            surface = font.render(text, True, (255, 255, 255))
            screen.blit(surface, (x, tech_y))
            tech_y += 25
            
        # Draw development and happiness
        dev_text = f"Development: {self.development:.2f}"
        happy_text = f"Happiness: {self.happiness:.2f}"
        screen.blit(font.render(dev_text, True, (255, 255, 255)), (x, tech_y))
        screen.blit(font.render(happy_text, True, (255, 255, 255)), (x, tech_y + 25))

class CivilizationSystem:
    def __init__(self):
        self.civilizations: List[Civilization] = []
        self._initialize_civilizations()
        
    def _initialize_civilizations(self):
        # Create initial civilizations with different colors
        self.civilizations = [
            Civilization("Western Alliance", (0, 100, 255)),  # Blue
            Civilization("Eastern Federation", (255, 50, 50)),  # Red
            Civilization("Southern Union", (50, 255, 50)),  # Green
            Civilization("Northern Coalition", (255, 255, 50))  # Yellow
        ]
        
    def update(self, delta_time: float, territory_resources: Dict[str, Dict[str, float]]):
        for civ in self.civilizations:
            civ.update(delta_time, territory_resources)
            
    def draw(self, screen: pygame.Surface, x: int, y: int):
        for i, civ in enumerate(self.civilizations):
            civ.draw(screen, x, y + i * 300)  # Stack civilization panels vertically
            
    def get_civilization_by_name(self, name: str) -> Optional[Civilization]:
        for civ in self.civilizations:
            if civ.name == name:
                return civ
        return None
        
    def can_claim_territory(self, civ_name: str, territory_name: str, territory_development: float) -> bool:
        civ = self.get_civilization_by_name(civ_name)
        if civ:
            return civ.can_claim_territory(territory_name, territory_development)
        return False
        
    def claim_territory(self, civ_name: str, territory_name: str):
        civ = self.get_civilization_by_name(civ_name)
        if civ:
            civ.claim_territory(territory_name)
            
    def upgrade_technology(self, civ_name: str, tech_name: str) -> bool:
        civ = self.get_civilization_by_name(civ_name)
        if civ:
            return civ.upgrade_technology(tech_name)
        return False 