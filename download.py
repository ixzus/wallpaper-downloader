from bs4 import BeautifulSoup
import requests
import sys

category = sys.argv[1]

try:
    page_index = [int(sys.argv[2])]
    page_end = int(sys.argv[3])
except:
    print('The second and third arguments must be a number but not string!')

PAGE_DOMAIN = 'http://wallpaperswide.com'
PAGE_URL = 'http://wallpaperswide.com/' + category + '-desktop-wallpapers/page/'

def visit_page(url):
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    }
    r = requests.get(url, headers = headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml')
    return soup

def get_paper_link(page):
    links = page.select('#content > div > ul > li > div > div a')
    collect = []

    for link in links:
        collect.append(link.get('href'))

    return collect

def download_wallpaper(link, index, total, callback):
    wallpaper_source = visit_page(PAGE_DOMAIN + link)
    wallpaper_size_links = wallpaper_source.select('#wallpaper-resolutions > a')
    size_list = []

    for link in wallpaper_size_links:
        href = link.get('href')
        size_list.append({
            'size': eval(link.get_text().replace('x', '*')),
            'name': href.replace('/download/', ''),
            'url': href
        })

    biggest_one = max(size_list, key = lambda item: item['size'])
    print('Downloading the ' + str(index + 1) + '/' + str(total) + ' wallpaper: ' + biggest_one['name'])
    result = requests.get(PAGE_DOMAIN + biggest_one['url'])

    if result.status_code == 200:
        open('wallpapers/' + biggest_one['name'], 'wb').write(result.content)

    if index + 1 == total:
        print('Download completed!\n\n')
        callback()

def start():
    if page_index[0] <= page_end:
        print('Preparing to download the ' + str(page_index[0])  + ' page of all the "' + category + '" wallpapers...')
        PAGE_SOURCE = visit_page(PAGE_URL + str(page_index[0]))
        WALLPAPER_LINKS = get_paper_link(PAGE_SOURCE)
        page_index[0] = page_index[0] + 1

        for index, link in enumerate(WALLPAPER_LINKS):
            download_wallpaper(link, index, len(WALLPAPER_LINKS), start)

if __name__ == '__main__':
     start()
