import time
from utils import log_action
from pathfinding import a_star_search

class Robot:
    def __init__(self, robot_id, current_location, battery_level=100):
        self.robot_id = robot_id
        self.current_location = current_location  # (x, y) tuple
        self.battery_level = battery_level  # 0 to 100
        self.payload = None  # Item object or None
        self.status = 'IDLE'  # IDLE, FETCHING, DELIVERING, CHARGING, RETURNING_TO_DOCK
        self.current_path = []  # Current path the robot is following

    def move(self, path):
        if not path:
            return
            
        # Move one step at a time
        next_step = path[0]
        self.current_location = next_step
        self.battery_level -= 1  # Deplete battery with each move
        log_action('logs/robot_log.txt', f'Robot moving to {self.current_location}.')
        
        if self.battery_level <= 0:
            log_action('logs/robot_log.txt', 'Battery depleted. Robot needs to recharge.')
            return path[1:]
            
        return path[1:] if len(path) > 1 else []

    def fetch_item(self, item_id, warehouse):
        log_action('logs/order_log.txt', f'Order for item {item_id} received.')
        location = warehouse.get_item_location(item_id)
        if location:
            # Store the path as an instance variable
            self.current_path = a_star_search(warehouse.graph, self.current_location, location)
            # Move one step and update the path
            self.current_path = self.move(self.current_path)
            
            # Check if we've reached the destination
            if not self.current_path and self.current_location == location:
                items_moved = warehouse.retrieve_item(location, item_id)
                self.payload = items_moved[0] if items_moved else None
                log_action('logs/order_log.txt', f'Order for item {item_id} completed.')
        else:
            log_action('logs/order_log.txt', f'Item {item_id} not found in warehouse.')

    def deliver_item(self, warehouse):
        if self.payload:
            # Initialize path if not already set
            if not hasattr(self, 'current_path') or not self.current_path:
                self.current_path = a_star_search(warehouse.graph, self.current_location, warehouse.packing_station)
            
            # Move one step and update the path
            self.current_path = self.move(self.current_path)
            
            # Check if we've reached the destination
            if not self.current_path and self.current_location == warehouse.packing_station:
                log_action('logs/robot_log.txt', f'Item {self.payload.item_id} delivered to packing station.')
                self.payload = None  # Clear payload after delivery

    def recharge(self):
        # Increase battery level by 5% each time recharge is called
        if self.battery_level < 100:
            self.battery_level = min(100, self.battery_level + 5)  # Simulate charging
            log_action('logs/robot_log.txt', f'Charging... Battery level: {self.battery_level}%.')

    def go_to_dock(self, warehouse):
        # Initialize path if not already set
        if not hasattr(self, 'current_path') or not self.current_path:
            self.current_path = a_star_search(warehouse.graph, self.current_location, warehouse.charging_dock)
        
        # Move one step and update the path
        self.current_path = self.move(self.current_path)
        
        # Check if we've reached the destination
        if not self.current_path and self.current_location == warehouse.charging_dock:
            log_action('logs/robot_log.txt', 'Robot arrived at charging dock. Starting recharge.')