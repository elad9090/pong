from pathlib import Path
import tkinter as tk
import tkinter.font as tkFont

Font = tkFont.Font
score_file_path = Path('.') /'Game' / 'assets'/ 'score.txt'
table_content = []


class Table(tk.Frame):
    def __init__(self, content, *args, **kwargs):
        super().__init__(*args, **kwargs)

        rows = len(content)
        cols = len(content[0])

        min_height = 20
        width = int(600 / cols)

        for r in range(rows):
            self.grid_rowconfigure(r, minsize=min_height, uniform=True, weight=1)
            for c in range(cols):
                self.grid_columnconfigure(c, minsize=width, weight=1)
                entry = tk.Entry(self)
                entry.grid(row=r, column=c, sticky='we')
                entry.insert(tk.END, content[r][c])

                entry.config(font=Font(family="Calibre", size=14))
                entry.config(justify=tk.CENTER)
                entry.config(state=tk.DISABLED)


class MFrame(tk.Frame):
    def __init__(self, app, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.app = app


class PutScore(MFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        label = tk.Label(self)
        label["justify"] = "center"
        label["text"] = "Enter your name"
        label["font"] = Font(family="Calibre", size=24)
        label.place(x=160, y=80, width=300, height=100)

        name_entry = tk.Entry(self)
        name_entry["borderwidth"] = "1px"
        name_entry["justify"] = "center"
        name_entry["font"] = Font(family="Calibre", size=14)
        name_entry.place(x=160, y=160, width=292, height=30)

        button = tk.Button(self, text="Submit Score")
        button["justify"] = "center"
        button["font"] = Font(family="Calibre", size=14)
        button.place(x=160, y=200, width=292, height=30)

        def command(*args, **kwargs):
            name = name_entry.get()
            if ' ' in name or name == '':
                return

            with score_file_path.open('r+') as f:
                content = f.read().splitlines()
                players = {}

                f.truncate(0)
                f.seek(0)

                for line in content:
                    pname, pscore = line.split()
                    players[pname] = int(pscore)

                if name in players:
                    if self.app.score > players[name]:
                        players[name] = self.app.score
                else:
                    players[name] = self.app.score

                for k in {k: v for k, v in sorted(players.items(), reverse=True, key=lambda item: item[1])}.keys():
                    f.write(f'{k} {players[k]}\n')
                    table_content.append((k, players[k]))

            self.app.show_frame('ShowScore')

        name_entry.bind('<Return>', command)
        button.config(command=command)


class ShowScore(MFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def show_table(self):
        canvas = tk.Canvas(self)

        table = Table(table_content, canvas)
        scrollbar = tk.Scrollbar(canvas, orient=tk.VERTICAL, command=canvas.yview)

        canvas.create_window((0, 0), window=table, anchor='nw', tags='table')
        canvas.config(yscrollcommand=scrollbar.set)

        canvas.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        table.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig('table', width=e.width))

        # table.pack(fill=tk.BOTH, expand=True)

    def tkraise(self, **kwargs):
        self.show_table()
        return super().tkraise(**kwargs)


class score(tk.Tk):
    def __init__(self, mode, score_enemy, score_self):
        super().__init__()

        self.title = "Score"

        modes = {
            60: 100,
            120: 200,
            200: 300
        }

        self.score = modes[mode] + (score_self - score_enemy) * 10

        container = tk.Frame(self)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        width = 600
        height = 500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(False, False)

        self.frames = {}

        for F in (PutScore, ShowScore):
            name = F.__name__
            frame = F(self, container)
            frame.grid(row=0, column=0, sticky='nsew')
            self.frames[name] = frame

        self.show_frame('PutScore')

    def show_frame(self, frame):
        f = self.frames[frame]
        f.tkraise()