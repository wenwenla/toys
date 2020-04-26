import os
import argparse
import requests
import bs4


def parse_download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'GB18030'
    soup = bs4.BeautifulSoup(response.text, 'html5lib')
    table = soup.find_all('table')[0]
    caption = table.find('caption').find('a').text
    urls = table.find_all('tr')[1:]
    result = []
    for u in urls:
        u = u.find_all('td')
        title = u[1].text.strip()
        url = u[4].find('a')['href']
        result.append((title, url))
    return caption.strip(), result


def download_text(book_title, title, url):
    root = './book/{}'.format(book_title)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
    }
    result = requests.get(url, headers=headers)
    with open(os.path.join(root, 'all.txt'), 'ab') as f:
        f.write(('\n\n##' + title + '\n\n').encode('utf8'))
        f.write(result.content.decode('GB18030').encode('utf8'))


def main():
    parser = argparse.ArgumentParser(description='Download txt from download page of [http://book.suixw.com/]')
    parser.add_argument('--url', dest='url', required=True, help='the url of download page')
    args = parser.parse_args()
    caption, urls = parse_download_page(args.url)
    path = './book/{}'.format(caption)
    if not os.path.exists(path):
        os.mkdir(path)

    if os.path.exists(os.path.join(path, 'all.txt')):
        os.remove(os.path.join(path, 'all.txt'))

    for url in urls:
        print('Downloading {}...'.format(url[0]))
        download_text(caption, url[0], url[1])


if __name__ == '__main__':
    main()
