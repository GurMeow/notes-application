import tkinter as tk
from tkinter import messagebox
import mysql.connector

my_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ha@blablabla123",
    port="3306",
    database="notes_db"
)

my_cursor = my_db.cursor()


class Note:
    def __init__(self, note_number, title, date, info):
        self.note_number = note_number
        self.title = title
        self.date = date
        self.info = info


class MainNotesGUI:
    def __init__(self, root_width, root_height):

        self.root_width = root_width
        self.root_height = root_height

        self.notes = []

        my_cursor.execute("SELECT * FROM notes")

        notes = my_cursor.fetchall()

        for note in notes:
            note = list(note)
            new_note = Note(note[0], note[1], note[2], note[3])
            self.notes.append(new_note)

        for note in self.notes:
            print(note.info)

        self.origin_notes = self.notes

        self.saved = True

        self.root = tk.Tk()

        self.open_main_ui()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.mainloop()

    def open_main_ui(self):

        self.root.geometry(f"{self.root_width}x{self.root_height}")

        self.clear_interface()

        self.menuBar = tk.Menu(self.root)

        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="Save", command=self.save)

        self.notesMenu = tk.Menu(self.menuBar, tearoff=0)
        self.notesMenu.add_command(label="New", command=self.add_note)
        self.notesMenu.add_command(label="Edit", command= lambda : self.view_all_notes("edit note"))
        self.notesMenu.add_command(label="Delete", command= lambda : self.view_all_notes("delete note"))
        self.notesMenu.add_command(label="View All", command= lambda : self.view_all_notes("view notes"))

        self.menuBar.add_cascade(menu=self.fileMenu, label="File")
        self.menuBar.add_cascade(menu=self.notesMenu, label="Notes")

        self.root.config(menu=self.menuBar)

        try:
            for i in range(3):
                for j in range(2):
                    x = i * 250 + 20
                    y = j * 300 + 15
                    index = len(self.notes) - (i * 2 + j + 1)
                    if index >= 0:
                        text = self.notes[index].title
                        visible_note = tk.Button(text=text, height=15, width=30,
                                                 command=lambda position=index: self.open_note(position))
                        visible_note.place(x=x, y=y)
        except IndexError as error:
            print(error)

    def clear_interface(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def view_all_notes(self, mode):
        self.clear_interface()

        # Create a Canvas widget for the scrollable area
        canvas = tk.Canvas(self.root)
        canvas.pack(side="left", fill="both", expand=True)

        # Create a frame inside the canvas to contain the notes
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        # Create a vertical scrollbar and link it to the canvas
        scrollbar = tk.Scrollbar(self.root, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.config(yscrollcommand=scrollbar.set)

        # Add the notes (buttons) to the frame
        for i, note in enumerate(self.notes):
            visible_note = ""
            x = i % 3 * 250 + 100
            y = i // 3 * 300 + 50
            if mode=="view notes":
                visible_note = tk.Button(frame, text=note.title, height=15, width=30, command= lambda position=i: self.open_note(position))
            elif mode=="delete note":
                visible_note = tk.Button(frame, text=note.title, height=15, width=30, command=lambda position=i: self.del_note(position))
            elif mode=="edit note":
                visible_note = tk.Button(frame, text=note.title, height=15, width=30, command=lambda position=i: self.edit_note(position))
            visible_note.grid(row=i // 3, column=i % 3)

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Add a back button to return to the main UI
        back_button = tk.Button(self.root, text="Back", command=self.open_main_ui)
        back_button.pack()

    def on_closing(self):
        if not self.saved:
            if messagebox.askyesno(title="Quit?", message="Do you want to quit?"):
                self.root.destroy()
        else:
            self.root.destroy()

    def save(self):

        my_cursor.execute(f"DELETE FROM notes")

        for note in self.notes:
            note_number = note.note_number
            note_title = f"'{note.title}'"
            note_date = f"'{note.date}'"
            note_info = f"'{note.info}'"
            print(note_number, note_title, note_date, note_info)
            my_cursor.execute(f"INSERT INTO notes VALUES ({note_number}, {note_title}, {note_date}, {note_info})")

        my_cursor.execute("COMMIT")

        self.saved = True

    def open_note(self, position):
        if 0 <= position < len(self.notes):
            self.clear_interface()

            note = self.notes[position]

            titleLabel = tk.Label(text="Title: ")
            dateLabel = tk.Label(text="Date: ")

            titleLabel.place(x=20, y=10)
            dateLabel.place(x=20, y=50)

            noteTitleLabel = tk.Label(self.root, text=note.title)
            noteDateLabel = tk.Label(self.root, text=note.date)
            noteInfoText = tk.Text(self.root, font=("Arial", 16), width=60, height=20)

            noteTitleLabel.place(x=100, y=10)
            noteDateLabel.place(x=100, y=50)
            noteInfoText.place(x=20, y=150)

            noteInfoText.insert("1.0", note.info)
            noteInfoText.config(state="disabled")

            back_button = tk.Button(self.root, text="Back", command=self.open_main_ui)
            back_button.place(x=750, y=20)
        else:
            print("index out of range")


    def add_note(self):
        self.clear_interface()

        titleLabel = tk.Label(self.root, text="Title: ")
        titleLabel.place(x=20, y=10)

        self.titleEntry = tk.Entry(self.root, width=100)
        self.titleEntry.place(x=100, y=10)

        dateLabel = tk.Label(self.root, text="Date: ")
        dateLabel.place(x=20, y=50)

        self.dateEntry = tk.Entry(self.root, width=100)
        self.dateEntry.place(x=100, y=50)

        noteLabel = tk.Label(self.root, text="Note: ")
        noteLabel.place(x=20, y=100)

        self.noteText = tk.Text(self.root, font=("Arial", 16), width=60, height=20)
        self.noteText.place(x=20, y=150)

        create_button = tk.Button(self.root, text="Create Note", command=self.new_note)
        create_button.place(x=350, y=660)

    def new_note(self):
        self.title = self.titleEntry.get()
        self.date = self.dateEntry.get()
        self.info = self.noteText.get('1.0', tk.END)

        print(self.info)

        note_number = 0

        try:
            note_number = int(self.notes[-1].note_number)
            note_number+=1
        except IndexError as error:
            print(error)

        if not self.title=="" and not self.date=="":
            note = Note(note_number, self.title, self.date, self.info)
            self.notes.append(note)
            self.saved = False
            self.open_main_ui()
        else:
            messagebox.showerror(title="No Blank Spots", message="Please fill out what you didnt")

    def edit_note(self, position):
        self.clear_interface()

        titleCHangeLabel = tk.Label(self.root, text="Edit title: ")
        titleCHangeLabel.place(x=20, y=10)

        titleChangeEntry = tk.Entry(self.root, text="Edit title: ")
        titleChangeEntry.place(x=80, y=10)

        titleChangeEntry.insert(0, self.notes[position].title)

        changeTextLabel = tk.Label(self.root, text="Edit the text: ")
        changeTextLabel.place(x=80, y=80)

        noteText = self.notes[position].info

        newNoteText = tk.Text(self.root, font=("Arial", 16), width=60, height=20)
        newNoteText.place(x=40, y=120)

        newNoteText.insert('1.0', noteText)

        editBtn = tk.Button(self.root, text="Edit", command= lambda : self.edit_the_note(titleChangeEntry.get(), newNoteText.get("1.0", tk.END), position))
        editBtn.place(x=400, y=650)

    def edit_the_note(self, title, text, position):
        self.notes[position].title = title
        self.notes[position].info = text
        self.saved = False
        self.open_main_ui()

    def del_note(self, position):
        print(position)
        if messagebox.askyesno(title="Delete?", message="Delete the note?"):
            del self.notes[position]
            self.saved = False
            self.open_main_ui()
        else:
            self.open_main_ui()


e = MainNotesGUI(800, 700)
