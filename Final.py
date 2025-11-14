import tkinter as tk
from tkinter import messagebox

xp = 0
level = 1
streak = 0

def update_level():
    global level
    level = xp // 50 + 1

def save_money():
    global xp, streak
    amount = entry.get()

    if not amount.isdigit():
        messagebox.showerror("Error", "Enter numbers only!")
        return

    amount = int(amount)
    gain = amount // 5
    xp += gain
    streak += 1
    update_level()

    result_label.config(text=f"+{gain} XP earned!")
    update_stats()

def update_stats():
    stats_label.config(text=f"Level: {level}\nXP: {xp}\nStreak: {streak} days")

app = tk.Tk()
app.title("Purrfect Saver")

title = tk.Label(app, text="Purrfect Saver", font=("Arial", 18))
title.pack()

entry = tk.Entry(app, font=("Arial", 14))
entry.pack()

save_button = tk.Button(app, text="Save Money", font=("Arial", 14), command=save_money)
save_button.pack()

result_label = tk.Label(app, font=("Arial", 14), fg="green")
result_label.pack()

stats_label = tk.Label(app, font=("Arial", 14))
stats_label.pack()

update_stats()
app.mainloop()
