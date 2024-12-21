import pygame
import pygame.freetype

import random

from dataclasses import dataclass
from functools import cache

from typing import Optional


@cache
def fibonacci(n: int) -> int:
    if n < 1:
        raise ValueError("n must be greater than 0")
    if n == 1 or n == 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


@cache
def fib_idx(x: int) -> int:
    n = 2
    while True:
        found_x = fibonacci(n)
        if found_x == x:
            return n
        if found_x > x:
            raise ValueError(f"{x} is not a Fibonacci number")
        n += 1


@dataclass
class Tile:
    x: int
    y: int
    value: int

    def can_merge(self, other: "Tile") -> bool:
        if self.value == 1 and other.value == 1:
            return True
        my_idx = fib_idx(self.value)
        other_idx = fib_idx(other.value)
        return abs(my_idx - other_idx) == 1


def draw_board(screen: pygame.Surface):
    for y in range(4):
        for x in range(4):
            pygame.draw.rect(
                screen,
                "dimgray",
                ((80 * x) + (5 * x), (100 * y) + (5 * y), 80, 100),
                border_radius=5,
            )


def draw_tile(screen: pygame.Surface, font: pygame.freetype.Font, tile: Tile):
    pygame.draw.rect(
        screen,
        "lightgrey",
        ((80 * tile.x) + (5 * tile.x), (100 * tile.y) + (5 * tile.y), 80, 100),
        border_radius=5,
    )
    font.render_to(
        screen,
        ((80 * tile.x) + (5 * tile.x) + 10, (100 * tile.y) + (5 * tile.y) + 15),
        str(tile.value),
        "black",
    )


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.freetype.SysFont("monospace", 30)
    clock = pygame.time.Clock()
    running = True

    tiles = []

    def tile_at(x: int, y: int) -> Optional[Tile]:
        for tile in tiles:
            if tile.x == x and tile.y == y:
                return tile

    def empty_tiles() -> list[tuple[int, int]]:
        out = []
        for x in range(4):
            for y in range(4):
                if tile_at(x, y) is None:
                    out.append((x, y))
        return out

    def drop_tile():
        x, y = random.choice(empty_tiles())
        tiles.append(Tile(x, y, 1))

    for _ in range(random.randint(1, 4)):
        drop_tile()

    def right():
        moved = False
        for y in range(4):
            for x in reversed(range(4)):
                if tile := tile_at(x, y):
                    if left_tile := tile_at(x - 1, y):
                        if tile.can_merge(left_tile):
                            tile.value += left_tile.value
                            tiles.remove(left_tile)
                            for x in range(x - 1):
                                if tile := tile_at(x, y):
                                    tile.x += 1
                            moved = True
                            break
                else:
                    for tile in tiles:
                        if tile.y == y and tile.x < x:
                            tile.x += 1
                            moved = True
                    break
        if moved:
            drop_tile()

    def left():
        moved = False
        for y in range(4):
            for x in range(4):
                if tile := tile_at(x, y):
                    if right_tile := tile_at(x + 1, y):
                        if tile.can_merge(right_tile):
                            tile.value += right_tile.value
                            tiles.remove(right_tile)
                            for x in range(x + 1, 4):
                                if tile := tile_at(x, y):
                                    tile.x -= 1
                            moved = True
                            break
                else:
                    for tile in tiles:
                        if tile.y == y and tile.x > x:
                            tile.x -= 1
                            moved = True
                    break
        if moved:
            drop_tile()

    def down():
        moved = False
        for x in range(4):
            for y in reversed(range(4)):
                if tile := tile_at(x, y):
                    if up_tile := tile_at(x, y - 1):
                        if tile.can_merge(up_tile):
                            tile.value += up_tile.value
                            tiles.remove(up_tile)
                            for y in range(y - 1):
                                if tile := tile_at(x, y):
                                    tile.y += 1
                            moved = True
                            break
                else:
                    for tile in tiles:
                        if tile.y < y and tile.x == x:
                            tile.y += 1
                            moved = True
                    break
        if moved:
            drop_tile()

    def up():
        moved = False
        for x in range(4):
            for y in range(4):
                if tile := tile_at(x, y):
                    if down_tile := tile_at(x, y + 1):
                        if tile.can_merge(down_tile):
                            tile.value += down_tile.value
                            tiles.remove(down_tile)
                            for y in range(y + 1, 4):
                                if tile := tile_at(x, y):
                                    tile.y -= 1
                            moved = True
                            break
                else:
                    for tile in tiles:
                        if tile.y > y and tile.x == x:
                            tile.y -= 1
                            moved = True
                    break
        if moved:
            drop_tile()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_w, pygame.K_UP]:
                    up()
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    right()
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    down()
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    left()

        screen.fill("white")
        draw_board(screen)
        for tile in tiles:
            draw_tile(screen, font, tile)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
