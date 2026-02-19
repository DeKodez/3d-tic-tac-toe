"""3D Tic-Tac-Toe — Entry Point.

Temporary version for Commit 7: renders hardcoded game state, no interactivity.
"""
# pylint: disable=no-member

import pygame

from game.game_controller import GameController
from ui.renderer import Renderer
from ui.constants import WINDOW_WIDTH, WINDOW_HEIGHT


def main() -> None:
    pygame.init()
    surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("3D Tic-Tac-Toe")
    clock = pygame.time.Clock()

    game = GameController()
    renderer = Renderer()

    # --- Hardcoded moves for visual testing ---
    # Face 0: X wins top row
    game.make_move(0, 0, 0)  # X
    game.make_move(1, 1, 1)  # O on face 1
    game.make_move(0, 0, 1)  # X
    game.make_move(1, 2, 0)  # O on face 1
    game.make_move(0, 0, 2)  # X wins face 0

    # Face 1: O has center and bottom-left, still in progress
    # (already placed above: O at (1,1) and (2,0))

    # Face 2: some marks, in progress
    game.make_move(2, 0, 0)  # O
    game.make_move(2, 1, 1)  # X
    game.make_move(2, 2, 2)  # O

    active_face_index = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Use number keys 1-6 to switch faces for testing
                if pygame.K_1 <= event.key <= pygame.K_6:
                    active_face_index = event.key - pygame.K_1

        renderer.draw(surface, game, active_face_index)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
