import os, re

from click import group, argument
from requests import get
from tqdm import tqdm


TIMEOUT = 60
MEDIA_URL_PATTERN = re.compile(r'/b[^"]+\.(?:mp4|webm)')


@group
def main():
    pass


@main.command()
@argument('url', type = str)
@argument('destination', type = str, default = 'assets')
def pull(url: str, destination: str):
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

        response = get(url, timeout = TIMEOUT)

        if response.status_code == 200:
            with open(path, 'wb') as file:
                file.write(response.content)
        else:
            print(f'Can\'t download file {url}: response status is {response.status_code}')


if __name__ == '__main__':
    main()
