import requests
import bs4
import time


def get_title(soup):
    title = soup.find('h1')
    if title is None:
        return 'Unknown'
    return title.text.strip()

def get_content(soup):
    content = soup.find('div', attrs={'id': 'content'})
    return content.text.replace('　　', '\n\n').replace('\n\nchaptererror();', '').strip()

def get_next(soup):
    nxt = soup.find('a', attrs={'class': 'next'})
    if nxt['href'][-1] != 'l':
        return None

    return nxt['href']

if __name__ == '__main__':
    base = 'https://www.qu.la/book/145675/'
    url = 'https://www.qu.la/book/145675/7469043.html'
    fout = open('我的绝美鬼夫.txt', 'wb')

    sess = requests.Session()
    sess.headers.update({
        'Referer': 'https://www.qu.la/book/145675/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        })

    while url is not None:
        succ = False
        cnt = 0
        while not succ and cnt < 3:
            try:
                cnt += 1
                page = sess.get(url, timeout=3)
                succ = True
            except Exception as e:
                print(e)

        soup = bs4.BeautifulSoup(page.text, 'html5lib')
        title = get_title(soup)
        content = get_content(soup)
        nxt = get_next(soup)
        url = None if nxt is None else '{}{}'.format(base, nxt)
        fout.write((title + '\n').encode('utf8'))
        fout.write((content + '\n').encode('utf8'))
        print(title)
        time.sleep(3)

    fout.close()