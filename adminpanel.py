
#!/usr/bin/env python3

try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    import Tkinter as tk
    import tkMessageBox as messagebox
import json

class VerticalScrolledFrame:
    def __init__(self, master, **kwargs):
        self.outer = tk.Frame(master)

        self.vsb = tk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)
        self.canvas = tk.Canvas(self.outer, highlightthickness=0, **kwargs)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas['yscrollcommand'] = self.vsb.set
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview

        self.inner = tk.Frame(self.canvas)
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(tk.Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            return getattr(self.outer, item)
        else:
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units" )
        elif event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units" )

root=tk.Tk()
root.geometry('700x700+400+400')
root.title('Rishabh Arts Admin Panel')
img_label = tk.Label(root)
img_label.img = tk.PhotoImage(file='Logo.png')
'''logo seems to be big what size should i prefer coz its messed up
the frame i guess'''
img_label.config(image=img_label.img)
img_label.pack()

welcom=tk.Label(root,text="Quiz Database").pack()

score = 0

def mquit():
    mexit=messagebox.askyesno(title="Quit",message="Quit The Test ?")
    if mexit > 0:
        root.destroy()
        return

def finished():
    mexit=messagebox.askyesno(title="Finish",message="Are You Sure ?")
    if mexit > 0:
        score = 0
        for i in user_answers:
            if user_answers[i].get() == database[i]['answer']:
                score = score + 1

        lc.config(text="you got {} questions out of {} correct!".format(score, len(user_answers)))

with open('database.json') as f:
    database = json.load(f)


question_frame = VerticalScrolledFrame(root, height=500)
question_frame.pack(fill=tk.X)
user_data = [] # put the user data into a list, just like the database

for i in range(50):
    one_q_frame = tk.Frame(question_frame)
    one_q_frame.columnconfigure(1, weight=1) # make the 2nd column expand
    one_q_frame.pack(expand=True, fill=tk.X)

    user_data.append({
        'question': tk.StringVar(value=database[i]['question']),
        'options': [],
        'answer': tk.IntVar(value=database[i]['answer'])
        })

    ent = tk.Entry(one_q_frame, width=50, textvariable=user_data[i]['question'])
    ent.grid(row=0, column=0, columnspan=2, sticky='ew')

    for j in range(4):
        btn = tk.Radiobutton(one_q_frame,
            value=j,
            variable=user_data[i]['answer'])
        btn.grid(row=1+j, column=0)
        user_data[i]['options'].append(tk.StringVar(value=database[i]['options'][j]))
        ent = tk.Entry(one_q_frame, textvariable=user_data[i]['options'][j])
        ent.grid(row=1+j, column=1, sticky='ew')


mbutton=tk.Button(root,text='Quit',command=mquit,fg='red',bg='blue')
mbutton.pack()


lc = tk.Label(root) # the score will be displayed here.
lc.pack()

fbutton=tk.Button(root,text='Finish',command=finished,fg='red',bg='blue')
fbutton.pack()



root.mainloop()
