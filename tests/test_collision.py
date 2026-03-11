from dino_escape_room.collision import (
    collided_bottom,
    collided_left,
    collided_right,
    collided_top,
    within_x,
    within_y,
)
from dino_escape_room.models import Coords


def test_within_x_returns_true_when_ranges_overlap():
    co1 = Coords(10, 0, 20, 10)
    co2 = Coords(15, 0, 25, 10)
    assert within_x(co1, co2) is True


def test_within_x_returns_false_when_ranges_do_not_overlap():
    co1 = Coords(0, 0, 10, 10)
    co2 = Coords(20, 0, 30, 10)
    assert within_x(co1, co2) is False


def test_within_y_returns_true_when_ranges_overlap():
    co1 = Coords(0, 10, 10, 20)
    co2 = Coords(0, 15, 10, 25)
    assert within_y(co1, co2) is True


def test_within_y_returns_false_when_ranges_do_not_overlap():
    co1 = Coords(0, 0, 10, 10)
    co2 = Coords(0, 20, 10, 30)
    assert within_y(co1, co2) is False


def test_collided_left_detects_left_contact():
    moving = Coords(10, 10, 20, 20)
    obstacle = Coords(8, 8, 12, 22)
    assert collided_left(moving, obstacle) is True


def test_collided_right_detects_right_contact():
    moving = Coords(10, 10, 20, 20)
    obstacle = Coords(18, 8, 22, 22)
    assert collided_right(moving, obstacle) is True


def test_collided_top_detects_top_contact():
    moving = Coords(10, 10, 20, 20)
    obstacle = Coords(8, 8, 22, 12)
    assert collided_top(moving, obstacle) is True


def test_collided_bottom_detects_bottom_contact_after_move():
    moving = Coords(10, 10, 20, 20)
    obstacle = Coords(8, 22, 22, 30)
    assert collided_bottom(2, moving, obstacle) is True


def test_collided_bottom_returns_false_without_reach():
    moving = Coords(10, 10, 20, 20)
    obstacle = Coords(8, 25, 22, 30)
    assert collided_bottom(2, moving, obstacle) is False
