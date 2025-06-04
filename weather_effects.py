import pygame
import random
import math
from typing import List, Tuple

class WeatherEffect:
    def __init__(self, x: float, y: float, speed: float, size: float):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.opacity = random.randint(100, 200)
        self.lifetime = random.uniform(1.0, 3.0)
        self.age = 0.0

    def update(self, delta_time: float) -> bool:
        self.age += delta_time
        if self.age >= self.lifetime:
            return False
        return True

    def draw(self, screen: pygame.Surface, camera_x: float, camera_y: float, zoom: float):
        pass

class RainDrop(WeatherEffect):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, random.uniform(200, 400), random.uniform(1, 3))
        self.length = random.uniform(5, 15)

    def update(self, delta_time: float) -> bool:
        self.y += self.speed * delta_time
        self.x += random.uniform(-10, 10) * delta_time
        return super().update(delta_time)

    def draw(self, screen: pygame.Surface, camera_x: float, camera_y: float, zoom: float):
        end_x = self.x + camera_x
        end_y = self.y + camera_y + self.length * zoom
        pygame.draw.line(
            screen,
            (200, 200, 255, int(self.opacity * (1 - self.age / self.lifetime))),
            (self.x + camera_x, self.y + camera_y),
            (end_x, end_y),
            int(self.size * zoom)
        )

class SnowFlake(WeatherEffect):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, random.uniform(50, 150), random.uniform(2, 4))
        self.angle = random.uniform(0, 2 * math.pi)
        self.rotation_speed = random.uniform(-2, 2)

    def update(self, delta_time: float) -> bool:
        self.y += self.speed * delta_time
        self.x += math.sin(self.angle) * 50 * delta_time
        self.angle += self.rotation_speed * delta_time
        return super().update(delta_time)

    def draw(self, screen: pygame.Surface, camera_x: float, camera_y: float, zoom: float):
        size = self.size * zoom
        points = []
        for i in range(6):
            angle = self.angle + (i * math.pi / 3)
            points.append((
                self.x + camera_x + math.cos(angle) * size,
                self.y + camera_y + math.sin(angle) * size
            ))
        
        pygame.draw.polygon(
            screen,
            (255, 255, 255, int(self.opacity * (1 - self.age / self.lifetime))),
            points
        )

class WeatherSystem:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_weather = 'clear'
        self.weather_intensity = 0.0
        self.effects: List[WeatherEffect] = []
        self.weather_change_timer = 0
        self.weather_change_delay = 10.0  # seconds

    def update(self, delta_time: float):
        # Update weather change timer
        self.weather_change_timer += delta_time
        if self.weather_change_timer >= self.weather_change_delay:
            self.weather_change_timer = 0
            self._change_weather()

        # Update existing effects
        self.effects = [effect for effect in self.effects if effect.update(delta_time)]

        # Spawn new effects based on current weather
        if self.current_weather == 'rain':
            self._spawn_rain(delta_time)
        elif self.current_weather == 'snow':
            self._spawn_snow(delta_time)

    def _change_weather(self):
        weathers = ['clear', 'rain', 'storm', 'snow']
        self.current_weather = random.choice(weathers)
        self.weather_intensity = random.uniform(0.5, 1.0)
        self.effects.clear()

    def _spawn_rain(self, delta_time: float):
        if random.random() < 0.3 * self.weather_intensity:
            x = random.uniform(0, self.screen_width)
            self.effects.append(RainDrop(x, -10))

    def _spawn_snow(self, delta_time: float):
        if random.random() < 0.2 * self.weather_intensity:
            x = random.uniform(0, self.screen_width)
            self.effects.append(SnowFlake(x, -10))

    def draw(self, screen: pygame.Surface, camera_x: float, camera_y: float, zoom: float):
        for effect in self.effects:
            effect.draw(screen, camera_x, camera_y, zoom) 