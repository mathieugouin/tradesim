from __future__ import print_function
from six.moves import urllib
import sys


def download_url(url):
    """Download a URL and provide the result as a big string."""
    s = ""
    try:
        f = urllib.request.urlopen(url, timeout=2)
        if sys.version_info.major > 2:
            charset = f.info().get_content_charset()
        else:
            charset = f.headers.getparam('charset')

        if charset is None:  # Default according to HTTP
            charset = 'iso-8859-1'

        r = f.read()
        s = r.decode(charset)

    except urllib.error.URLError as e:
        print("URLError: {}".format(e))
        if hasattr(e, 'reason'):
            print('Failed to reach the server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
    except Exception as e:
        print("Unknown Exception: {}".format(e))
    return s


def _main():
    print(sys.version_info)
    url_array = [
        'https://www.google.ca',
        'https://www.bad234123421342134.com',
        'https://www.tmall.com',
        'https://tmxmoney.com/en/index.html',
    ]
    for url in url_array:
        print(download_url(url)[:50])
        print('DL ' + url)


if __name__ == '__main__':
    _main()
