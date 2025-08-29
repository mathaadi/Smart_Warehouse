import pygame
import sys
from warehouse import Warehouse, Item
from robot import Robot

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class WarehouseUI:
    def __init__(self, warehouse, robot, cell_size=50):
        pygame.init()
        self.warehouse = warehouse
        self.robot = robot
        self.cell_size = cell_size
        self.width = warehouse.grid[0].__len__() * cell_size
        self.height = warehouse.grid.__len__() * cell_size
        self.info_panel_width = 300
        
        # Create the display surface
        self.screen = pygame.display.set_mode((self.width + self.info_panel_width, self.height))
        pygame.display.set_caption("Smart Warehouse Simulation")
        
        # Font for text rendering
        self.font = pygame.font.SysFont(None, 24)
        
        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
        
    def draw_grid(self):
        # Draw the warehouse grid
        for x in range(len(self.warehouse.grid)):
            for y in range(len(self.warehouse.grid[x])):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                  self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, WHITE, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)  # Grid lines
                
                # Draw obstacles
                if (x, y) in self.warehouse.obstacles:
                    pygame.draw.rect(self.screen, BLACK, rect)
                
                # Draw racks
                if (x, y) in self.warehouse.racks:
                    rack_rect = pygame.Rect(x * self.cell_size + 5, y * self.cell_size + 5, 
                                         self.cell_size - 10, self.cell_size - 10)
                    pygame.draw.rect(self.screen, BLUE, rack_rect)
                    
                    # Show number of items in rack
                    items_count = len(self.warehouse.racks[(x, y)])
                    if items_count > 0:
                        text = self.font.render(str(items_count), True, WHITE)
                        text_rect = text.get_rect(center=(x * self.cell_size + self.cell_size // 2, 
                                                         y * self.cell_size + self.cell_size // 2))
                        self.screen.blit(text, text_rect)
                
                # Draw charging dock
                if (x, y) == self.warehouse.charging_dock:
                    dock_rect = pygame.Rect(x * self.cell_size + 5, y * self.cell_size + 5, 
                                          self.cell_size - 10, self.cell_size - 10)
                    pygame.draw.rect(self.screen, YELLOW, dock_rect)
                    
                # Draw packing station
                if (x, y) == self.warehouse.packing_station:
                    station_rect = pygame.Rect(x * self.cell_size + 5, y * self.cell_size + 5, 
                                             self.cell_size - 10, self.cell_size - 10)
                    pygame.draw.rect(self.screen, GREEN, station_rect)
    
    def draw_robot(self):
        # Draw the robot
        x, y = self.robot.current_location
        robot_rect = pygame.Rect(x * self.cell_size + 10, y * self.cell_size + 10, 
                               self.cell_size - 20, self.cell_size - 20)
        
        # Change robot color based on status
        robot_color = RED
        if self.robot.status == 'CHARGING':
            robot_color = YELLOW
        elif self.robot.status == 'FETCHING' or self.robot.status == 'DELIVERING':
            robot_color = GREEN
            
        pygame.draw.rect(self.screen, robot_color, robot_rect)
        
        # Draw battery level indicator
        battery_width = int((self.cell_size - 20) * (self.robot.battery_level / 100))
        battery_rect = pygame.Rect(x * self.cell_size + 10, y * self.cell_size + 5, 
                                 battery_width, 5)
        pygame.draw.rect(self.screen, GREEN, battery_rect)
    
    def draw_info_panel(self, paused=False, simulation_speed=0.5):
        # Draw the information panel
        panel_rect = pygame.Rect(self.width, 0, self.info_panel_width, self.height)
        pygame.draw.rect(self.screen, GRAY, panel_rect)
        
        # Simulation status
        status_text = "PAUSED" if paused else "RUNNING"
        status_color = RED if paused else GREEN
        text = self.font.render(f"Simulation: {status_text}", True, status_color)
        self.screen.blit(text, (self.width + 10, 20))
        
        # Simulation speed
        speed_text = f"Speed: {1/simulation_speed:.1f}x"
        text = self.font.render(speed_text, True, BLACK)
        self.screen.blit(text, (self.width + 10, 50))
        
        # Robot information
        robot_info = [
            f"Robot ID: {self.robot.robot_id}",
            f"Status: {self.robot.status}",
            f"Battery: {self.robot.battery_level}%",
            f"Location: {self.robot.current_location}",
            f"Payload: {self.robot.payload.item_id if self.robot.payload else 'None'}"
        ]
        
        y_offset = 90
        text = self.font.render("Robot Information:", True, BLUE)
        self.screen.blit(text, (self.width + 10, y_offset))
        y_offset += 30
        
        for info in robot_info:
            text = self.font.render(info, True, BLACK)
            self.screen.blit(text, (self.width + 10, y_offset))
            y_offset += 30
        
        # Warehouse information
        y_offset += 20
        text = self.font.render("Warehouse Information:", True, BLUE)
        self.screen.blit(text, (self.width + 10, y_offset))
        y_offset += 30
        
        warehouse_info = [
            f"Size: {len(self.warehouse.grid)}x{len(self.warehouse.grid[0])}",
            f"Racks: {len(self.warehouse.racks)}",
            f"Obstacles: {len(self.warehouse.obstacles)}"
        ]
        
        for info in warehouse_info:
            text = self.font.render(info, True, BLACK)
            self.screen.blit(text, (self.width + 10, y_offset))
            y_offset += 30
            
        # Legend
        y_offset += 20
        text = self.font.render("Legend:", True, BLUE)
        self.screen.blit(text, (self.width + 10, y_offset))
        y_offset += 30
        
        legend_items = [
            ("Robot", RED),
            ("Charging Dock", YELLOW),
            ("Packing Station", GREEN),
            ("Rack", BLUE),
            ("Obstacle", BLACK)
        ]
        
        for label, color in legend_items:
            pygame.draw.rect(self.screen, color, (self.width + 10, y_offset, 20, 20))
            text = self.font.render(label, True, BLACK)
            self.screen.blit(text, (self.width + 40, y_offset))
            y_offset += 30
            
        # Controls information
        y_offset += 20
        text = self.font.render("Controls:", True, BLUE)
        self.screen.blit(text, (self.width + 10, y_offset))
        y_offset += 30
        
        controls = [
            "SPACE: Pause/Resume",
            "UP: Speed up",
            "DOWN: Slow down",
            "O: Add new order",
            "R: Reset simulation"
        ]
        
        for control in controls:
            text = self.font.render(control, True, BLACK)
            self.screen.blit(text, (self.width + 10, y_offset))
            y_offset += 30
    
    def update(self, paused=False, simulation_speed=0.5):
        # Clear the screen
        self.screen.fill(WHITE)
        
        # Draw the warehouse components
        self.draw_grid()
        self.draw_robot()
        self.draw_info_panel(paused, simulation_speed)
        
        # Update the display
        pygame.display.flip()
        
        # Control the frame rate
        self.clock.tick(30)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Handle key presses
            elif event.type == pygame.KEYDOWN:
                # Pause/Resume simulation with Space
                if event.key == pygame.K_SPACE:
                    return "toggle_pause"
                # Speed up simulation with Up arrow
                elif event.key == pygame.K_UP:
                    return "speed_up"
                # Slow down simulation with Down arrow
                elif event.key == pygame.K_DOWN:
                    return "slow_down"
                # Add new random order with 'O' key
                elif event.key == pygame.K_o:
                    return "add_order"
                # Reset simulation with 'R' key
                elif event.key == pygame.K_r:
                    return "reset"
        
        return None
    
    def run(self, paused=False, simulation_speed=0.5):
        # This method is kept for compatibility but is not used in the main loop
        # The main loop in main.py handles the simulation and UI updates
        event_result = self.handle_events()
        self.update(paused, simulation_speed)
        return event_result