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

To pull `webms` and merge them into one file using [wambala](http://github.com/zeionara/wambala):

```sh
python -m bull pull https://2ch.hk/b/res/299434735.html assets/webm-01
$HOME/wambala/run.sh assets/webm-01

vlc assets/wemb-01.mp4
```
