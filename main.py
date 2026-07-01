from __future__ import annotations

from typing import List, Optional, Tuple


class ChessBoard:
    """A simple chess board represented as an array of 64 squares."""

    def __init__(self, board: Optional[List[Optional[str]]] = None) -> None:
        # If a board is given, copy it. Otherwise create an empty 64-square board.
        self.board = board[:] if board is not None else [None] * 64

    @classmethod
    def from_fen(cls, fen: str) -> "ChessBoard":
        # FEN is a text format for chess positions. We only use the board part here.
        board_part = fen.split()[0]
        # Split the board into 8 rows (ranks).
        rows = board_part.split("/")
        if len(rows) != 8:
            raise ValueError("FEN board part must contain 8 ranks")

        squares: List[Optional[str]] = []
        # Read each row character by character.
        for row in rows:
            for char in row:
                # A number means that many empty squares.
                if char.isdigit():
                    squares.extend([None] * int(char))
                else:
                    # A letter means a piece on that square.
                    squares.append(char)

        # Make sure we really built a full 8x8 board.
        if len(squares) != 64:
            raise ValueError("FEN board does not contain 64 squares")

        # Create and return a board object from the list of squares.
        return cls(squares)

    def piece_at(self, square: int) -> Optional[str]:
        # Return the piece on a square if the index is valid.
        if 0 <= square < 64:
            return self.board[square]
        raise IndexError("square index must be between 0 and 63")

    def set_piece(self, square: int, piece: Optional[str]) -> None:
        # Put a piece on a square, or clear it if piece is None.
        if 0 <= square < 64:
            self.board[square] = piece
        else:
            raise IndexError("square index must be between 0 and 63")

    def square_name(self, square: int) -> str:
        # Convert a 0..63 index into chess coordinates like a1, h8.
        file = square % 8
        rank = 8 - (square // 8)
        return f"{chr(ord('a') + file)}{rank}"

    def pretty_print(self) -> None:
        # Print the board in a human-friendly way.
        for rank in range(8):
            row = []
            for file in range(8):
                square = rank * 8 + file
                row.append(self.board[square] or ".")
            print(" ".join(row))
        print()

    def legal_pawn_moves(self, side: str = "w") -> List[Tuple[int, int]]:
        """Return a simple list of legal pawn moves for one side.

        This currently handles:
        - one-step pushes
        - two-step pushes from the starting rank
        - diagonal captures

        It does not yet account for checks, en passant, or promotion rules.
        """
        # Only allow white or black pawns.
        if side not in {"w", "b"}:
            raise ValueError("side must be 'w' or 'b'")

        # White pawns move "up" the board (toward smaller index), black pawns move down.
        direction = -8 if side == "w" else 8
        # White starts on rank 2, black starts on rank 7.
        start_rank = 6 if side == "w" else 1
        # Promotion rank is the far end of the board.
        promotion_rank = 0 if side == "w" else 7

        moves: List[Tuple[int, int]] = []
        # Check every square on the board.
        for square, piece in enumerate(self.board):
            if piece is None:
                # Empty square, nothing to do.
                continue
            # Find pawns of the requested side.
            if piece == "P" and side == "w" or piece == "p" and side == "b":
                # Convert board index to a rank number like 1..8.
                rank = 8 - (square // 8)

                # Try a one-step forward move.
                one_step = square + direction
                if 0 <= one_step < 64 and self.board[one_step] is None:
                    moves.append((square, one_step))

                    # If the pawn is on its starting rank, allow a two-step move.
                    if rank == start_rank:
                        two_step = square + 2 * direction
                        if 0 <= two_step < 64 and self.board[two_step] is None:
                            moves.append((square, two_step))

                # Try diagonal captures.
                for delta in (-1, 1):
                    capture_square = square + direction + delta
                    if not (0 <= capture_square < 64):
                        continue
                    # Avoid wrapping from file a to h or h to a.
                    if square % 8 == 0 and delta == -1:
                        continue
                    if square % 8 == 7 and delta == 1:
                        continue
                    target = self.board[capture_square]
                    # A capture is legal if the target square has an enemy piece.
                    if target is not None and target.isupper() != piece.isupper():
                        moves.append((square, capture_square))

                # This part is just a placeholder for future promotion logic.
                if rank == promotion_rank:
                    continue

        return moves


def main() -> None:
    # A standard initial chess position in FEN format.
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board = ChessBoard.from_fen(fen)
    print("Initial board:")
    board.pretty_print()

    # Ask the board for legal pawn moves for both sides.
    white_moves = board.legal_pawn_moves("w")
    black_moves = board.legal_pawn_moves("b")

    print("White pawn moves:")
    for start, end in white_moves:
        print(f"{board.square_name(start)} -> {board.square_name(end)}")

    print("\nBlack pawn moves:")
    for start, end in black_moves:
        print(f"{board.square_name(start)} -> {board.square_name(end)}")


if __name__ == "__main__":
    main()

