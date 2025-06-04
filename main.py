import pygame
import sys
import math
from pygame.locals import *
from game_objects import GameState, Civilization, Resources
from earth_visualization import EarthVisualization
from weather_effects import WeatherSystem
from climate_system import ClimateSystem
from resource_economy import ResourceEconomy
from population_system import PopulationSystem
from territory_system import TerritorySystem
from civilization_system import CivilizationSystem
from diplomacy_system import DiplomacySystem

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
YELLOW = (200, 200, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Earth Simulation Game")
        self.clock = pygame.time.Clock()
        
        # Initialize game state
        self.game_state = GameState()
        
        # Add a test civilization
        test_civ = Civilization.create_random_civilization("Test Civilization")
        self.game_state.add_civilization(test_civ)
        
        # Initialize Earth visualization
        self.earth = EarthVisualization(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Initialize weather system
        self.weather = WeatherSystem(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Initialize climate system
        self.climate = ClimateSystem(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Initialize resource economy
        self.resource_economy = ResourceEconomy()
        
        # Initialize population system
        self.population = PopulationSystem(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Initialize territory system
        self.territory = TerritorySystem()
        
        # Initialize civilization system
        self.civilization_system = CivilizationSystem()
        
        # Initialize diplomacy system
        civ_names = [civ.name for civ in self.civilization_system.civilizations]
        self.diplomacy_system = DiplomacySystem(civ_names)
        
        # Camera settings
        self.camera_x = 0
        self.camera_y = 0
        self.zoom = 1.0
        self.dragging = False
        self.last_mouse_pos = None
        
        # UI settings
        self.font = pygame.font.Font(None, 24)
        
        # Speed control
        self.speed_multiplier = 1.0
        self.speed_levels = [0.25, 0.5, 1.0, 2.0, 4.0]
        self.current_speed_index = 2  # Start at normal speed (1.0)
        
        # Territory selection
        self.selected_territory = None
        
        # Territory name rect map
        self.territory_name_rect_map = {}
        
        # Diplomacy panel toggle
        self.show_diplomacy = True
        self.diplomacy_panel_rect = pygame.Rect(WINDOW_WIDTH - 450, 10, 200, 40)  # Shifted left
        self.diplomacy_content_rect = pygame.Rect(WINDOW_WIDTH - 500, 60, 240, 300)  # Keep content panel position
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.dragging = True
                    self.last_mouse_pos = pygame.mouse.get_pos()
                    # Check if weather button is clicked
                    if hasattr(self, 'weather_button_rect') and self.weather_button_rect.collidepoint(event.pos):
                        self.weather._change_weather()
                    # Check if speed button is clicked
                    if hasattr(self, 'speed_button_rect') and self.speed_button_rect.collidepoint(event.pos):
                        self.current_speed_index = (self.current_speed_index + 1) % len(self.speed_levels)
                        self.speed_multiplier = self.speed_levels[self.current_speed_index]
                    # Check if technology upgrade buttons are clicked
                    for tech_name, buttons in self.tech_button_rects.items():
                        if buttons['upgrade'] and buttons['upgrade'].collidepoint(event.pos):
                            self.resource_economy.upgrade_technology(tech_name)
                        elif buttons['reduce'] and buttons['reduce'].collidepoint(event.pos):
                            self.resource_economy.reduce_technology(tech_name)
                    # Check for territory name click
                    for rect_tuple, territory in self.territory_name_rect_map.items():
                        left, top, right, bottom = rect_tuple
                        if left <= event.pos[0] <= right and top <= event.pos[1] <= bottom:
                            self.selected_territory = territory
                            break
                    else:
                        # If not on a name, check for territory selection by position
                        mouse_x, mouse_y = event.pos
                        world_x = (mouse_x - WINDOW_WIDTH/2) / self.zoom + self.camera_x
                        world_y = (mouse_y - WINDOW_HEIGHT/2) / self.zoom + self.camera_y
                        self.selected_territory = self.territory.get_territory_at(world_x, world_y)
                    # Toggle diplomacy panel
                    if self.diplomacy_panel_rect.collidepoint(event.pos):
                        self.show_diplomacy = not self.show_diplomacy
                    # For demonstration: click on diplomacy panel to cycle relationship between first two civs
                    if self.show_diplomacy and self.diplomacy_panel_rect.collidepoint(event.pos):
                        civs = self.civilization_system.civilizations
                        if len(civs) >= 2:
                            rel = self.diplomacy_system.get_relationship(civs[0].name, civs[1].name)
                            if rel == 'neutral':
                                self.diplomacy_system.propose_alliance(civs[0].name, civs[1].name)
                            elif rel == 'allied':
                                self.diplomacy_system.declare_war(civs[0].name, civs[1].name)
                            else:
                                self.diplomacy_system.make_peace(civs[0].name, civs[1].name)
                elif event.button == 4:  # Mouse wheel up
                    self.zoom = min(2.0, self.zoom + 0.1)
                elif event.button == 5:  # Mouse wheel down
                    self.zoom = max(0.5, self.zoom - 0.1)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            elif event.type == MOUSEMOTION:
                if self.dragging and self.last_mouse_pos:
                    current_pos = pygame.mouse.get_pos()
                    dx = current_pos[0] - self.last_mouse_pos[0]
                    dy = current_pos[1] - self.last_mouse_pos[1]
                    self.camera_x += dx
                    self.camera_y += dy
                    self.last_mouse_pos = current_pos
                else:
                    # Update territory hover states
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    world_x = (mouse_x - WINDOW_WIDTH/2) / self.zoom + self.camera_x
                    world_y = (mouse_y - WINDOW_HEIGHT/2) / self.zoom + self.camera_y
                    for territory in self.territory.territories:
                        territory.is_hovered = False
                    hovered_territory = self.territory.get_territory_at(world_x, world_y)
                    if hovered_territory:
                        hovered_territory.is_hovered = True

    def draw_ui(self):
        # Draw resource information
        if self.game_state.civilizations:
            civ = self.game_state.civilizations[0]  # Show first civilization's resources
            resources = civ.resources
            
            # Create resource display
            resource_texts = [
                f"Food: {resources.food:.1f}",
                f"Water: {resources.water:.1f}",
                f"Energy: {resources.energy:.1f}",
                f"Materials: {resources.materials:.1f}",
                f"Population: {resources.population:.1f}",
                f"Technology: {resources.technology:.1f}"
            ]
            
            # Draw resource panel
            panel_width = 200
            panel_height = len(resource_texts) * 25 + 10
            panel_rect = pygame.Rect(10, 10, panel_width, panel_height)
            pygame.draw.rect(self.screen, GRAY, panel_rect)
            pygame.draw.rect(self.screen, WHITE, panel_rect, 2)
            
            # Draw resource text
            for i, text in enumerate(resource_texts):
                text_surface = self.font.render(text, True, WHITE)
                self.screen.blit(text_surface, (20, 20 + i * 25))
            
            # Draw weather information
            weather_text = f"Weather: {self.weather.current_weather}"
            weather_surface = self.font.render(weather_text, True, WHITE)
            weather_x = 20
            weather_y = panel_height + 20
            self.screen.blit(weather_surface, (weather_x, weather_y))
            
            # Draw weather change button
            button_text = "Change"
            button_surface = self.font.render(button_text, True, BLACK)
            button_width = button_surface.get_width() + 20
            button_height = button_surface.get_height() + 10
            button_x = weather_x + weather_surface.get_width() + 20
            button_y = weather_y - 5
            self.weather_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(self.screen, YELLOW, self.weather_button_rect)
            pygame.draw.rect(self.screen, WHITE, self.weather_button_rect, 2)
            self.screen.blit(button_surface, (button_x + 10, button_y + 5))
            
            # Draw speed control
            speed_text = f"Speed: {self.speed_multiplier}x"
            speed_surface = self.font.render(speed_text, True, WHITE)
            speed_x = button_x + button_width + 20
            speed_y = weather_y
            self.screen.blit(speed_surface, (speed_x, speed_y))
            
            # Draw speed change button
            speed_button_text = "Change"
            speed_button_surface = self.font.render(speed_button_text, True, BLACK)
            speed_button_width = speed_button_surface.get_width() + 20
            speed_button_height = speed_button_surface.get_height() + 10
            speed_button_x = speed_x + speed_surface.get_width() + 20
            speed_button_y = speed_y - 5
            self.speed_button_rect = pygame.Rect(speed_button_x, speed_button_y, speed_button_width, speed_button_height)
            pygame.draw.rect(self.screen, GREEN, self.speed_button_rect)
            pygame.draw.rect(self.screen, WHITE, self.speed_button_rect, 2)
            self.screen.blit(speed_button_surface, (speed_button_x + 10, speed_button_y + 5))
            
            # Draw technology panel
            tech_panel_x = WINDOW_WIDTH - 250
            tech_panel_y = 10
            tech_panel_width = 240
            tech_panel_height = 200
            tech_panel_rect = pygame.Rect(tech_panel_x, tech_panel_y, tech_panel_width, tech_panel_height)
            pygame.draw.rect(self.screen, GRAY, tech_panel_rect)
            pygame.draw.rect(self.screen, WHITE, tech_panel_rect, 2)
            
            # Draw technology information and upgrade/reduce buttons
            self.tech_button_rects = {}
            for i, (tech_name, tech) in enumerate(self.resource_economy.technologies.items()):
                tech_text = f"{tech_name.capitalize()}: Level {tech.level}/{tech.max_level}"
                tech_surface = self.font.render(tech_text, True, WHITE)
                text_x = tech_panel_x + 10
                text_y = tech_panel_y + 10 + i * 40
                self.screen.blit(tech_surface, (text_x, text_y))

                # Button positions to the right of the text
                button_y = text_y
                button_x_start = text_x + tech_surface.get_width() + 20
                button_gap = 6
                button_width = 36
                button_height = 28

                # Draw upgrade button if not at max level
                if tech.level < tech.max_level:
                    upgrade_text = "Up"
                    upgrade_surface = self.font.render(upgrade_text, True, BLACK)
                    upgrade_rect = pygame.Rect(button_x_start, button_y, button_width, button_height)
                    pygame.draw.rect(self.screen, YELLOW, upgrade_rect)
                    pygame.draw.rect(self.screen, WHITE, upgrade_rect, 2)
                    self.screen.blit(upgrade_surface, (button_x_start + 8, button_y + 5))
                else:
                    upgrade_rect = None

                # Draw reduce button if level is greater than 0
                if tech.level > 0:
                    reduce_text = "Down"
                    reduce_surface = self.font.render(reduce_text, True, BLACK)
                    reduce_rect = pygame.Rect(button_x_start + button_width + button_gap, button_y, button_width, button_height)
                    pygame.draw.rect(self.screen, RED, reduce_rect)
                    pygame.draw.rect(self.screen, WHITE, reduce_rect, 2)
                    self.screen.blit(reduce_surface, (button_x_start + button_width + button_gap + 2, button_y + 5))
                else:
                    reduce_rect = None

                # Store both button rects
                self.tech_button_rects[tech_name] = {
                    'upgrade': upgrade_rect,
                    'reduce': reduce_rect
                }
            
            # Draw population panel
            pop_panel_x = WINDOW_WIDTH - 250
            pop_panel_y = tech_panel_y + tech_panel_height + 20
            self.population.draw(self.screen, pop_panel_x, pop_panel_y)
            
            # Draw territory information if a territory is selected
            if self.selected_territory:
                territory = self.selected_territory
                territory_panel_x = WINDOW_WIDTH - 250
                territory_panel_y = pop_panel_y + 200
                territory_panel_width = 240
                territory_panel_height = 200
                
                # Draw territory panel
                territory_panel_rect = pygame.Rect(territory_panel_x, territory_panel_y, territory_panel_width, territory_panel_height)
                pygame.draw.rect(self.screen, GRAY, territory_panel_rect)
                pygame.draw.rect(self.screen, WHITE, territory_panel_rect, 2)
                
                # Draw territory information
                info_texts = [
                    f"Territory: {territory.name}",
                    f"Development: {territory.development:.2f}",
                    f"Food: {territory.resources['food']:.1f}",
                    f"Water: {territory.resources['water']:.1f}",
                    f"Energy: {territory.resources['energy']:.1f}",
                    f"Materials: {territory.resources['materials']:.1f}"
                ]
                
                for i, text in enumerate(info_texts):
                    text_surface = self.font.render(text, True, WHITE)
                    self.screen.blit(text_surface, (territory_panel_x + 10, territory_panel_y + 10 + i * 25))

        # Draw diplomacy button
        button_color = (50, 50, 100) if not self.show_diplomacy else (70, 70, 120)
        pygame.draw.rect(self.screen, button_color, self.diplomacy_panel_rect)
        pygame.draw.rect(self.screen, WHITE, self.diplomacy_panel_rect, 2)
        
        # Draw button text
        button_font = pygame.font.Font(None, 24)
        button_text = "Diplomacy Panel"
        text_surface = button_font.render(button_text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.diplomacy_panel_rect.center)
        self.screen.blit(text_surface, text_rect)
        
        # Draw diplomacy content if panel is shown
        if self.show_diplomacy:
            pygame.draw.rect(self.screen, (50, 50, 100), self.diplomacy_content_rect)
            pygame.draw.rect(self.screen, WHITE, self.diplomacy_content_rect, 2)
            content_font = pygame.font.Font(None, 22)
            self.diplomacy_system.draw(self.screen, content_font, 
                                     self.diplomacy_content_rect.x + 10, 
                                     self.diplomacy_content_rect.y + 10, 
                                     self.civilization_system.civilizations)

    def run(self):
        last_time = pygame.time.get_ticks()
        
        while True:
            current_time = pygame.time.get_ticks()
            delta_time = (current_time - last_time) / 1000.0  # Convert to seconds
            last_time = current_time
            
            # Apply speed multiplier to delta_time
            delta_time *= self.speed_multiplier
            
            self.handle_events()
            
            # Update game state
            self.game_state.update(delta_time)
            
            # Update Earth visualization
            self.earth.update(delta_time)
            
            # Update weather
            self.weather.update(delta_time)
            
            # Update climate
            self.climate.update(delta_time)
            
            # Update resource economy with climate effects
            climate_effects = self.climate.get_climate_effects()
            self.resource_economy.update(delta_time, climate_effects)
            
            # Update population with climate effects and resources
            total_population = self.population.update(delta_time, climate_effects, self.resource_economy.resources)
            
            # Update territory system
            self.territory.update(delta_time, climate_effects)
            
            # Update civilization system with territory resources
            # Update civilization population
            if self.game_state.civilizations:
                self.game_state.civilizations[0].resources.population = total_population
            
            # Clear screen
            self.screen.fill(BLACK)
            
            # Draw Earth and clouds
            self.earth.draw(self.screen, self.camera_x, self.camera_y, self.zoom)
            
            # Draw territories and get name rect map for click detection
            self.territory_name_rect_map = self.territory.draw(self.screen, self.camera_x, self.camera_y, self.zoom)
            
            # Draw weather effects
            self.weather.draw(self.screen, self.camera_x, self.camera_y, self.zoom)
            
            # Draw climate information
            self.climate.draw(self.screen, self.camera_x, self.camera_y, self.zoom)
            
            # Draw UI
            self.draw_ui()
            
            # Update display
            pygame.display.flip()
            
            # Cap the frame rate
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run() 