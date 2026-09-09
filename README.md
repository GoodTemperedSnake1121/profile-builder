# Profile Builder

A simple Python/Tkinter profile manager designed to make profile creation and management easy.

## Features

- Easy manual profile entry
- Open and save `.profile` files
- Proprietary binary `.profile` container format
- Versioned file format for future compatibility
- Compressed JSON payload inside the binary container
- Human-readable profile preview in the GUI
- Uses Python's standard library and Tkinter

## `.profile` format

Profile Builder stores profiles as a small binary container rather than plain text.

The format currently uses:

- `PBLD` magic bytes
- Format version `1`
- A 4-byte big-endian payload length
- A zlib-compressed UTF-8 JSON payload

The format is proprietary to Profile Builder but **is not encrypted**. Anyone who knows the format can decode the contents. Do not use `.profile` files for secrets or sensitive information that needs confidentiality.

The format is versioned so future versions can add fields or change the encoding without silently misreading older files.

## Requirements

- Python 3
- Tkinter

On Debian/Ubuntu-based Linux systems, Tkinter may be installed with:

```bash
sudo apt install python3-tk
```

## Run

```bash
python3 profile_builder.py
```

## License

MIT License. See [LICENSE](LICENSE).
