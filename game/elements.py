""" Game objects definitions. """

import pygame


class CenteredRect(pygame.Rect):
    def __init__(self, pos=(0, 0), size=(100, 100), color=(255, 255, 255)):
        super(CenteredRect, self).__init__(pos, size)
        self.center = pos
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self)


class Slot(pygame.Rect):
    def __init__(self, pos=(0, 0), size=(100, 100)):
        super(Slot, self).__init__(pos, size)
        self._card = None

    @property
    def card(self):
        return self._card

    @card.setter
    def card(self, value):
        self._card = value

    @property
    def is_free(self):
        if self._card is None:
            return True
        else:
            return False


class Hand:
    def __init__(self, n_cards, slot_size, slot_color):
        self.n_cards = n_cards
        self.slot_color = slot_color
        self.slots = [Slot((0, 0), slot_size) for _ in range(n_cards)]

    def __iter__(self):
        yield from self.slots

    def draw(self, surface, y, ref="top"):
        for i, slot in enumerate(self.slots):
            # When creating less than 5 cards row, keep it centered.
            i += (5 - self.n_cards) // 2

            x = (i + 1) * surface.get_width() / 6

            slot.centerx = x
            if "top" in ref.lower():
                slot.top = y
            else:
                slot.bottom = y
            pygame.draw.rect(surface, self.slot_color, slot)


class Board:
    def __init__(self, player, slot_size, slot_color, slot_gap):
        self.player = player
        self.slot_size = slot_size
        self.slot_gap = slot_gap

        self.hole = Hand(n_cards=5, slot_size=slot_size, slot_color=slot_color)
        self.btm = Hand(n_cards=5, slot_size=slot_size, slot_color=slot_color)
        self.mid = Hand(n_cards=5, slot_size=slot_size, slot_color=slot_color)
        self.top = Hand(n_cards=3, slot_size=slot_size, slot_color=slot_color)

        self.hands = [self.hole, self.btm, self.mid, self.top]

    def draw(self, surface, pos):
        for i, hand in enumerate(self.hands):
            if "top" in pos:
                y = i * (self.slot_size[1] + self.slot_gap)
                if i > 0:
                    y += self.slot_gap
            else:
                y = surface.get_height() - i * (self.slot_size[1] + self.slot_gap)
                if i > 0:
                    y -= self.slot_gap

            hand.draw(surface, y, ref=pos)
