"""Renderer — all Pygame drawing logic. Reads game state, never mutates it."""
# pylint: disable=no-member

import math

import pygame

from game.board import Board
from game.enums import CellState, FaceStatus, Player
from game.game_controller import GameController
from ui.constants import (
    ARROW_BG,
    ARROW_ICON,
    ARROW_PADDING,
    ARROW_SIZE,
    ARROWS,
    BG_COLOR,
    CELL_SIZE,
    CUBE_EDGE_BACK_COLOR,
    CUBE_EDGE_COLOR,
    CUBE_LEGEND_CX,
    CUBE_LEGEND_CY,
    CUBE_LEGEND_R,
    FACE_LABELS,
    FACE_LABEL_Y,
    FONT_SIZE_CUBE_LABEL,
    FONT_SIZE_FACE_LABEL,
    FONT_SIZE_GAME_OVER,
    FONT_SIZE_GAME_OVER_SUB,
    FONT_SIZE_STATUS,
    GRID_COLOR,
    GRID_HEIGHT,
    GRID_LINE_WIDTH,
    GRID_ORIGIN_X,
    GRID_ORIGIN_Y,
    GRID_WIDTH,
    MARK_LINE_WIDTH,
    MARK_PADDING,
    NUM_FACES,
    O_COLOR,
    STATUS_BAR_HEIGHT,
    STATUS_BAR_Y,
    STATUS_BG,
    TEXT_COLOR,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    X_COLOR,
)


class Renderer:
    """Handles all drawing to the Pygame surface.

    Reads game state via GameController but never mutates it.
    """

    def __init__(self) -> None:
        self._font_face_label = pygame.font.SysFont(None, FONT_SIZE_FACE_LABEL)
        self._font_cube_label = pygame.font.SysFont(None, FONT_SIZE_CUBE_LABEL)
        self._font_status = pygame.font.SysFont(None, FONT_SIZE_STATUS)
        self._font_game_over = pygame.font.SysFont(None, FONT_SIZE_GAME_OVER)
        self._font_game_over_sub = pygame.font.SysFont(None, FONT_SIZE_GAME_OVER_SUB)
        self._cube_geometry = self._compute_cube_geometry()

    def draw(
        self,
        surface: pygame.Surface,
        game: GameController,
        active_face_index: int,
    ) -> None:
        """Master draw call — clears screen and draws everything."""
        surface.fill(BG_COLOR)

        active_board = game.get_face(active_face_index)

        self._draw_face_label(surface, active_face_index, active_board)
        self._draw_cube_legend(surface, active_face_index, game.faces)
        self._draw_arrows(surface)
        self._draw_grid(surface, active_board)
        self._draw_status_bar(
            surface,
            game.current_player,
            game.score_tracker.get_scores(),
        )

        if game.is_game_over():
            self._draw_game_over(surface, game.get_result_text(), game.faces)

    # --- Face label (top center) ---

    def _draw_face_label(
        self, surface: pygame.Surface, face_index: int, board: Board
    ) -> None:
        """Draw the current face name and status above the grid."""
        label = FACE_LABELS[face_index]

        if board.status == FaceStatus.WON_X:
            label += "  \u2014  Won by X"
            color = X_COLOR
        elif board.status == FaceStatus.WON_O:
            label += "  \u2014  Won by O"
            color = O_COLOR
        elif board.status == FaceStatus.DRAW:
            label += "  \u2014  Draw"
            color = (150, 150, 150)
        else:
            color = TEXT_COLOR

        text_surf = self._font_face_label.render(label, True, color)
        text_rect = text_surf.get_rect(centerx=WINDOW_WIDTH // 2, y=FACE_LABEL_Y)
        surface.blit(text_surf, text_rect)

    # --- Mini isometric cube legend (top left) ---

    @staticmethod
    def _compute_cube_geometry() -> dict:
        """Pre-compute the vertices, face polygons, and edges for the legend cube."""
        cx = CUBE_LEGEND_CX
        cy = CUBE_LEGEND_CY
        r = CUBE_LEGEND_R

        dx = int(r * math.cos(math.radians(30)))
        dy = r // 2

        center = (cx, cy)
        top = (cx, cy - r)
        tr = (cx + dx, cy - dy)
        br = (cx + dx, cy + dy)
        bottom = (cx, cy + r)
        bl = (cx - dx, cy + dy)
        tl = (cx - dx, cy - dy)

        # Each face maps to a rhombus (2 triangular sectors of the hexagon).
        # Opposite faces occupy non-overlapping areas.
        face_polygons = [
            [center, tl, top, tr],        # 0: Top     — upper rhombus
            [center, tr, br, bottom],     # 1: Front   — lower-right rhombus
            [center, bottom, bl, tl],     # 2: Left    — lower-left rhombus
            [center, br, bottom, bl],     # 3: Bottom  — lower rhombus
            [center, bl, tl, top],        # 4: Back    — upper-left rhombus
            [center, top, tr, br],        # 5: Right   — upper-right rhombus
        ]

        # Outer hexagon edges (always solid)
        outer_edges = [
            (top, tr), (tr, br), (br, bottom),
            (bottom, bl), (bl, tl), (tl, top),
        ]

        # Front spokes (from nearest corner v0 → center, drawn solid)
        front_spokes = [(center, top), (center, br), (center, bl)]

        # Back spokes (from farthest corner v6 → center, drawn dashed)
        back_spokes = [(center, bottom), (center, tr), (center, tl)]

        return {
            "face_polygons": face_polygons,
            "outer_edges": outer_edges,
            "front_spokes": front_spokes,
            "back_spokes": back_spokes,
        }

    def _draw_cube_legend(
        self,
        surface: pygame.Surface,
        active_face_index: int,
        faces: list[Board],
    ) -> None:
        """Draw the mini isometric cube with the active face highlighted."""
        geo = self._cube_geometry

        # Fill won/drawn faces with tinted colors
        for i, face in enumerate(faces):
            if face.status == FaceStatus.WON_X:
                self._fill_polygon_alpha(
                    surface, geo["face_polygons"][i], (*X_COLOR, 60)
                )
            elif face.status == FaceStatus.WON_O:
                self._fill_polygon_alpha(
                    surface, geo["face_polygons"][i], (*O_COLOR, 60)
                )
            elif face.status == FaceStatus.DRAW:
                self._fill_polygon_alpha(
                    surface, geo["face_polygons"][i], (150, 150, 150, 40)
                )

        # Highlight the active face
        self._fill_polygon_alpha(
            surface, geo["face_polygons"][active_face_index], (255, 255, 255, 80)
        )

        # Outer hexagon edges (solid)
        for start, end in geo["outer_edges"]:
            pygame.draw.line(surface, CUBE_EDGE_COLOR, start, end, 2)

        # Front spokes (solid)
        for start, end in geo["front_spokes"]:
            pygame.draw.line(surface, CUBE_EDGE_COLOR, start, end, 2)

        # Back spokes (dashed)
        for start, end in geo["back_spokes"]:
            self._draw_dashed_line(surface, CUBE_EDGE_BACK_COLOR, start, end, 1)

        # Small label beneath the cube
        label_surf = self._font_cube_label.render(
            FACE_LABELS[active_face_index], True, TEXT_COLOR
        )
        label_rect = label_surf.get_rect(
            centerx=CUBE_LEGEND_CX, top=CUBE_LEGEND_CY + CUBE_LEGEND_R + 6
        )
        surface.blit(label_surf, label_rect)

    @staticmethod
    def _fill_polygon_alpha(
        surface: pygame.Surface,
        polygon: list[tuple[int, int]],
        color_rgba: tuple[int, int, int, int],
    ) -> None:
        """Draw a filled polygon with per-pixel alpha onto the surface."""
        xs = [p[0] for p in polygon]
        ys = [p[1] for p in polygon]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        w = max_x - min_x + 1
        h = max_y - min_y + 1

        temp = pygame.Surface((w, h), pygame.SRCALPHA)
        offset_polygon = [(x - min_x, y - min_y) for x, y in polygon]
        pygame.draw.polygon(temp, color_rgba, offset_polygon)
        surface.blit(temp, (min_x, min_y))

    @staticmethod
    def _draw_dashed_line(
        surface: pygame.Surface,
        color: tuple[int, int, int],
        start: tuple[int, int],
        end: tuple[int, int],
        width: int = 1,
        dash_len: int = 4,
        gap_len: int = 3,
    ) -> None:
        """Draw a dashed line between two points."""
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.sqrt(dx * dx + dy * dy)
        if length == 0:
            return
        dx_n, dy_n = dx / length, dy / length

        pos = 0.0
        drawing = True
        while pos < length:
            seg = min(dash_len if drawing else gap_len, length - pos)
            if drawing:
                sx = int(start[0] + dx_n * pos)
                sy = int(start[1] + dy_n * pos)
                ex = int(start[0] + dx_n * (pos + seg))
                ey = int(start[1] + dy_n * (pos + seg))
                pygame.draw.line(surface, color, (sx, sy), (ex, ey), width)
            pos += seg
            drawing = not drawing

    # --- Arrow buttons ---

    def _draw_arrows(self, surface: pygame.Surface) -> None:
        """Draw the 4 directional arrow buttons around the grid."""
        for direction, pos in ARROWS.items():
            rect = pygame.Rect(pos[0], pos[1], ARROW_SIZE, ARROW_SIZE)
            pygame.draw.rect(surface, ARROW_BG, rect, border_radius=4)

            cx = rect.centerx
            cy = rect.centery
            p = ARROW_PADDING

            if direction == "up":
                tri = [
                    (cx, rect.top + p),
                    (rect.left + p, rect.bottom - p),
                    (rect.right - p, rect.bottom - p),
                ]
            elif direction == "down":
                tri = [
                    (cx, rect.bottom - p),
                    (rect.left + p, rect.top + p),
                    (rect.right - p, rect.top + p),
                ]
            elif direction == "left":
                tri = [
                    (rect.left + p, cy),
                    (rect.right - p, rect.top + p),
                    (rect.right - p, rect.bottom - p),
                ]
            else:  # right
                tri = [
                    (rect.right - p, cy),
                    (rect.left + p, rect.top + p),
                    (rect.left + p, rect.bottom - p),
                ]

            pygame.draw.polygon(surface, ARROW_ICON, tri)

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
        """Draw a prominent line through the 3 winning cells with a glow."""
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

        # Glow backdrop (wider, semi-transparent)
        glow_color = (*color, 60)
        glow_surf = pygame.Surface(
            (GRID_WIDTH + 20, GRID_HEIGHT + 20), pygame.SRCALPHA
        )
        glow_start = (start_pos[0] - ox + 10, start_pos[1] - oy + 10)
        glow_end = (end_pos[0] - ox + 10, end_pos[1] - oy + 10)
        pygame.draw.line(glow_surf, glow_color, glow_start, glow_end, 16)
        surface.blit(glow_surf, (ox - 10, oy - 10))

        # Main line
        pygame.draw.line(surface, color, start_pos, end_pos, MARK_LINE_WIDTH + 3)

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
        score_rect = score_surf.get_rect(
            right=WINDOW_WIDTH - 20, top=STATUS_BAR_Y + 10
        )
        surface.blit(score_surf, score_rect)

    # --- Game over ---

    def _draw_game_over(
        self,
        surface: pygame.Surface,
        result_text: str,
        faces: list[Board],
    ) -> None:
        """Draw a semi-transparent overlay with the final result and face breakdown."""
        overlay = pygame.Surface(
            (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2

        # Title: "GAME OVER"
        title_surf = self._font_game_over.render("GAME OVER", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(center_x, center_y - 80))
        surface.blit(title_surf, title_rect)

        # Result text (e.g. "Player X wins 4-2!")
        result_surf = self._font_face_label.render(result_text, True, TEXT_COLOR)
        result_rect = result_surf.get_rect(center=(center_x, center_y - 45))
        surface.blit(result_surf, result_rect)

        # Per-face breakdown
        breakdown_y = center_y - 10
        for i in range(NUM_FACES):
            face = faces[i]
            label = FACE_LABELS[i]

            if face.status == FaceStatus.WON_X:
                status_str = "X"
                color = X_COLOR
            elif face.status == FaceStatus.WON_O:
                status_str = "O"
                color = O_COLOR
            else:
                status_str = "-"
                color = (120, 120, 120)

            line_text = f"{label}: {status_str}"
            line_surf = self._font_game_over_sub.render(line_text, True, color)

            # Arrange in two columns (3 per column)
            col = i // 3
            row = i % 3
            lx = center_x - 80 + col * 160
            ly = breakdown_y + row * 26
            line_rect = line_surf.get_rect(centerx=lx, top=ly)
            surface.blit(line_surf, line_rect)

        # Sub text
        sub_text = "Navigate with arrows to review  |  Press ESC to exit"
        sub_surf = self._font_game_over_sub.render(sub_text, True, (160, 160, 160))
        sub_rect = sub_surf.get_rect(center=(center_x, center_y + 100))
        surface.blit(sub_surf, sub_rect)
