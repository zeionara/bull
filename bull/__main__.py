import os, re

from click import group, argument
from requests import get
from tqdm import tqdm


TIMEOUT = 60
MEDIA_URL_PATTERN = re.compile(r'/b[^"]+\.(?:mp4|webm)')


@group
def main():
    pass


def _pull(url: str, destination: str):
    prefix = '/'.join(url.split('/')[:3])

    response = get(url, timeout = TIMEOUT)

    assert response.status_code == 200

    page = response.text

    if not os.path.isdir(destination):
        os.makedirs(destination)

    urls = []

    for match in MEDIA_URL_PATTERN.findall(page):
        urls.append(f'{prefix}/{match}')

    urls = tuple(set(urls))

    print(f'Found {len(urls)} urls')

    for url in tqdm(urls):
        path = os.path.join(destination, url.split('/')[-1])

        if os.path.isfile(path):
            continue

        response = get(url, timeout = TIMEOUT)

        if response.status_code == 200:
            with open(path, 'wb') as file:
                file.write(response.content)
        else:
            print(f'Can\'t download file {url}: response status is {response.status_code}')


@main.command()
@argument('url', type = str)
@argument('destination', type = str, default = 'assets')
def pull(url: str, destination: str):
    _pull(url, destination)


@main.command()
@argument('thread', type = int)
@argument('destination', type = str)
def dull(thread: int, destination: str):
    path = f'../Downloads/{destination}'

    if not os.path.isdir(path):
        os.makedirs(path)

    _pull(f'https://2ch.hk/b/res/{thread}.html', path)


if __name__ == '__main__':
    main()
