from dataclasses import dataclass
from typing import Dict, List
import random

@dataclass
class Resources:
    food: float = 100.0
    water: float = 100.0
    energy: float = 100.0
    materials: float = 100.0
    population: float = 100.0
    technology: float = 0.0

    # Resource caps
    MAX_FOOD = 1000.0
    MAX_WATER = 1000.0
    MAX_ENERGY = 1000.0
    MAX_MATERIALS = 1000.0
    MAX_POPULATION = 1000.0
    MAX_TECHNOLOGY = 100.0

    def update(self, delta_time: float):
        # Calculate resource changes
        food_change = (self.population * 0.05 - self.population * 0.1) * delta_time
        water_change = (self.population * 0.05 - self.population * 0.1) * delta_time
        energy_change = (self.technology * 0.05 - self.population * 0.02) * delta_time
        materials_change = (self.technology * 0.02) * delta_time
        
        # Population growth depends on available food and water
        population_growth = min(
            self.food * 0.001,
            self.water * 0.001,
            self.energy * 0.0005
        ) * delta_time
        
        # Technology growth depends on population and available energy
        tech_growth = (self.population * 0.0001 * min(1.0, self.energy / 100.0)) * delta_time

        # Apply changes with caps
        self.food = max(0, min(self.MAX_FOOD, self.food + food_change))
        self.water = max(0, min(self.MAX_WATER, self.water + water_change))
        self.energy = max(0, min(self.MAX_ENERGY, self.energy + energy_change))
        self.materials = max(0, min(self.MAX_MATERIALS, self.materials + materials_change))
        self.population = max(0, min(self.MAX_POPULATION, self.population + population_growth))
        self.technology = max(0, min(self.MAX_TECHNOLOGY, self.technology + tech_growth))

class Civilization:
    def __init__(self, name: str, traits: Dict[str, float]):
        self.name = name
        self.traits = traits
        self.resources = Resources()
        self.territory = []  # List of coordinates this civilization controls
        self.relations = {}  # Relations with other civilizations

    def update(self, delta_time: float):
        # Apply trait bonuses to resource generation
        self.resources.food *= (1 + self.traits.get('agricultural_bonus', 0))
        self.resources.technology *= (1 + self.traits.get('scientific_bonus', 0))
        self.resources.energy *= (1 + self.traits.get('industrial_bonus', 0))
        
        # Update resources
        self.resources.update(delta_time)

    @staticmethod
    def create_random_civilization(name: str) -> 'Civilization':
        traits = {
            'agricultural_bonus': random.uniform(0, 0.5),
            'scientific_bonus': random.uniform(0, 0.5),
            'industrial_bonus': random.uniform(0, 0.5),
            'military_bonus': random.uniform(0, 0.5),
            'diplomatic_bonus': random.uniform(0, 0.5)
        }
        return Civilization(name, traits)

class GameState:
    def __init__(self):
        self.civilizations: List[Civilization] = []
        self.time_scale = 1.0
        self.current_time = 0.0
        self.natural_disasters = []
        self.weather_system = WeatherSystem()

    def add_civilization(self, civilization: Civilization):
        self.civilizations.append(civilization)

    def update(self, delta_time: float):
        scaled_delta = delta_time * self.time_scale
        self.current_time += scaled_delta

        # Update all civilizations
        for civ in self.civilizations:
            civ.update(scaled_delta)

        # Update weather and natural disasters
        self.weather_system.update(scaled_delta)
        self.update_natural_disasters(scaled_delta)

    def update_natural_disasters(self, delta_time: float):
        # Random chance of natural disasters
        if random.random() < 0.001 * delta_time:
            disaster_type = random.choice(['earthquake', 'hurricane', 'volcanic_eruption'])
            self.natural_disasters.append({
                'type': disaster_type,
                'position': (random.randint(0, 1000), random.randint(0, 1000)),
                'intensity': random.uniform(0.5, 1.0),
                'duration': random.uniform(5.0, 20.0)
            })

class WeatherSystem:
    def __init__(self):
        self.weather_patterns = {}
        self.current_weather = 'clear'
        self.weather_intensity = 0.0

    def update(self, delta_time: float):
        # Simple weather system - will be expanded later
        if random.random() < 0.01 * delta_time:
            self.current_weather = random.choice(['clear', 'rain', 'storm', 'snow'])
            self.weather_intensity = random.uniform(0.0, 1.0) 