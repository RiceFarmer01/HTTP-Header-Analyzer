import requests
import tkinter as tk
from tkinter import filedialog, messagebox

class HyperlinkManager:
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="white", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)
        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(tk.CURRENT):
            if tag[:5] == "hyper" and tag in self.links:
                self.links[tag]()
                return

class HeaderAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title('HTTP Header Analyzer')
        self.root.geometry('400x300')
        self.root.configure(background='#2B2B2B')

        self.url_label = tk.Label(root, text="Website URL", fg='white', bg='#2B2B2B', font=("Arial", 12))
        self.url_entry = tk.Entry(root, fg='white', bg='#3C3F41', insertbackground='white')
        self.submit_button = tk.Button(root, text="Get Headers", command=self.get_headers, fg='white', bg='#3C3F41', activebackground='#4E4E4E', font=("Arial", 12))

        self.url_label.pack(fill='x', padx=10, pady=5)
        self.url_entry.pack(fill='x', padx=10, pady=5)
        self.submit_button.pack(fill='x', padx=10, pady=5)

        self.text = tk.Text(root, bg='#2B2B2B', fg='white', bd=0, highlightthickness=0)
        self.text.pack(padx=10, pady=5)

        self.hyperlink = HyperlinkManager(self.text)

        self.text.insert(tk.INSERT, "Made by ", "")
        self.text.insert(tk.INSERT, "Jaiden", self.hyperlink.add(self.open_url))
        self.text.config(state=tk.DISABLED) # to make the text read-only

    def open_url(self):
        import webbrowser
        webbrowser.open("https://github.com/RiceFarmer01")

    def get_headers(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        try:
            response = requests.get(url)
            headers = response.headers

            with filedialog.asksaveasfile(mode='w', defaultextension=".txt") as output_file:
                output_file.write("Response headers from the server:\n")
                for key, value in headers.items():
                    output_file.write(f"{key}: {value}\n")
            
            messagebox.showinfo("Success", "Headers written to file successfully.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

root = tk.Tk()
app = HeaderAnalyzer(root)
root.mainloop()