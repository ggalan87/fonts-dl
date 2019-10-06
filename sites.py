from bs4 import BeautifulSoup
import requests
import zipfile
import io
from requests_html import HTMLSession
import re


class FontSite:
    def download(self):
        pass


class AkaAcid(FontSite):
    def __init__(self):
        self.name = 'aka-acid'
        self.base_url = 'http://aka-acid.com/'

        self.fonts_pages = \
            {
                'script': 'scriptfonts.html',
                'text': 'textfonts.html',
                'pixel': 'pixelfonts.html'
            }

    def download(self):
        for fp in self.fonts_pages:
            print('Downloading {} fonts'.format(fp))

            font_url = self.base_url + self.fonts_pages[fp]

            session = HTMLSession()
            r = session.get(font_url)

            if r.status_code != 200:
                exit()

            r.html.render()
            soup = BeautifulSoup(r.text, 'html.parser')

            # First two and last two containers are not fonts
            fonts_divs = soup.find_all('div', id=lambda x: x and x.endswith('_hype_container'))[2:-2]

            for fd in fonts_divs:

                font_script_url = self.base_url + fd.contents[1].attrs['src']
                print(font_script_url)
                r = session.get(font_script_url)
                font_html = re.findall('\w*.html', r.text)[0]

                r = session.get(self.base_url + font_html)

                font_id = font_html.split('.')[0]

                if r.status_code != 200:
                    print(font_id, 'does not exist')
                else:
                    print('Font {}'.format(font_id))

                font_soup = BeautifulSoup(r.text, 'html.parser')
                dl_img = font_soup.find('img', id='download')

                zip_file_url = self.base_url + dl_img.parent.attrs['href']

                zr = requests.get(zip_file_url)
                z = zipfile.ZipFile(io.BytesIO(zr.content))
                z.extractall('./fonts/{}-{}'.format(self.name, fp))


__font_sites = {
    'aka-acid': AkaAcid,
}


def initialize_site(name):
    if name not in __font_sites:
        raise ValueError('Invalid site name. Received: "{}", supported sites: {}'.format(name, __font_sites.keys()))
    return __font_sites[name]()
