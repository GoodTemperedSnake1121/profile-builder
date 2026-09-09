# Profile Builder

A simple Python/Tkinter profile manager designed to make profile creation and management easy.

## Features

- Easy manual profile entry
- Open and save `.profile` files
- Supports both the original text `.profile` files and the current binary format
- Automatically converts legacy text profiles when they are saved again
- Proprietary binary `.profile` container format
- Versioned file format for future compatibility
- Compressed JSON payload inside the binary container
- Human-readable profile preview in the GUI
- Uses Python's standard library and Tkinter

## `.profile` format

New profiles are stored as a small binary container rather than plain text.

The current format uses:

- `PBLD` magic bytes
- Format version `1`
- A 4-byte big-endian payload length
- A zlib-compressed UTF-8 JSON payload

The format is proprietary to Profile Builder but **is not encrypted**. Anyone who knows the format can decode the contents. Do not use `.profile` files for secrets or sensitive information that needs confidentiality.

### Legacy text profiles

Earlier versions of Profile Builder saved `.profile` files as human-readable text. The current version can still open those files.

When an old text profile is opened, its contents are loaded into the editor and a notice is shown. Saving it again writes it in the current binary format.

The original text format stored the complete address on one line, so its individual Street, Number, Town, and Country components cannot always be recovered reliably. For legacy files, the complete address is therefore loaded into the Street field rather than being silently discarded.

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
