import requests
import bs4
import re
from lzstring import LZString
import json
import time
import os
import itertools
import argparse


class ComicDownloader(object):

    def __init__(self):
        self.sess = requests.Session()
        self.sess.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'})
        self.root = './'
        self.comic_path = ''
        

    def download(self, url, rt='./'):
        self.root = rt
        home_page = self.sess.get(url)

        res = self.parse_chapter(home_page.text)
        
        index = list(res.keys())
        for i, k in enumerate(index):
            print('{}: {}'.format(i, k))
        
        demands = map(int, input('Input index: ').split())
        
        for demand in demands:
            k = index[demand]
            v = res[k]
            js = self.parse_page(v)
            self.sess.headers.update({
            'Referer': v
            })
            # print(js)

            now_dict = json.loads(self.parse_js(js))
            print(now_dict)
            # break

            if not self.comic_path:
                regex = re.compile(r'[~!@#$%^&*()_+?:;,<>/\\]')
                bname = now_dict['bname']
                bname = regex.sub('_', bname)
                self.comic_path = os.path.join(self.root, bname)
                print(self.comic_path)
            
                if not os.path.exists(self.comic_path):
                    os.mkdir(self.comic_path)

            self.download_img(now_dict)

    def parse_chapter(self, text):
        chapter_result = {}
        soup = bs4.BeautifulSoup(text, 'html5lib')
        chapter_list = soup.find_all('div', attrs={'class': 'chapter-list'})
        for cp in chapter_list:
            for url in cp.find_all('a'):
                chapter_result[url['title']] = 'https://www.manhuagui.com/' + url['href']

        return chapter_result


    def parse_page(self, url):
        js = ''
        response = self.sess.get(url)
        soup = bs4.BeautifulSoup(response.text, 'html5lib')
        for _ in soup.find_all('script'):
            if _.text[0:6] == 'window':
                js = _.text
                break
        return js

    def parse_js(self, js):
        param = js[js.find('}(')+2:-1]
        p1_end = param[1:].find('\'') + 1
        p1 = param[1:p1_end]
        param = param[p1_end+2:]
        p2_end = param.find(',')
        p2 = int(param[:p2_end])
        param = param[p2_end+1:]
        p3_end = param.find(',')
        p3 = int(param[:p3_end])
        param = param[p3_end+2:]
        p4_end = param.find('\'')
        p4 = param[:p4_end]
        p5 = 0
        p6 = {}
        (p, a, c, k, e, d) = (p1, p2, p3, p4, p5, p6)
        k = LZString.decompressFromBase64(k).split('|');
        lenk = len(k)
        left = lenk - 10 - 26
            
        key = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        index = 0
        for i in key:
            d[i] = k[index] if k[index] else i
            index += 1
            if index == lenk:
                break
        if index != lenk:
            for i in itertools.product('123456789', '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'):
                tmp = i[0] + i[1]
                d[tmp] = k[index] if k[index] else tmp
                index += 1
                if index == lenk:
                    break
        
        print('d: ', d)
        
        ac_list = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        now_rep = ''
        res = ''
        for i in p:
            if i in ac_list:
                now_rep += i
            else:
                res += d[now_rep] if now_rep in d else now_rep
                now_rep = ''
                res += i
        if now_rep:
            res += d[now_rep] if now_rep in d else now_rep
        res = res[res.find('{'):res.rfind('}')+1]
        # print(res)
        
        return res


    def download_img(self, source):
        chapter_path = os.path.join(self.comic_path, source['cname'])
        if not os.path.exists(chapter_path):
            os.mkdir(chapter_path)
        print(chapter_path)
        prefix = 'https://i.hamreus.com'
        prefix += source['path']
        cnt = 1
        for f in source['files']:
            url = '{}{}?cid={}&md5={}'.format(prefix, f, source['cid'], source['sl']['md5'])
            print('Grabing {}...'.format(url))
            try_cnt = 0
            succ = False
            file_path = os.path.join(chapter_path, '{:03d}.jpg.webp'.format(cnt))

            if os.path.exists(file_path):
                # This file has been downloaded
                print('Pass {}.'.format(cnt))
            else:
                while not succ and try_cnt < 3:
                    try:
                        res = self.sess.get(url, timeout=9)
                        if res.status_code == 200:
                            with open(file_path, 'wb') as f:
                                f.write(res.content)
                            succ = True
                    except Exception as e:
                        print(e)
                        try_cnt += 1
     
                if succ:
                    print('get {} success.'.format(cnt))
                else:
                    with open(os.path.join(self.comic_path, 'error.log'), 'a') as error_log:
                        error_log.writelines('{} get {} failed!\n'.format(source['cname'], cnt))
            # time.sleep(2)
            cnt += 1
            
            
if __name__ == '__main__':
    '''
    example:
    python down_comic.py --url=https://www.manhuagui.com/comic/17023/
    '''
    parser = argparse.ArgumentParser(description='Input download homepage')
    parser.add_argument('-u', '--url', metavar='url', dest='url', required=True, help='download homepage')
    args = parser.parse_args()
    downloader = ComicDownloader()
    downloader.download(args.url)