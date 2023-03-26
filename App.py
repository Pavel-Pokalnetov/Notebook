import tkinter as tk



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Записная книжка. Учебный проект")
        self.geometry('600x400')
        self.resizable(0, 0)
        self.frame = tk.Frame(
            self,
            padx=10,
            pady=10
        )
        self.records_lb = tk.Label(
            self.frame,
            text="Записи"
        )
        self.records_lb.grid(row=1, column=1)
        self.listRecords = tk.Listbox(self)
        self.listRecords.grid(row=2,column=2)    
        
        self.frame.pack(expand=True)


if __name__ == '__main__':
    app = App()
    app.mainloop()
