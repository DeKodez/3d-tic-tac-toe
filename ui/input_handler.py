"""InputHandler — maps mouse click coordinates to game actions."""

from dataclasses import dataclass
from typing import Optional, Union

from ui.constants import (
    ARROW_SIZE,
    ARROWS,
    CELL_SIZE,
    GRID_ORIGIN_X,
    GRID_ORIGIN_Y,
    GRID_WIDTH,
    GRID_HEIGHT,
)


@dataclass
class NavigateAction:
    """Action indicating the player clicked an arrow to navigate the cube."""

    direction: str  # "up", "down", "left", "right"


@dataclass
class PlaceMoveAction:
    """Action indicating the player clicked a grid cell."""

    row: int
    col: int


class InputHandler:
    """Translates mouse click positions into game-meaningful actions.

    Knows nothing about game rules — only geometry and layout constants.
    """

    def handle_click(
        self, pos: tuple[int, int]
    ) -> Optional[Union[NavigateAction, PlaceMoveAction]]:
        """Map a click position to an action.

        Args:
            pos: (x, y) pixel coordinates of the mouse click.

        Returns:
            NavigateAction if an arrow button was clicked,
            PlaceMoveAction if a grid cell was clicked,
            or None if the click was on empty space.
        """
        x, y = pos

        # Check arrow buttons
        arrow_action = self._check_arrow_click(x, y)
        if arrow_action is not None:
            return arrow_action

        # Check grid cells
        cell_action = self._check_cell_click(x, y)
        if cell_action is not None:
            return cell_action

        return None

    def _check_arrow_click(self, x: int, y: int) -> Optional[NavigateAction]:
        """Check if the click lands on one of the 4 arrow buttons."""
        for direction, pos in ARROWS.items():
            ax, ay = pos
            if ax <= x <= ax + ARROW_SIZE and ay <= y <= ay + ARROW_SIZE:
                return NavigateAction(direction=direction)
        return None

    def _check_cell_click(self, x: int, y: int) -> Optional[PlaceMoveAction]:
        """Check if the click lands on a cell in the 3x3 grid."""
        if not (
            GRID_ORIGIN_X <= x <= GRID_ORIGIN_X + GRID_WIDTH
            and GRID_ORIGIN_Y <= y <= GRID_ORIGIN_Y + GRID_HEIGHT
        ):
            return None

        col = (x - GRID_ORIGIN_X) // CELL_SIZE
        row = (y - GRID_ORIGIN_Y) // CELL_SIZE

        # Clamp to valid range (edge case: clicking exactly on the boundary)
        col = min(col, 2)
        row = min(row, 2)

        return PlaceMoveAction(row=row, col=col)
