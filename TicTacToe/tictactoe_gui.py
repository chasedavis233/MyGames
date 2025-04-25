import tkinter as tk
import random
import tkinter.messagebox as msgbox

class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.configure(bg="#0F0F0F")

        # Game difficulty mode ("Easy" or "Hard")
        self.difficulty = tk.StringVar(value="Easy")

        # Player and AI symbols
        self.player_symbol = "X"
        self.ai_symbol = "O"

        # Internal board representation
        self.board = [""] * 9
        self.buttons = []
        self.game_over = False

        # Initialize UI components
        self.create_widgets()

    def create_widgets(self):
        # Game title label
        title = tk.Label(self.root, text="Tic Tac Toe", font=("Orbitron", 28, "bold"),
                         bg="#0F0F0F", fg="#00FFFF")
        title.pack(pady=10)

        # Top options panel: difficulty toggle & reset
        options_frame = tk.Frame(self.root, bg="#0F0F0F")
        options_frame.pack(pady=10)

        # Difficulty toggle button (Easy <-> Hard)
        self.difficulty_button = tk.Button(options_frame, text="Difficulty: Easy", font=("Orbitron", 12),
                                           width=16, bg="#1A1A1A", fg="#00FF00", activebackground="#2A2A2A",
                                           command=self.toggle_difficulty)
        self.difficulty_button.pack(side=tk.LEFT, padx=5)

        # Reset button
        self.reset_button = tk.Button(options_frame, text="Reset", font=("Orbitron", 12),
                                      command=self.reset_game, bg="#1A1A1A", fg="#00FFFF", activebackground="#2A2A2A")
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # Game board UI (3x3 grid of buttons)
        self.frame = tk.Frame(self.root, bg="#0F0F0F")
        self.frame.pack(expand=True)

        for i in range(9):
            btn = tk.Button(self.frame, text="", font=("Orbitron", 40, "bold"),
                            bg="#1A1A1A", fg="#00FF00", width=3, height=1,
                            borderwidth=2, relief="groove",
                            command=lambda i=i: self.make_move(i))
            btn.grid(row=i//3, column=i%3, sticky="nsew", padx=5, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2A2A2A"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#1A1A1A"))
            self.buttons.append(btn)

        # Make the grid cells expand responsively
        for i in range(3):
            self.frame.columnconfigure(i, weight=1)
            self.frame.rowconfigure(i, weight=1)

    def toggle_difficulty(self):
        """Toggle between Easy and Hard mode and update the button"""
        if self.difficulty.get() == "Easy":
            self.difficulty.set("Hard")
            self.difficulty_button.config(text="Difficulty: Hard", fg="#FF00FF")
        else:
            self.difficulty.set("Easy")
            self.difficulty_button.config(text="Difficulty: Easy", fg="#00FF00")

    def reset_game(self):
        """Clear the board and reset game state"""
        self.board = [""] * 9
        for btn in self.buttons:
            btn.config(text="", state=tk.NORMAL, bg="#1A1A1A", fg="#00FF00")
        self.game_over = False

    def make_move(self, index):
        """Handle player's move and trigger AI response"""
        if self.board[index] or self.game_over:
            return

        self.board[index] = self.player_symbol
        self.buttons[index].config(text=self.player_symbol, fg="#39FF14")

        if self.check_winner(self.player_symbol):
            self.end_game("You win!")
            return
        elif all(self.board):
            self.end_game("It's a draw!")
            return

        self.root.after(200, self.ai_move)

    def ai_move(self):
        """AI selects move based on difficulty setting"""
        if self.difficulty.get() == "Easy":
            move = self.random_move()
        else:
            move = self.best_move()

        if move is not None:
            self.board[move] = self.ai_symbol
            self.buttons[move].config(text=self.ai_symbol, fg="#FF1493")

        if self.check_winner(self.ai_symbol):
            self.end_game("AI wins!")
        elif all(self.board):
            self.end_game("It's a draw!")

    def end_game(self, message):
        """Display game over message and auto-reset"""
        self.game_over = True
        response = msgbox.showinfo("Game Over", message)
        if response == "ok":
            self.reset_game()

    def check_winner(self, symbol):
        """Check if a symbol has a winning combination"""
        wins = [(0,1,2),(3,4,5),(6,7,8),
                (0,3,6),(1,4,7),(2,5,8),
                (0,4,8),(2,4,6)]
        return any(self.board[i]==self.board[j]==self.board[k]==symbol for i,j,k in wins)

    def random_move(self):
        """Choose a random available cell"""
        empty = [i for i in range(9) if not self.board[i]]
        return random.choice(empty) if empty else None

    def best_move(self):
        """Use minimax to find the best move for the AI"""
        best_score = -float('inf')
        move = None
        for i in range(9):
            if not self.board[i]:
                self.board[i] = self.ai_symbol
                score = self.minimax(False)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    move = i
        return move

    def minimax(self, is_maximizing):
        """Recursive minimax algorithm for AI logic"""
        if self.check_winner(self.ai_symbol):
            return 1
        elif self.check_winner(self.player_symbol):
            return -1
        elif all(self.board):
            return 0

        if is_maximizing:
            best = -float('inf')
            for i in range(9):
                if not self.board[i]:
                    self.board[i] = self.ai_symbol
                    val = self.minimax(False)
                    self.board[i] = ""
                    best = max(best, val)
            return best
        else:
            best = float('inf')
            for i in range(9):
                if not self.board[i]:
                    self.board[i] = self.player_symbol
                    val = self.minimax(True)
                    self.board[i] = ""
                    best = min(best, val)
            return best

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x600")
    game = TicTacToeGame(root)
    root.mainloop()
