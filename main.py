"""3D Tic-Tac-Toe — Entry Point."""
# pylint: disable=no-member

import pygame

from game.game_controller import GameController
from ui.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FACE_ADJACENCY, DEFAULT_FACE
from ui.input_handler import InputHandler, NavigateAction, PlaceMoveAction
from ui.renderer import Renderer


def main() -> None:
    """Initialize Pygame, wire up components, and run the game loop."""
    pygame.init()
    surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("3D Tic-Tac-Toe")
    clock = pygame.time.Clock()

    game = GameController()
    renderer = Renderer()
    input_handler = InputHandler()

    active_face_index = DEFAULT_FACE
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action = input_handler.handle_click(event.pos)

                if isinstance(action, NavigateAction):
                    active_face_index = FACE_ADJACENCY[active_face_index][
                        action.direction
                    ]

                elif isinstance(action, PlaceMoveAction):
                    if not game.is_game_over():
                        game.make_move(
                            active_face_index, action.row, action.col
                        )

        mouse_pos = pygame.mouse.get_pos()
        renderer.draw(surface, game, active_face_index, mouse_pos)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
