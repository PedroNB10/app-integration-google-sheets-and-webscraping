import tkinter as tk
import tkinter.ttk as ttk

from datetime import datetime

class ScrollableTextWithButtons(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.text_widget = tk.Text(self, wrap=tk.WORD)
        self.scrollbar = tk.Scrollbar(self, command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Insert buttons as window widgets in the Text widget
        for i in range(300):
            button = ttk.Button(self.text_widget, text=f"{datetime.now()}", command=lambda i=i: print(i))
            self.text_widget.window_create(tk.END, window=button)
            self.text_widget.insert(tk.END, "\n")  # Add a newline after each button

            # Center the entire line containing the button
            line_start = f"{i + 1}.0"
            self.text_widget.tag_add(f"button_{i+1}", line_start, f"{line_start}+2l")
            self.text_widget.tag_configure(f"button_{i+1}", justify='center')

def main():
    root = tk.Tk()
    app = ScrollableTextWithButtons(root)
    app.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()
