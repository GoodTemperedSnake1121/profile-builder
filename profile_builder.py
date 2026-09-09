import tkinter as tk
from tkinter import filedialog, messagebox


def open_profile():
    filename = filedialog.askopenfilename(
        filetypes=[("Profile files", "*.profile"), ("All files", "*.*")],
    )
    if not filename:
        return

    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
    except OSError:
        messagebox.showerror("Open profile", "Could not open the selected profile.")
        return

    output.delete("1.0", tk.END)
    output.insert(tk.END, content)
    messagebox.showinfo("Profile opened", "The profile was opened successfully.")


def save_profile():
    values = {label: entry.get().strip() for label, entry in fields.items()}
    address = " ".join(values.pop(label) for label in ("Street", "Number", "Town", "Country"))

    profile = (
        f"Name: {values['Name']}\n"
        f"Age: {values['Age']}\n"
        f"Date of Birth: {values['Date of Birth']}\n"
        f"Likes: {values['Likes']}\n"
        f"Does not like: {values['Does not like']}\n"
        f"Address: {address}\n"
    )

    filename = filedialog.asksaveasfilename(
        defaultextension=".profile",
        filetypes=[("Profile files", "*.profile"), ("All files", "*.*")],
        initialfile="profile.profile",
    )
    if filename:
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(profile)
        except OSError:
            messagebox.showerror("Save profile", "Could not save the profile.")
            return

        output.delete("1.0", tk.END)
        output.insert(tk.END, profile)
        messagebox.showinfo("Profile saved", "The profile was saved successfully.")


root = tk.Tk()
root.title("Profile Builder")
root.resizable(False, False)

form = tk.Frame(root, padx=16, pady=16)
form.pack()

fields = {}
field_names = (
    "Name", "Age", "Date of Birth", "Likes", "Does not like",
    "Street", "Number", "Town", "Country",
)
for row, label in enumerate(field_names):
    tk.Label(form, text=f"{label}:").grid(row=row, column=0, sticky="w", pady=3)
    entry = tk.Entry(form, width=38)
    entry.grid(row=row, column=1, pady=3, padx=(8, 0))
    fields[label] = entry

tk.Button(form, text="Open .profile", command=open_profile).grid(
    row=len(field_names), column=0, pady=(12, 8), sticky="ew"
)
tk.Button(form, text="Save .profile", command=save_profile).grid(
    row=len(field_names), column=1, pady=(12, 8), sticky="ew", padx=(8, 0)
)

tk.Label(form, text="Output:").grid(row=len(field_names) + 1, column=0, sticky="nw")
output = tk.Text(form, width=38, height=7, state=tk.NORMAL)
output.grid(row=len(field_names) + 1, column=1, padx=(8, 0))

root.mainloop()
