import pygame
import pytmx
from pytmx.util_pygame import load_pygame

class Map:
    def __init__(self, filename, scale):
        self.tmx_data = load_pygame(filename)
        self.scale = scale
        self.width = self.tmx_data.width * self.tmx_data.tilewidth * self.scale
        self.height = self.tmx_data.height * self.tmx_data.tileheight * self.scale
        self.surface = pygame.Surface((self.width, self.height))
        self.make_map()

    def make_map(self):
        self.layers = []
        for layer in self.tmx_data.visible_layers:
            layer_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(tile, (tile.get_width() * self.scale, tile.get_height() * self.scale))
                        layer_surface.blit(tile, (x * self.tmx_data.tilewidth * self.scale, y * self.tmx_data.tileheight * self.scale))
            self.layers.append(layer_surface)

    def render_layer(self, screen, camera, layer_index):
        screen.blit(self.layers[layer_index], camera.apply_rect(self.layers[layer_index].get_rect()))

    def render_layers(self, screen, camera, below_player_layers, above_player_layers):
        for layer_index in below_player_layers:
            self.render_layer(screen, camera, layer_index)
        for layer_index in above_player_layers:
            self.render_layer(screen, camera, layer_index)

    def get_surface(self):
        return self.surface
