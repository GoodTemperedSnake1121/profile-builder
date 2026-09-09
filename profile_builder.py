import json
import struct
import tkinter as tk
import zlib
from tkinter import filedialog, messagebox


# .profile file format:
#   4 bytes  magic: PBLD
#   1 byte   format version: 1
#   4 bytes  big-endian compressed payload length
#   N bytes  zlib-compressed UTF-8 JSON payload
MAGIC = b"PBLD"
FORMAT_VERSION = 1
HEADER = struct.Struct(">4sBI")

FIELD_NAMES = (
    "Name", "Age", "Date of Birth", "Likes", "Does not like",
    "Street", "Number", "Town", "Country",
)


def build_profile():
    return {label: fields[label].get().strip() for label in FIELD_NAMES}


def profile_to_blob(profile):
    payload = json.dumps(
        {"version": FORMAT_VERSION, "profile": profile},
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    compressed = zlib.compress(payload, level=9)
    return HEADER.pack(MAGIC, FORMAT_VERSION, len(compressed)) + compressed


def blob_to_profile(data):
    if len(data) < HEADER.size:
        raise ValueError("File is too small to be a Profile Builder file.")

    magic, version, payload_length = HEADER.unpack(data[:HEADER.size])
    if magic != MAGIC:
        raise ValueError("Not a Profile Builder binary .profile file.")
    if version != FORMAT_VERSION:
        raise ValueError(f"Unsupported .profile format version: {version}")

    payload = data[HEADER.size:]
    if len(payload) != payload_length:
        raise ValueError("The .profile file is truncated or corrupted.")

    try:
        decoded = zlib.decompress(payload).decode("utf-8")
        document = json.loads(decoded)
    except (zlib.error, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("The .profile file contains an invalid payload.") from exc

    if document.get("version") != FORMAT_VERSION:
        raise ValueError("The .profile payload version is unsupported.")

    profile = document.get("profile")
    if not isinstance(profile, dict):
        raise ValueError("The .profile file does not contain a valid profile.")

    return {label: str(profile.get(label, "")) for label in FIELD_NAMES}


def legacy_text_to_profile(text):
    """Read the original human-readable .profile format.

    The original format stored all four address fields on one line, so the
    address cannot always be split back into its original components. In that
    case the complete address is placed in the Street field rather than
    silently losing it.
    """
    values = {}
    expected = {
        "Name": "Name",
        "Age": "Age",
        "Date of Birth": "Date of Birth",
        "Likes": "Likes",
        "Does not like": "Does not like",
        "Address": "Address",
    }

    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in expected:
            values[expected[key]] = value.strip()

    required = ("Name", "Age", "Date of Birth", "Likes", "Does not like", "Address")
    if not any(key in values for key in required):
        raise ValueError("The text file does not look like a legacy Profile Builder profile.")

    profile = {label: "" for label in FIELD_NAMES}
    for label in ("Name", "Age", "Date of Birth", "Likes", "Does not like"):
        profile[label] = values.get(label, "")

    # Old files had no separators between Street/Number/Town/Country.
    profile["Street"] = values.get("Address", "")
    return profile


def read_profile(data):
    """Read either the current binary format or the original text format."""
    if data.startswith(MAGIC):
        return blob_to_profile(data), False

    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("The file is neither a valid binary nor a UTF-8 text profile.") from exc

    return legacy_text_to_profile(text), True


def display_profile(profile):
    address = " ".join(
        profile[label] for label in ("Street", "Number", "Town", "Country")
    ).strip()
    return (
        f"Name: {profile['Name']}\n"
        f"Age: {profile['Age']}\n"
        f"Date of Birth: {profile['Date of Birth']}\n"
        f"Likes: {profile['Likes']}\n"
        f"Does not like: {profile['Does not like']}\n"
        f"Address: {address}\n"
    )


def load_fields(profile):
    for label in FIELD_NAMES:
        fields[label].delete(0, tk.END)
        fields[label].insert(0, profile[label])


def open_profile():
    filename = filedialog.askopenfilename(
        filetypes=[("Profile files", "*.profile"), ("All files", "*.*")],
    )
    if not filename:
        return

    try:
        with open(filename, "rb") as file:
            data = file.read()
        profile, legacy = read_profile(data)
    except (OSError, ValueError) as exc:
        messagebox.showerror("Open profile", f"Could not open the selected profile.\n\n{exc}")
        return

    load_fields(profile)
    output.delete("1.0", tk.END)
    output.insert(tk.END, display_profile(profile))

    if legacy:
        messagebox.showinfo(
            "Legacy profile opened",
            "This is an older text .profile file.\n\n"
            "It was loaded successfully. Save it to convert it to the new binary format."
        )
    else:
        messagebox.showinfo("Profile opened", "The profile was opened successfully.")


def save_profile():
    profile = build_profile()
    data = profile_to_blob(profile)

    filename = filedialog.asksaveasfilename(
        defaultextension=".profile",
        filetypes=[("Profile files", "*.profile"), ("All files", "*.*")],
        initialfile="profile.profile",
    )
    if not filename:
        return

    try:
        with open(filename, "wb") as file:
            file.write(data)
    except OSError:
        messagebox.showerror("Save profile", "Could not save the profile.")
        return

    output.delete("1.0", tk.END)
    output.insert(tk.END, display_profile(profile))
    messagebox.showinfo("Profile saved", "The profile was saved successfully.")


root = tk.Tk()
root.title("Profile Builder")
root.resizable(False, False)

form = tk.Frame(root, padx=16, pady=16)
form.pack()

fields = {}
for row, label in enumerate(FIELD_NAMES):
    tk.Label(form, text=f"{label}:").grid(row=row, column=0, sticky="w", pady=3)
    entry = tk.Entry(form, width=38)
    entry.grid(row=row, column=1, pady=3, padx=(8, 0))
    fields[label] = entry

tk.Button(form, text="Open .profile", command=open_profile).grid(
    row=len(FIELD_NAMES), column=0, pady=(12, 8), sticky="ew"
)
tk.Button(form, text="Save .profile", command=save_profile).grid(
    row=len(FIELD_NAMES), column=1, pady=(12, 8), sticky="ew", padx=(8, 0)
)

tk.Label(form, text="Output:").grid(row=len(FIELD_NAMES) + 1, column=0, sticky="nw")
output = tk.Text(form, width=38, height=7, state=tk.NORMAL)
output.grid(row=len(FIELD_NAMES) + 1, column=1, padx=(8, 0))

root.mainloop()
