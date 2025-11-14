import tkinter as tk
from tkinter import messagebox
import random

class GuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("400x300")
        
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.max_attempts = 10
        
        # Title
        title = tk.Label(root, text="Guess the Number (1-100)", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Instructions
        instructions = tk.Label(root, text=f"You have {self.max_attempts} attempts", font=("Arial", 10))
        instructions.pack()
        
        # Input frame
        input_frame = tk.Frame(root)
        input_frame.pack(pady=15)
        
        tk.Label(input_frame, text="Enter your guess:").pack(side=tk.LEFT, padx=5)
        self.entry = tk.Entry(input_frame, width=10, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind("<Return>", lambda e: self.check_guess())
        
        # Guess button
        guess_btn = tk.Button(root, text="Guess", command=self.check_guess, bg="lightblue", width=15)
        guess_btn.pack(pady=10)
        
        # Feedback label
        self.feedback = tk.Label(root, text="", font=("Arial", 11), fg="blue")
        self.feedback.pack(pady=10)
        
        # Attempts label
        self.attempts_label = tk.Label(root, text=f"Attempts left: {self.max_attempts}", font=("Arial", 10))
        self.attempts_label.pack()
        
        # Reset button
        reset_btn = tk.Button(root, text="New Game", command=self.reset_game, bg="lightgreen", width=15)
        reset_btn.pack(pady=10)
    
    def check_guess(self):
        try:
            guess = int(self.entry.get())
            self.entry.delete(0, tk.END)
            
            if guess < 1 or guess > 100:
                self.feedback.config(text="Please enter a number between 1 and 100", fg="red")
                return
            
            self.attempts += 1
            remaining = self.max_attempts - self.attempts
            
            if guess == self.secret_number:
                messagebox.showinfo("Win!", f"Correct! The number was {self.secret_number}\nAttempts: {self.attempts}")
                self.reset_game()
            elif guess < self.secret_number:
                self.feedback.config(text="Too low! Try a higher number", fg="orange")
            else:
                self.feedback.config(text="Too high! Try a lower number", fg="orange")
            
            self.attempts_label.config(text=f"Attempts left: {remaining}")
            
            if remaining == 0:
                messagebox.showinfo("Game Over", f"You lost! The number was {self.secret_number}")
                self.reset_game()
        
        except ValueError:
            self.feedback.config(text="Invalid input! Enter a number", fg="red")
    
    def reset_game(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.entry.delete(0, tk.END)
        self.feedback.config(text="")
        self.attempts_label.config(text=f"Attempts left: {self.max_attempts}")

if __name__ == "__main__":
    root = tk.Tk()
    game = GuessingGame(root)
    root.mainloop()