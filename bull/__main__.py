import os
import re
from time import sleep

from click import group, argument, option
from requests import Session
from requests.exceptions import ConnectTimeout, SSLError
from tqdm import tqdm


TIMEOUT = 300
MEDIA_URL_PATTERN = re.compile(r'/b[^"]+\.(?:mp4|webm)')

N_ATTEMPTS = 3


@group
def main():
    pass


def _pull(url: str, destination: str):
    session = Session()

    if 'arhivach' in url:
        parts = url.split('/')

        prefix = '/'.join((parts[0], parts[1], f'i.{parts[2]}', 'storage'))
    else:
        prefix = '/'.join(url.split('/')[:3])

    print(f'Querying page {url}...')

    response = session.get(url, timeout = TIMEOUT)

    print(f'Got page {url}...')

    assert response.status_code == 200

    page = response.text

    if not os.path.isdir(destination):
        os.makedirs(destination)

    urls = []

    for match in MEDIA_URL_PATTERN.findall(page):
        urls.append(f'{prefix}{match}')

    urls = tuple(set(urls))

    print(f'Found {len(urls)} urls')
    pbar = tqdm(urls)

    for url in pbar:
        path = os.path.join(destination, url.split('/')[-1])

        pbar.set_description(f'Handling file {url} -> {path}')

        if os.path.isfile(path):
            continue

        attempt_count = 0

        while True:
            try:
                os.system(f'wget -T {TIMEOUT} -O {path} {url} -q')
            except (ConnectTimeout, SSLError):
                if attempt_count < N_ATTEMPTS:
                    attempt_count += 1
                    continue
                raise

        # n_attempts = N_ATTEMPTS
        # failed = False

        # while True:
        #     try:
        #         response = session.get(url, timeout = TIMEOUT, headers = headers)
        #     except ConnectTimeout:
        #         if n_attempts > 0:
        #             n_attempts -= 1
        #         else:
        #             failed = True
        #             break

        # if failed:
        #     print(f'Failed to pull {url} after {N_ATTEMPTS} attempts. Skipping...')
        #     continue

        # if response.status_code == 200:
        #     with open(path, 'wb') as file:
        #         file.write(response.content)
        # else:
        #     print(f'Can\'t download file {url}: response status is {response.status_code}')


@main.command()
@argument('url', type = str)
@argument('destination', type = str, default = 'assets')
@option('-i', '--interval', type = float, default = None)
def pull(url: str, destination: str, interval: float):
    if not os.path.isdir(destination):
        os.makedirs(destination)

    if interval is None:
        _pull(url, destination)
    else:
        while True:
            try:
                _pull(url, destination)
            except AssertionError:
                print('Stop pooling')
                break
            else:
                print(f'Making a pause for {interval} seconds before checking again...')
                sleep(interval)


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
