"""Renderer — all Pygame drawing logic. Reads game state, never mutates it."""

import pygame

from game.board import Board
from game.enums import CellState, FaceStatus, Player
from game.game_controller import GameController
from ui.constants import (
    BG_COLOR,
    CELL_HOVER,
    CELL_SIZE,
    FACE_LABELS,
    FONT_SIZE_GAME_OVER,
    FONT_SIZE_GAME_OVER_SUB,
    FONT_SIZE_STATUS,
    FONT_SIZE_TAB,
    GRID_COLOR,
    GRID_LINE_WIDTH,
    GRID_ORIGIN_X,
    GRID_ORIGIN_Y,
    GRID_WIDTH,
    GRID_HEIGHT,
    MARK_LINE_WIDTH,
    MARK_PADDING,
    O_COLOR,
    STATUS_BAR_HEIGHT,
    STATUS_BAR_Y,
    STATUS_BG,
    TAB_ACTIVE,
    TAB_BORDER,
    TAB_DRAW,
    TAB_GAP,
    TAB_HEIGHT,
    TAB_INACTIVE,
    TAB_START_X,
    TAB_WIDTH,
    TAB_WON_O,
    TAB_WON_X,
    TAB_Y,
    TEXT_COLOR,
    WINDOW_WIDTH,
    X_COLOR,
)


class Renderer:
    """Handles all drawing to the Pygame surface.

    Reads game state via GameController but never mutates it.
    """

    def __init__(self) -> None:
        self._font_tab = pygame.font.SysFont(None, FONT_SIZE_TAB)
        self._font_status = pygame.font.SysFont(None, FONT_SIZE_STATUS)
        self._font_game_over = pygame.font.SysFont(None, FONT_SIZE_GAME_OVER)
        self._font_game_over_sub = pygame.font.SysFont(None, FONT_SIZE_GAME_OVER_SUB)

    def draw(
        self,
        surface: pygame.Surface,
        game: GameController,
        active_face_index: int,
    ) -> None:
        """Master draw call — clears screen and draws everything."""
        surface.fill(BG_COLOR)

        active_board = game.get_face(active_face_index)

        self._draw_face_tabs(surface, game.faces, active_face_index)
        self._draw_grid(surface, active_board)
        self._draw_status_bar(
            surface,
            game.current_player,
            game.score_tracker.get_scores(),
        )

        if game.is_game_over():
            self._draw_game_over(surface, game.get_result_text())

    # --- Grid ---

    def _draw_grid(self, surface: pygame.Surface, board: Board) -> None:
        """Draw the 3x3 grid lines and any X/O marks."""
        ox, oy = GRID_ORIGIN_X, GRID_ORIGIN_Y

        # Draw cell backgrounds
        for r in range(3):
            for c in range(3):
                rect = pygame.Rect(
                    ox + c * CELL_SIZE,
                    oy + r * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                )
                pygame.draw.rect(surface, BG_COLOR, rect)

        # Draw grid lines
        for i in range(1, 3):
            # Vertical
            x = ox + i * CELL_SIZE
            pygame.draw.line(
                surface, GRID_COLOR, (x, oy), (x, oy + GRID_HEIGHT), GRID_LINE_WIDTH
            )
            # Horizontal
            y = oy + i * CELL_SIZE
            pygame.draw.line(
                surface, GRID_COLOR, (ox, y), (ox + GRID_WIDTH, y), GRID_LINE_WIDTH
            )

        # Draw border
        border_rect = pygame.Rect(ox, oy, GRID_WIDTH, GRID_HEIGHT)
        pygame.draw.rect(surface, GRID_COLOR, border_rect, GRID_LINE_WIDTH)

        # Draw marks
        for r in range(3):
            for c in range(3):
                cell = board.get_cell(r, c)
                cx = ox + c * CELL_SIZE + CELL_SIZE // 2
                cy = oy + r * CELL_SIZE + CELL_SIZE // 2
                if cell == CellState.X:
                    self._draw_x(surface, (cx, cy), CELL_SIZE)
                elif cell == CellState.O:
                    self._draw_o(surface, (cx, cy), CELL_SIZE)

        # Draw winning line if face is won
        if board.winner is not None and board.winning_cells is not None:
            self._draw_winning_line(surface, board)

    def _draw_x(
        self, surface: pygame.Surface, center: tuple[int, int], size: int
    ) -> None:
        """Draw an X mark (two diagonal lines)."""
        half = size // 2 - MARK_PADDING
        cx, cy = center
        pygame.draw.line(
            surface,
            X_COLOR,
            (cx - half, cy - half),
            (cx + half, cy + half),
            MARK_LINE_WIDTH,
        )
        pygame.draw.line(
            surface,
            X_COLOR,
            (cx + half, cy - half),
            (cx - half, cy + half),
            MARK_LINE_WIDTH,
        )

    def _draw_o(
        self, surface: pygame.Surface, center: tuple[int, int], size: int
    ) -> None:
        """Draw an O mark (circle)."""
        radius = size // 2 - MARK_PADDING
        pygame.draw.circle(surface, O_COLOR, center, radius, MARK_LINE_WIDTH)

    def _draw_winning_line(self, surface: pygame.Surface, board: Board) -> None:
        """Draw a line through the 3 winning cells."""
        if board.winning_cells is None:
            return

        ox, oy = GRID_ORIGIN_X, GRID_ORIGIN_Y
        color = X_COLOR if board.winner == Player.X else O_COLOR

        start_r, start_c = board.winning_cells[0]
        end_r, end_c = board.winning_cells[2]

        start_pos = (
            ox + start_c * CELL_SIZE + CELL_SIZE // 2,
            oy + start_r * CELL_SIZE + CELL_SIZE // 2,
        )
        end_pos = (
            ox + end_c * CELL_SIZE + CELL_SIZE // 2,
            oy + end_r * CELL_SIZE + CELL_SIZE // 2,
        )

        pygame.draw.line(surface, color, start_pos, end_pos, MARK_LINE_WIDTH + 2)

    # --- Face tabs ---

    def _draw_face_tabs(
        self,
        surface: pygame.Surface,
        faces: list[Board],
        active_index: int,
    ) -> None:
        """Draw 6 face tabs along the top, color-coded by status."""
        for i, face in enumerate(faces):
            x = TAB_START_X + i * (TAB_WIDTH + TAB_GAP)
            rect = pygame.Rect(x, TAB_Y, TAB_WIDTH, TAB_HEIGHT)

            # Pick background color based on face status
            if i == active_index:
                bg = TAB_ACTIVE
            elif face.status == FaceStatus.WON_X:
                bg = TAB_WON_X
            elif face.status == FaceStatus.WON_O:
                bg = TAB_WON_O
            elif face.status == FaceStatus.DRAW:
                bg = TAB_DRAW
            else:
                bg = TAB_INACTIVE

            pygame.draw.rect(surface, bg, rect, border_radius=5)
            pygame.draw.rect(surface, TAB_BORDER, rect, 1, border_radius=5)

            # Label
            label = FACE_LABELS[i]
            if face.status == FaceStatus.WON_X:
                label += " (X)"
            elif face.status == FaceStatus.WON_O:
                label += " (O)"
            elif face.status == FaceStatus.DRAW:
                label += " (-)"

            text_surf = self._font_tab.render(label, True, TEXT_COLOR)
            text_rect = text_surf.get_rect(center=rect.center)
            surface.blit(text_surf, text_rect)

    # --- Status bar ---

    def _draw_status_bar(
        self,
        surface: pygame.Surface,
        current_player: Player,
        scores: dict[Player, int],
    ) -> None:
        """Draw the status bar showing whose turn it is and current scores."""
        bar_rect = pygame.Rect(0, STATUS_BAR_Y, WINDOW_WIDTH, STATUS_BAR_HEIGHT)
        pygame.draw.rect(surface, STATUS_BG, bar_rect)

        # Turn indicator (left side)
        turn_color = X_COLOR if current_player == Player.X else O_COLOR
        turn_text = f"Player {current_player.symbol}'s turn"
        turn_surf = self._font_status.render(turn_text, True, turn_color)
        surface.blit(turn_surf, (20, STATUS_BAR_Y + 10))

        # Score (right side)
        x_score = scores[Player.X]
        o_score = scores[Player.O]
        score_text = f"X: {x_score}  |  O: {o_score}"
        score_surf = self._font_status.render(score_text, True, TEXT_COLOR)
        score_rect = score_surf.get_rect(right=WINDOW_WIDTH - 20, top=STATUS_BAR_Y + 10)
        surface.blit(score_surf, score_rect)

    # --- Game over ---

    def _draw_game_over(self, surface: pygame.Surface, result_text: str) -> None:
        """Draw a semi-transparent overlay with the final result."""
        overlay = pygame.Surface((WINDOW_WIDTH, surface.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        # Result text
        result_surf = self._font_game_over.render(result_text, True, TEXT_COLOR)
        result_rect = result_surf.get_rect(
            center=(WINDOW_WIDTH // 2, surface.get_height() // 2 - 20)
        )
        surface.blit(result_surf, result_rect)

        # Sub text
        sub_text = "Click anywhere to exit"
        sub_surf = self._font_game_over_sub.render(sub_text, True, TEXT_COLOR)
        sub_rect = sub_surf.get_rect(
            center=(WINDOW_WIDTH // 2, surface.get_height() // 2 + 30)
        )
        surface.blit(sub_surf, sub_rect)
