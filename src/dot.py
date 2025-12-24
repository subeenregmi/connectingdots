import math
import random
from typing import Tuple

import pygame


class Dot:
    def __init__(
        self,
        SCREEN_SIZE: Tuple[int, int],
        MAX_SPEED: float = 10,
        EXPIRY_TIME: float = 3,
    ) -> None:
        self.screen_size = SCREEN_SIZE
        self.x: float = random.random() * SCREEN_SIZE[0]
        self.y: float = random.random() * SCREEN_SIZE[1]
        self.vx: float = (random.random() - 0.5) * MAX_SPEED
        self.vy: float = (random.random() - 0.5) * MAX_SPEED
        self.radius = 5
        self.friends: list["Dot"] = []
        self.time_lived = 0
        self.expiry = 3 + (random.random() * EXPIRY_TIME * 2)

    def update(self, tick: float):
        self.x += self.vx / tick
        self.y += self.vy / tick
        self.time_lived += 1 / tick

    def draw(self, surface: pygame.Surface):
        alpha = self.alpha()

        for friend in self.friends:
            line_alpha = min(alpha, friend.alpha())
            pygame.draw.line(
                surface, (255, 0, 0, line_alpha), (self.x, self.y), (friend.x, friend.y)
            )

        pygame.draw.circle(
            surface,
            (255, 255, 255, alpha),
            (self.x, self.y),
            self.radius,
        )

    def is_on_screen(self) -> bool:
        if self.x < self.radius or self.x > self.screen_size[0]:
            return False

        if self.y < self.radius or self.y > self.screen_size[1]:
            return False

        return True

    def distance(self, dot: "Dot") -> float:
        return math.sqrt((self.x - dot.x) ** 2 + (self.y - dot.y) ** 2)

    def prune_friends(self, DISTANCE_LIMIT: int) -> None:
        for friend in self.friends.copy():
            if self.distance(friend) > DISTANCE_LIMIT:
                self.friends.remove(friend)

    def add_friend(self, friend: "Dot"):
        if len(self.friends) < 5:
            self.friends.append(friend)

    def expired(self) -> bool:
        return self.time_lived > self.expiry

    def alpha(self) -> int:
        p_lived = (self.time_lived * 4) / (self.expiry)
        if p_lived > 3:
            p_lived = 4 - p_lived
        elif p_lived > 1:
            p_lived = 1

        return max(min(int(255 * p_lived), 255), 0)

    def is_friendable(self, friend: "Dot", DISTANCE_LIMIT: float) -> bool:
        p_lived = (self.time_lived * 4) / self.expiry
        return (
            len(self.friends) < 5
            and len(friend.friends) < 5
            and self.distance(friend) < DISTANCE_LIMIT
            and 0.5 < p_lived < 3.5
        )
