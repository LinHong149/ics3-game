import pygame
import pytmx
import csv
from pytmx.util_pygame import load_pygame

class Map:
    gid_list = []
    def __init__(self, filename, scale):
        self.tmx_data = load_pygame(filename)
        self.scale = scale
        self.width = self.tmx_data.width * self.tmx_data.tilewidth * self.scale
        self.height = self.tmx_data.height * self.tmx_data.tileheight * self.scale
        self.surface = pygame.Surface((self.width, self.height))
        self.filename = filename
        self.make_map()

    def make_map(self):
        self.layers = []
        for layer in self.tmx_data.visible_layers:
            layer_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    # if gid not in self.gid_list:
                    #     self.gid_list.append(gid)
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(tile, (tile.get_width() * self.scale, tile.get_height() * self.scale))
                        layer_surface.blit(tile, (x * self.tmx_data.tilewidth * self.scale, y * self.tmx_data.tileheight * self.scale))
            self.layers.append(layer_surface)
        # print(self.gid_list)

    def render_layer(self, screen, camera, layer_index):
        screen.blit(self.layers[layer_index], camera.apply_rect(self.layers[layer_index].get_rect()))

    def render_layers(self, screen, camera, below_player_layers, above_player_layers):
        for layer_index in below_player_layers:
            self.render_layer(screen, camera, layer_index)
        for layer_index in above_player_layers:
            self.render_layer(screen, camera, layer_index)

    def get_tile_properties(self, x, y, layer):
        if 0 <= x < self.tmx_data.width and 0 <= y < self.tmx_data.height:
            for tile_x, tile_y, gid in layer.tiles():
                # if int(tile_x) == x and int(tile_y) == y:
                    # print(layer, tile_x, tile_y, x, y, layer.data[tile_y][tile_x])
                if tile_x == x and tile_y == y:
                    gid = layer.data[tile_y+1][tile_x+1]
                    # print("gid", gid, "tile property", self.tmx_data.get_tile_properties_by_gid(gid), "layer", layer)
                    # print(self.tmx_data.get_tile_properties_by_gid(gid))
                    return self.tmx_data.get_tile_properties_by_gid(gid)
        return None

    def check_collision(self, x, y):
        for layer in self.tmx_data.visible_layers:
            # if isinstance(layer, pytmx.TiledTileLayer):
            properties = self.get_tile_properties(x, y, layer)
            # print(layer, properties)
            if properties and 'Collision' in properties and properties['Collision'] == True:
                # print(layer, properties, "has collision")
                return True
        return False

    # def test(self, x, y):
    #     tile_x = int(x // (self.tmx_data.tilewidth * self.scale))
    #     tile_y = int(y // (self.tmx_data.tileheight * self.scale))
    #     tile_layer = self.tmx_data.get_layer_by_name("Map")
    #     gid = tile_layer.data[tile_y][tile_x]
    #     return(tile_layer.data, gid, tile_x, tile_y)
        
    def expand_land(self, x, y, direction, inventory):
        if "dirt" in inventory.get_items() and inventory.get_items()["dirt"] > 0:
            layer = self.tmx_data.get_layer_by_name("Map")
            # Makes the current tile the one in front of the player
            grass_block = 39
            print(direction)
            match direction:
                case "u":
                    target_tile = (y, x+1)
                case "d":
                    target_tile = (y+2, x+1)
                case "l":
                    target_tile = (y+1, x)
                case "r":
                    target_tile = (y+1, x+2)
            current_tile = layer.data[target_tile[0]][target_tile[1]]
            # If not grass tile
            if current_tile != grass_block:
                layer.data[target_tile[0]][target_tile[1]] = grass_block
                self.make_map()
                inventory.remove_item("dirt")
            print(current_tile)

    def hoe_land(self, x, y, direction):
            layer = self.tmx_data.get_layer_by_name("Map")
            # Makes the current tile the one in front of the player
            dry_dirt_block = 17
            print(direction)
            match direction:
                case "u":
                    target_tile = (y, x+1)
                case "d":
                    target_tile = (y+2, x+1)
                case "l":
                    target_tile = (y+1, x)
                case "r":
                    target_tile = (y+1, x+2)
            current_tile = layer.data[target_tile[0]][target_tile[1]]
            # If not grass tile
            if current_tile != dry_dirt_block:
                layer.data[target_tile[0]][target_tile[1]] = dry_dirt_block
                self.make_map()

    def water_land(self, x, y, direction):
        layer = self.tmx_data.get_layer_by_name("Map")
        # Makes the current tile the one in front of the player
        dry_dirt_block = 17
        wet_dirt_block = 23
        print(direction)
        match direction:
            case "u":
                target_tile = (y, x+1)
            case "d":
                target_tile = (y+2, x+1)
            case "l":
                target_tile = (y+1, x)
            case "r":
                target_tile = (y+1, x+2)
        current_tile = layer.data[target_tile[0]][target_tile[1]]
        # If not grass tile
        if current_tile == dry_dirt_block:
            layer.data[target_tile[0]][target_tile[1]] = wet_dirt_block
            self.make_map()

    def plant_seed(self, x, y, direction, inventory):
        if "carrot_seeds" in inventory.get_items() and inventory.get_items()["carrot_seeds"] > 0:
            map_layer = self.tmx_data.get_layer_by_name("Map")
            nature_layer = self.tmx_data.get_layer_by_name("Nature")
            # Makes the current tile the one in front of the player
            wet_dirt_block = 23
            seed_block = 83
            print(direction)
            match direction:
                case "u":
                    target_tile = (y, x+1)
                case "d":
                    target_tile = (y+2, x+1)
                case "l":
                    target_tile = (y+1, x)
                case "r":
                    target_tile = (y+1, x+2)
            current_map_tile = map_layer.data[target_tile[0]][target_tile[1]]
            current_nature_tile = nature_layer.data[target_tile[0]][target_tile[1]]
            # If not grass tile
            if current_map_tile == wet_dirt_block and current_nature_tile == 0:
                nature_layer.data[target_tile[0]][target_tile[1]] = seed_block
                inventory.get_items()["carrot_seeds"] -= 1
                self.make_map()
            print(current_map_tile, current_nature_tile)


    def get_surface(self):
        return self.surface
