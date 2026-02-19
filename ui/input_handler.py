"""InputHandler — maps mouse click coordinates to game actions."""

from dataclasses import dataclass
from typing import Optional, Union

from ui.constants import (
    CELL_SIZE,
    GRID_ORIGIN_X,
    GRID_ORIGIN_Y,
    GRID_WIDTH,
    GRID_HEIGHT,
    TAB_COUNT,
    TAB_GAP,
    TAB_HEIGHT,
    TAB_START_X,
    TAB_WIDTH,
    TAB_Y,
)


@dataclass
class SwitchFaceAction:
    """Action indicating the player clicked a face tab."""

    face_index: int


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
    ) -> Optional[Union[SwitchFaceAction, PlaceMoveAction]]:
        """Map a click position to an action.

        Args:
            pos: (x, y) pixel coordinates of the mouse click.

        Returns:
            SwitchFaceAction if a face tab was clicked,
            PlaceMoveAction if a grid cell was clicked,
            or None if the click was on empty space.
        """
        x, y = pos

        # Check face tabs
        tab_action = self._check_tab_click(x, y)
        if tab_action is not None:
            return tab_action

        # Check grid cells
        cell_action = self._check_cell_click(x, y)
        if cell_action is not None:
            return cell_action

        return None

    def _check_tab_click(self, x: int, y: int) -> Optional[SwitchFaceAction]:
        """Check if the click lands on one of the 6 face tabs."""
        if not (TAB_Y <= y <= TAB_Y + TAB_HEIGHT):
            return None

        for i in range(TAB_COUNT):
            tab_x = TAB_START_X + i * (TAB_WIDTH + TAB_GAP)
            if tab_x <= x <= tab_x + TAB_WIDTH:
                return SwitchFaceAction(face_index=i)

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
