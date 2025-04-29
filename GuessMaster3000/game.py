## NOT COMPETE

import tkinter as tk
import random
from tkinter import messagebox

# Create main window
root = tk.Tk()
root.title("GuessMaster3000")
root.geometry("400x300")
root.minsize(300, 250)
root.configure(bg="#2d3436")  # Dark background

# Generate a random number between 1 and 100
number_to_guess = random.randint(1, 100)

# Function to check the guess
def check_guess():
    try:
        guess = int(entry.get())
        if guess < number_to_guess:
            feedback_label.config(text="Too low! Try again.", fg="#74b9ff")
        elif guess > number_to_guess:
            feedback_label.config(text="Too high! Try again.", fg="#ff7675")
        else:
            messagebox.showinfo("Congratulations!", "You guessed the number!")
            reset_game()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")

# Function to reset the game
def reset_game():
    global number_to_guess
    number_to_guess = random.randint(1, 100)
    entry.delete(0, tk.END)
    feedback_label.config(text="")

# Create input box (with visible background color)
entry = tk.Entry(root, font=("Helvetica", 16), bg="#dfe6e9", fg="black")
entry.pack(pady=20)

# Create Guess button
guess_button = tk.Button(root, text="Guess!", font=("Helvetica", 16, "bold"), bg="#0984e3", fg="white", command=check_guess)
guess_button.pack(pady=10)

# Feedback Label
feedback_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#2d3436")
feedback_label.pack(pady=20)

# Make layout resizable
def resize(event):
    entry.config(width=int(event.width / 15))
    feedback_label.config(wraplength=event.width - 40)

root.bind('<Configure>', resize)

# Start the game
root.mainloop()
