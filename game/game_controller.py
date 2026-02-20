"""GameController — orchestrates the 6-face game flow."""

from game.board import Board
from game.enums import GamePhase, Player
from game.score_tracker import ScoreTracker


class GameController:
    """Central orchestrator for the 3D tic-tac-toe game.

    Manages 6 Board instances, global turn order, delegates scoring
    to ScoreTracker, and determines when the game ends.
    Knows nothing about UI or rendering.
    """

    NUM_FACES = 6

    def __init__(self, nukes_enabled: bool = False) -> None:
        self.faces: list[Board] = [Board() for _ in range(self.NUM_FACES)]
        self.current_player: Player = Player.X
        self.score_tracker: ScoreTracker = ScoreTracker()
        self.phase: GamePhase = GamePhase.PLAYING
        self.nukes_enabled: bool = nukes_enabled
        self.nukes_used: dict[Player, bool] = {
            Player.X: False,
            Player.O: False,
        }

    def make_move(self, face_index: int, row: int, col: int) -> bool:
        """Attempt to place the current player's mark on the given face and cell.

        Delegates to the Board, records a win if the face was just won,
        switches turn, and checks if the game is over.

        Args:
            face_index: Index of the face (0-5).
            row: Row index (0-2).
            col: Column index (0-2).

        Returns:
            True if the move was accepted, False otherwise.
        """
        if self.phase != GamePhase.PLAYING:
            return False

        if not (0 <= face_index < self.NUM_FACES):
            return False

        face = self.faces[face_index]
        was_locked = face.is_locked()

        if not face.place(row, col, self.current_player):
            return False

        # If this move just locked the face (win), record the score
        if not was_locked and face.is_locked() and face.winner is not None:
            self.score_tracker.record_win(face.winner)

        self._switch_turn()
        self._check_game_over()
        return True

    def nuke_face(self, face_index: int) -> bool:
        """Nuke (reset) the board at the given face index.

        The nuke wipes an in-progress board back to empty. It consumes
        the current player's one-time nuke and ends their turn.

        Args:
            face_index: Index of the face (0-5).

        Returns:
            True if the nuke was used, False if it was blocked.
        """
        if not self.nukes_enabled:
            return False

        if self.phase != GamePhase.PLAYING:
            return False

        if self.nukes_used[self.current_player]:
            return False

        if not (0 <= face_index < self.NUM_FACES):
            return False

        face = self.faces[face_index]
        if face.is_locked():
            return False

        face.reset()
        self.nukes_used[self.current_player] = True
        self._switch_turn()
        return True

    def can_nuke(self, face_index: int) -> bool:
        """Return True if the current player can nuke the given face right now."""
        if not self.nukes_enabled:
            return False
        if self.phase != GamePhase.PLAYING:
            return False
        if self.nukes_used[self.current_player]:
            return False
        if not (0 <= face_index < self.NUM_FACES):
            return False
        return not self.faces[face_index].is_locked()

    def skip_turn(self) -> bool:
        """Skip the current player's turn (e.g. timer expired).

        Returns:
            True if the turn was skipped, False if the game isn't playing.
        """
        if self.phase != GamePhase.PLAYING:
            return False
        self._switch_turn()
        return True

    def get_face(self, index: int) -> Board:
        """Return the Board at the given index."""
        return self.faces[index]

    def is_game_over(self) -> bool:
        """Return True if the game has finished."""
        return self.phase == GamePhase.FINISHED

    def get_result_text(self) -> str:
        """Return a human-readable result string."""
        return self.score_tracker.get_result_text()

    def _switch_turn(self) -> None:
        """Toggle the current player."""
        self.current_player = self.current_player.next()

    def _check_game_over(self) -> None:
        """If all 6 faces are locked, set the game phase to FINISHED."""
        if all(face.is_locked() for face in self.faces):
            self.phase = GamePhase.FINISHED
