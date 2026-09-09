# Profile Builder

A simple Python/Tkinter profile manager designed to make profile creation and management easy.

## Features

- Easy manual profile entry
- Open and save `.profile` files
- Supports both the original text `.profile` files and the current binary format
- Automatically converts legacy text profiles when they are saved again
- Open, documented `.profile` binary format
- Versioned file format for future compatibility
- Compressed JSON payload inside the binary container
- Human-readable profile preview in the GUI
- Uses Python's standard library and Tkinter

## `.profile` format

The `.profile` format is **open and fully documented**. The format is not intended to be a secret or tied to the Profile Builder program: anyone can implement a reader or writer for it.

### Binary layout

All integer fields use **big-endian** byte order.

| Offset | Size | Field | Description |
|---|---:|---|---|
| `0` | 4 bytes | Magic | ASCII `PBLD` |
| `4` | 1 byte | Format version | Currently `1` |
| `5` | 4 bytes | Payload length | Unsigned 32-bit big-endian length of the compressed payload |
| `9` | N bytes | Payload | zlib-compressed UTF-8 JSON |

The payload length must exactly match the number of bytes following the 9-byte header.

### JSON payload

After zlib decompression and UTF-8 decoding, version 1 contains a JSON object with this structure:

```json
{
  "version": 1,
  "profile": {
    "Name": "...",
    "Age": "...",
    "Date of Birth": "...",
    "Likes": "...",
    "Does not like": "...",
    "Street": "...",
    "Number": "...",
    "Town": "...",
    "Country": "..."
  }
}
```

The JSON is encoded as UTF-8. JSON is generated with compact separators, but readers should parse JSON normally rather than relying on whitespace or property order.

### Reading and writing `.profile` files

A compatible implementation should:

1. Read and validate the 9-byte header.
2. Check that the magic bytes are `PBLD`.
3. Check the format version.
4. Read exactly the declared compressed payload length.
5. Decompress the payload with zlib.
6. Decode the result as UTF-8.
7. Parse the JSON object.
8. Read the `version` and `profile` members.

Writers should produce the same header structure and a valid zlib-compressed UTF-8 JSON payload.

### Format versioning

The format version allows the format to evolve without silently misreading files. A reader should reject unsupported versions rather than guessing how to interpret them.

### Security

The binary format is **not encryption**. zlib compression only reduces size and obscures the plain text from casual viewing; it does not provide confidentiality. Anyone can decode a `.profile` file using this public specification. Do not use `.profile` files for passwords, secrets, or sensitive information that requires encryption.

### Legacy text profiles

Earlier versions of Profile Builder saved `.profile` files as human-readable text. The current version can still open those files.

When an old text profile is opened, its contents are loaded into the editor and a notice is shown. Saving it again writes it in the current binary format.

The original text format stored the complete address on one line, so its individual Street, Number, Town, and Country components cannot always be recovered reliably. For legacy files, the complete address is therefore loaded into the Street field rather than being silently discarded.

## Reference implementation

`profile_builder.py` contains the reference implementation of the format. The functions `profile_to_blob()` and `blob_to_profile()` implement the current binary format, while `read_profile()` also supports the legacy text format.

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
