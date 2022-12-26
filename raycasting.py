import pygame as pg
import math

from settings import *


class RayCasting:
    def __init__(self, game):
        self.game = game

    def ray_cast(self):

        player_x, player_y = self.game.player.pos
        map_x, map_y = self.game.player.map_pos

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):

            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # horizontal ray collision
            if sin_a > 0:
                y_hor, dy = (map_y + 1, 1)
            else:
                y_hor, dy = map_y - 0.0001, -1

            # first horizontal intersection
            depth_hor = (y_hor - player_y) / sin_a
            x_hor = player_x + depth_hor * cos_a

            # calculating delta_depth and dx
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            # calculating length of ray
            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # vertical ray collision
            if cos_a > 0:
                x_vert, dx = (map_x + 1, 1)
            else:
                x_vert, dx = (map_x - 0.0001, -1)

            # first vertical intersection
            depth_vert = (x_vert - player_x) / cos_a
            y_vert = player_y + depth_vert * sin_a

            # calculating delta_depth and dy
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            # calculating length of ray
            for i in range(MAX_DEPTH):
                tile_vert = (int(x_vert), int(y_vert))
                if tile_vert in self.game.map.world_map:
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # use the minimum of the depths
            depth = min(depth_hor, depth_vert)

            depth *= math.cos(self.game.player.angle - ray_angle)

            # projection
            proj_height = SCREEN_DIST / (depth + 0.0001)
            color = [255 / (1 + depth**5 * 0.00002)] * 3
            pg.draw.rect(
                self.game.screen,
                color,
                (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height),
            )

            # lines
            pg.draw.line(
                self.game.screen,
                "yellow",
                (WIDTH + 50 * player_x, 50 * player_y),
                (
                    WIDTH + 50 * player_x + 50 * depth * cos_a,
                    50 * player_y + 50 * depth * sin_a,
                ),
                2,
            )

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
