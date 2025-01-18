import chess

class MinimaxEngine:
    def __init__(self, depth):
        self.depth = depth

    def evaluate_board(self, board):
        # Valutazione semplice: differenza di materiale
        values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}
        score = 0
        for piece in board.piece_map().values():
            value = values[piece.piece_type]
            score += value if piece.color == chess.WHITE else -value
        return score

    def minimax(self, board, depth, is_maximizing):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board), None

        best_move = None
        if is_maximizing:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval, _ = self.minimax(board, depth - 1, False)
                board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval, _ = self.minimax(board, depth - 1, True)
                board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def play(self, board, limit=None):
        _, move = self.minimax(board, self.depth, board.turn == chess.WHITE)
        return chess.engine.PlayResult(move=move)