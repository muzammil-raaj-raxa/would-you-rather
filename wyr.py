import tkinter as tk
from tkinter import messagebox
import json

class WouldYouRatherGUI:
    def __init__(self):
        self.question_num = 0
        self.load_data()
        self.user_over_12 = self.ask_user_age()
        self.window = tk.Tk()
        self.center_window()
        self.window.title("Would You Rather")
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(padx=120, pady=10)

        self.question_label = tk.Label(self.main_frame, text="Would you rather...")
        self.question_label.grid(row=0, column=0, columnspan=2, padx=5, pady=15)

        self.vote_button_1 = tk.Button(self.main_frame, text="Option 1?", command=lambda: self.record_vote('votes_1'))
        self.vote_button_1.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.vote_button_2 = tk.Button(self.main_frame, text="Option 2?", command=lambda: self.record_vote('votes_2'))
        self.vote_button_2.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.show_question()
        self.window.mainloop()

    def center_window(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - self.window.winfo_reqwidth()) / 2
        y = (screen_height - self.window.winfo_reqheight()) / 2
        self.window.geometry("+%d+%d" % (x, y))

    def load_data(self):
        try:
            with open("data.txt", "r") as file:
                self.data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "Missing/Invalid file")
            return

    def ask_user_age(self):
        return messagebox.askyesno("Age Restriction", "Are you over the age of 12?")

    def show_question(self):
        if self.question_num < len(self.data):
            question = self.data[self.question_num]
            if not question['children'] or self.user_over_12:
                self.vote_button_1.configure(text=f"{question['option_1']}?")
                self.vote_button_2.configure(text=f"{question['option_2']}?")
            else:
                self.question_num += 1
                self.show_question()
        else:
            messagebox.showinfo("End of Questions", "That was the final question.\nThe program will now end.")
            self.window.destroy()

    def record_vote(self, vote):
        if self.question_num < len(self.data):
            question = self.data[self.question_num]
            question[vote] += 1
            self.show_like_dislike(question)
            self.save_data()
            self.question_num += 1
            self.show_question()

    def show_like_dislike(self, question):
        response = messagebox.askyesno("Choice Recorded?", "Your choice has been recorded.\nDid you like this question?")
        if response:
            question['likes'] += 1
        else:
            question['dislikes'] += 1

    def save_data(self):
        with open("data.txt", "w") as file:
            json.dump(self.data, file, indent=4)

if __name__ == "__main__":
    WouldYouRatherGUI()
