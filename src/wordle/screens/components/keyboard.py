import pygame

from wordle.game import LetterResult
from wordle.screens.components.base_component import BaseComponent


class Keyboard(BaseComponent):
    font_color = (0, 0, 0)
    font_size = 28

    key_border_color = (100, 100, 100)
    key_color = (200, 200, 200)
    key_margin = 10
    key_radius = 8
    key_width = 60
    key_height = 60

    letter_right_position_color = (83, 141, 78)
    letter_wrong_position_color = (181, 159, 59)
    letter_wrong_color = (120, 124, 126)

    # the keys rows can be changed to display a different keyboard layout
    rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
    special_keys = ["ENTER", "BACKSPACE"]

    keyboard_keys = []
    keyboard_keys_dict = {}

    def __init__(self, width=800, height=None, background_color=(0, 0, 0)):
        super().__init__(
            width=width,
            height=height or 300,
            background_color=background_color,
        )

        self.special_key_width = self.key_width * 2
        self._create_keys()

        self.font = pygame.font.SysFont(None, self.font_size)

    def _create_keys(self):
        for row_index, row in enumerate(self.rows):
            row_rects = []

            position_x = self.get_x_to_center(
                len(row) * (self.key_width + self.key_margin) - self.key_margin
            )
            position_y = row_index * (self.key_height + self.key_margin)
            for letter in row:
                rect = pygame.Rect(
                    position_x,
                    position_y,
                    self.key_width,
                    self.key_height,
                )
                row_rects.append((rect, letter))
                self.keyboard_keys_dict[letter] = rect
                position_x += self.key_width + self.key_margin

            self.keyboard_keys.append(row_rects)

        x_before_first_key_last_row = (
            self.keyboard_keys[-1][0][0].x - self.special_key_width - self.key_margin
        )
        self.enter_rect = pygame.Rect(
            x_before_first_key_last_row,
            self.keyboard_keys[-1][0][0].y,
            self.special_key_width,
            self.key_height,
        )

        x_after_last_key = self.keyboard_keys[-1][-1][0].right + self.key_margin
        self.backspace_rect = pygame.Rect(
            x_after_last_key,
            self.keyboard_keys[-1][-1][0].y,
            self.special_key_width,
            self.key_height,
        )

    def draw(self):
        super().draw()
        self._draw_keys(self.surface)

    def _draw_keys(self, surface):
        for letter, key_rect in self.keyboard_keys_dict.items():
            self._draw_key(surface, key_rect, text=letter)

        self._draw_key(surface, self.enter_rect, text="ENTER")
        self._draw_key(surface, self.backspace_rect, icon="BACKSPACE")

    def _draw_key(self, surface, key_rect, color=None, text=None, icon=None):
        self.draw_rect_rounded_corners(
            surface, key_rect, color or self.key_color, border_radius=self.key_radius
        )

        # draw a border around the key
        self.draw_rect_rounded_corners(
            surface,
            key_rect,
            self.key_border_color,
            border_radius=self.key_radius,
            width=3,
        )

        if text:
            self._draw_text_on_key(surface, key_rect, text)

        elif icon == "BACKSPACE":
            self._draw_backspace_on_key(surface, key_rect, icon)

    def draw_rect_rounded_corners(self, surface, rect, color, border_radius=5, width=0):
        pygame.draw.rect(surface, color, rect, width=width, border_radius=border_radius)

    def _draw_text_on_key(self, surface, key_rect, text):
        text_surf = self.font.render(text, True, self.font_color)
        text_rect = text_surf.get_rect(center=key_rect.center)
        surface.blit(text_surf, text_rect)

    def _draw_backspace_on_key(self, surface, key_rect, icon):
        icon_width = key_rect.width // 2
        icon_height = key_rect.height // 2
        padding = icon_width // 3

        center_x, center_y = key_rect.center
        position_x = center_x - icon_width // 2 + 15
        position_y = center_y - icon_height // 2

        edge_offset = icon_width // 2
        arrow_tip_offset = 5

        pygame.draw.polygon(
            surface,
            self.font_color,
            [
                (position_x, position_y),
                (position_x + icon_width - edge_offset, position_y),
                (position_x + icon_width - edge_offset, position_y + icon_height),
                (position_x, position_y + icon_height),
                (position_x - arrow_tip_offset, center_y),
            ],
            3,
        )

        self._draw_x(
            surface,
            position_x=center_x - icon_width // 2 + padding,
            position_y=center_y - icon_height // 2 + padding,
            width=icon_width - 2 * padding,
            height=icon_height - 2 * padding,
        )

    def _draw_x(self, surface, position_x, position_y, width, height):
        pygame.draw.line(
            surface,
            self.font_color,
            (position_x, position_y),
            (position_x + width, position_y + height),
            3,
        )

        pygame.draw.line(
            surface,
            self.font_color,
            (position_x, position_y + height),
            (position_x + width, position_y),
            3,
        )

    def draw_guess(self, current_attempt, guess):
        """Nothing happens here but animations could be implemented."""

    def draw_result(self, current_attempt, guess, results):
        for letter, result in zip(guess, results):
            key_rect = self.keyboard_keys_dict[letter.upper()]

            color = self.letter_wrong_color
            if result == LetterResult.RIGHT_LETTER_RIGHT_POSITION:
                color = self.letter_right_position_color

            elif result == LetterResult.RIGHT_LETTER_WRONG_POSITION:
                color = self.letter_wrong_position_color

            self._draw_key(
                surface=self.surface, key_rect=key_rect, color=color, text=letter
            )
