import random
import tkinter as tk
from tkinter import messagebox, ttk

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns

def deposit():
    deposit_window = tk.Toplevel(root)
    deposit_window.title("Deposit")
    deposit_window.geometry("300x100")

    def deposit_amount():
        global balance
        amount = deposit_entry.get()
        if amount.isdigit() and int(amount) > 0:
            balance += int(amount)
            balance_label.config(text=f"Current balance is $ {balance}")
            deposit_window.destroy()
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")

    deposit_label = tk.Label(deposit_window, text="What would you like to deposit? $")
    deposit_label.pack(pady=10)

    deposit_entry = tk.Entry(deposit_window)
    deposit_entry.pack(pady=5)

    deposit_button = tk.Button(deposit_window, text="Deposit", command=deposit_amount)
    deposit_button.pack(pady=10)

def spin_slot_machine():
    global balance
    lines = int(lines_entry.get())
    bet = int(bet_entry.get())

    while True:
        total_bet = bet * lines

        if total_bet > balance:
            messagebox.showinfo("Insufficient Balance", f"You do not have enough to bet that amount. Your current balance is: ${balance}.")
            return
        else:
            break

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)

    winnings, _ = check_winnings(slots, lines, bet, symbol_count) 

    spin_results_text = ""
    for row in range(len(slots[0])):
        for i, column in enumerate(slots):
            if i != len(slots) - 1:
                spin_results_text += column[row] + " | "
            else:
                spin_results_text += column[row]
        spin_results_text += "\n"

    spin_results_text += f"You won ${winnings}."
    spin_results_text += "\n"

    spin_results_text_widget.config(state="normal")
    spin_results_text_widget.delete("1.0", tk.END)
    spin_results_text_widget.insert(tk.END, spin_results_text)
    spin_results_text_widget.config(state="disabled")

    balance += (winnings - total_bet)
    balance_label.config(text=f"Current balance is $ {balance}")

def show_help():
    help_text = """
    How to Play:
    - Enter the number of lines you want to bet on (1-3).
    - Enter the amount you want to bet per line (${MIN_BET}-${MAX_BET}).
    - Click the 'Spin' button to play the slot machine.
    - The results of the spin will be displayed.
    
    How It Works:
    - The slot machine has 3 rows and 3 columns.
    - Each row contains a random symbol (A, B, C, or D).
    - If all symbols in a line match, you win the corresponding prize.
    - The winnings are calculated based on the matched symbols and your bet.
    - Good luck and have fun!
    """

    help_window = tk.Toplevel(root)
    help_window.title("Help")
    help_window.geometry("400x300")

    help_label = tk.Label(help_window, text=help_text, justify="left")
    help_label.pack(pady=10)

def show_about():
    about_text = """
    Hello, I'm Arman
    Python and Full Stack Web Developer. 
    Find me on GitHub: Armancollab. 
    Let's create amazing things together!
    """

    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.geometry("300x150")

    about_label = tk.Label(about_window, text=about_text, justify="left")
    about_label.pack(pady=10)

    def open_github():
        import webbrowser
        webbrowser.open("https://github.com/Armancollab")

    github_button = tk.Button(about_window, text="Visit GitHub", command=open_github)
    github_button.pack(pady=5)

# Main GUI setup
root = tk.Tk()
root.title("Slot Machine")

balance = 0

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Help", command=show_help)

about_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="About", command=show_about)

deposit_button = tk.Button(root, text="Deposit", command=deposit)
deposit_button.pack(pady=10)

balance_label = tk.Label(root, text=f"Current balance is $ {balance}")
balance_label.pack(pady=10)

lines_label = tk.Label(root, text="Enter the number of lines to bet on (1-3):")
lines_label.pack(pady=5)

lines_entry = tk.Entry(root)
lines_entry.pack(pady=5)

bet_label = tk.Label(root, text=f"Enter the amount to bet (${MIN_BET}-${MAX_BET}):")
bet_label.pack(pady=5)

bet_entry = tk.Entry(root)
bet_entry.pack(pady=5)

spin_button = tk.Button(root, text="Spin", command=spin_slot_machine)
spin_button.pack(pady=10)

spin_results_frame = tk.Frame(root)
spin_results_frame.pack(pady=10)

spin_results_text_widget = tk.Text(spin_results_frame, wrap="word", width=50, height=10)
spin_results_text_widget.pack(side="left")

spin_results_scrollbar = ttk.Scrollbar(spin_results_frame, command=spin_results_text_widget.yview)
spin_results_scrollbar.pack(side="right", fill="y")

spin_results_text_widget.config(yscrollcommand=spin_results_scrollbar.set, state="disabled")

root.mainloop()
