import time
import pygame
import os
from collections import deque
from warehouse import Warehouse, Item
from robot import Robot
from utils import log_action
from ui import WarehouseUI

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Initialize the Warehouse object with a defined layout, racks, obstacles, etc.
warehouse_size = (10, 10)
# Create rack configuration with positions for all items
racks_config = {(1, 1): [], (2, 2): [], (3, 3): [], (4, 4): [], (5, 5): []}
obstacles = [(0, 0), (0, 1), (1, 0)]  # Example obstacles
charging_dock = (0, 2)
packing_station = (9, 9)

warehouse = Warehouse(warehouse_size, racks_config, obstacles, charging_dock, packing_station)

# Populate the warehouse racks with initial Item objects
items = [Item(item_id=f'item_{i}', name=f'Item {i}') for i in range(5)]
for i, item in enumerate(items):
    warehouse.add_item(item, (i + 1, i + 1))

# Initialize the Robot object at the charging dock
robot = Robot(robot_id='robot_1', current_location=charging_dock, battery_level=100)

# Create an Order Queue
order_queue = deque(['item_0', 'item_1', 'item_2'])

# Initialize the UI
ui = WarehouseUI(warehouse, robot)

# Main Simulation Loop
running = True
paused = False
simulation_speed = 0.5  # seconds between simulation steps
last_update_time = time.time()
pygame.init()  # Initialize pygame

# Function to add a new random order
def add_random_order():
    import random
    item_id = f"item_{random.randint(0, 4)}"
    order_queue.append(item_id)
    log_action('logs/order_log.txt', f"New order for item '{item_id}' added.")
    return f"Added order for {item_id}"

# Function to reset the simulation
def reset_simulation():
    global robot, order_queue
    robot = Robot(robot_id='robot_1', current_location=charging_dock, battery_level=100)
    order_queue = deque(['item_0', 'item_1', 'item_2'])
    log_action('logs/robot_log.txt', "Simulation reset.")
    return "Simulation reset"

while running:
    current_time = time.time()
    
    # Handle UI events
    event_result = ui.handle_events()
    if event_result == "toggle_pause":
        paused = not paused
    elif event_result == "speed_up":
        simulation_speed = max(0.1, simulation_speed - 0.1)
    elif event_result == "slow_down":
        simulation_speed = min(2.0, simulation_speed + 0.1)
    elif event_result == "add_order":
        add_random_order()
    elif event_result == "reset":
        reset_simulation()
    
    # Update simulation at specified intervals if not paused
    if not paused and current_time - last_update_time >= simulation_speed:
        # Check Robot Status
        if robot.battery_level < 25 and robot.status not in ['CHARGING', 'RETURNING_TO_DOCK']:
            robot.status = 'RETURNING_TO_DOCK'

        if robot.status == 'IDLE' and order_queue:
            order_item_id = order_queue.popleft()
            log_action('logs/order_log.txt', f"Order for item '{order_item_id}' received.")
            robot.status = 'FETCHING'
            robot.fetch_item(order_item_id, warehouse)

        elif robot.status == 'FETCHING':
            if robot.payload:
                robot.status = 'DELIVERING'
            elif robot.current_path:  # Continue moving if we have a path
                robot.current_path = robot.move(robot.current_path)
            else:  # Try fetching again if we reached the destination but didn't get the item
                item_id = None
                if order_queue and len(order_queue) > 0:
                    item_id = order_queue[0]
                if item_id:
                    robot.fetch_item(item_id, warehouse)

        elif robot.status == 'DELIVERING':
            robot.deliver_item(warehouse)
            if not robot.payload and not robot.current_path:  # If delivered and no more path
                log_action('logs/order_log.txt', "Order completed.")
                robot.status = 'IDLE'

        elif robot.status == 'RETURNING_TO_DOCK':
            robot.go_to_dock(warehouse)
            if not robot.current_path and robot.current_location == warehouse.charging_dock:
                robot.status = 'CHARGING'

        elif robot.status == 'CHARGING':
            robot.recharge()
            if robot.battery_level > 95:
                robot.status = 'IDLE'
                
        last_update_time = current_time
    
    # Update the UI with simulation status
    ui.update(paused, simulation_speed)