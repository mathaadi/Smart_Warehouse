class Item:
    def __init__(self, item_id, name):
        self.item_id = item_id
        self.name = name


class Warehouse:
    def __init__(self, size, racks_config, obstacles, dock, station):
        # Handle size as a tuple (width, height)
        width, height = size
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.graph = {}
        self.racks = {}
        self.obstacles = obstacles
        self.charging_dock = dock
        self.packing_station = station
        self.build_graph()
        self.initialize_racks(racks_config)

    def build_graph(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                if (x, y) not in self.obstacles:
                    self.graph[(x, y)] = []
                    if x > 0 and (x - 1, y) not in self.obstacles:
                        self.graph[(x, y)].append((x - 1, y))
                    if x < len(self.grid) - 1 and (x + 1, y) not in self.obstacles:
                        self.graph[(x, y)].append((x + 1, y))
                    if y > 0 and (x, y - 1) not in self.obstacles:
                        self.graph[(x, y)].append((x, y - 1))
                    if y < len(self.grid[x]) - 1 and (x, y + 1) not in self.obstacles:
                        self.graph[(x, y)].append((x, y + 1))

    def initialize_racks(self, racks_config):
        for location in racks_config:
            self.racks[location] = []

    def add_item(self, item, location):
        self.racks[location].append(item)
        self.log_inventory(f"Item '{item.name}' added to rack {location}.")

    def get_item_location(self, item_id):
        for location, stack in self.racks.items():
            for item in stack:
                if item.item_id == item_id:
                    return location
        return None

    def retrieve_item(self, location, item_id):
        stack = self.racks[location]
        temp_items = []
        while stack:
            item = stack.pop()
            temp_items.append(item)
            if item.item_id == item_id:
                self.log_inventory(f"Item '{item.name}' removed from rack {location}.")
                return item, temp_items[:-1]
        for temp_item in temp_items:
            stack.append(temp_item)
        return None, []

    def update_layout(self, new_obstacles):
        self.obstacles = new_obstacles
        self.build_graph()

    def log_inventory(self, message):
        from utils import log_action
        log_action('logs/inventory_log.txt', message)