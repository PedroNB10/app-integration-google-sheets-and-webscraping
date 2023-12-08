import tkinter as tk

class ScrollbarApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Scrollbar Example")

        # Create a Text widget with a vertical scrollbar
        self.text_widget = tk.Text(self.master, wrap=tk.WORD, width=40, height=10)
        self.text_widget.pack(side=tk.LEFT, fill=tk.Y)

        self.scrollbar = tk.Scrollbar(self.master, command=self.text_widget.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        # Insert some sample text
        for i in range(300):
            self.text_widget.insert(tk.END, f"This is line {i+1}\n")

def main():
    root = tk.Tk()
    app = ScrollbarApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
