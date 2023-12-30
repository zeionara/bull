# Bull

Download all media from a web page

## Requirements

The tool uses the following pythong packages:

- `requests`
- `click`
- `tqdm`

## Usage

To use the tool pass url to the web page, and path to the destination folder (`./assets` by default):

```sh
python -m bull pull https://example.com/media.html /home/$USER/Downloads
```
