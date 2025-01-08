import random
import sqlite3
import logging
from tkinter import Tk, Label, Entry, Button

# Setting up logging
logging.basicConfig(filename='spelling_game.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Word list for the spelling game
WORD_LIST = ["python", "developer", "algorithm", "function", "variable", "database", "syntax", "exception", "iteration", "recursion"]

# Database setup
def initialize_db():
    conn = sqlite3.connect('spelling_game.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      word TEXT,
                      user_input TEXT,
                      correct BOOLEAN)
                   ''')
    conn.commit()
    conn.close()

def save_to_db(word, user_input, correct):
    conn = sqlite3.connect('spelling_game.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (word, user_input, correct) VALUES (?, ?, ?)", (word, user_input, correct))
    conn.commit()
    conn.close()

def generate_random_word():
    return random.choice(WORD_LIST)

# Console-based game
def play_console_game():
    score = 0
    print("Welcome to the Spelling Game!")
    while True:
        word = generate_random_word()
        print(f"Spell the word: {word}")
        user_input = input("Your answer: ").strip()
        if user_input.lower() == word:
            print("Correct!")
            score += 1
            correct = True
        else:
            print(f"Wrong! The correct spelling is {word}.")
            correct = False
        save_to_db(word, user_input, correct)
        logging.info(f"Word: {word}, User Input: {user_input}, Correct: {correct}")
        
        cont = input("Do you want to continue? (yes/no): ").strip().lower()
        if cont != 'yes':
            break
    print(f"Your final score is: {score}")

# GUI-based game (Tkinter)
def play_gui_game():
    def check_spelling():
        nonlocal current_word, score
        user_input = entry.get().strip()
        if user_input.lower() == current_word:
            result_label.config(text="Correct!", fg="green")
            score += 1
            correct = True
        else:
            result_label.config(text=f"Wrong! Correct spelling: {current_word}", fg="red")
            correct = False
        save_to_db(current_word, user_input, correct)
        logging.info(f"Word: {current_word}, User Input: {user_input}, Correct: {correct}")
        entry.delete(0, 'end')
        current_word = generate_random_word()
        word_label.config(text=f"Spell the word: {current_word}")

    current_word = generate_random_word()
    score = 0

    root = Tk()
    root.title("Spelling Game")

    word_label = Label(root, text=f"Spell the word: {current_word}", font=("Arial", 16))
    word_label.pack(pady=10)

    entry = Entry(root, font=("Arial", 14))
    entry.pack(pady=5)

    check_button = Button(root, text="Check", command=check_spelling, font=("Arial", 14))
    check_button.pack(pady=10)

    result_label = Label(root, text="", font=("Arial", 14))
    result_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    initialize_db()
    mode = input("Choose mode (console/gui): ").strip().lower()
    if mode == "console":
        play_console_game()
    elif mode == "gui":
        play_gui_game()
    else:
        print("Invalid mode selected. Exiting.")
