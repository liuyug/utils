#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import time
import gzip
import random

from six.moves.urllib.error import URLError
from six.moves.urllib.request import Request, build_opener, HTTPCookieProcessor
from six.moves.urllib.parse import urlencode
from six.moves.http_cookiejar import CookieJar

# pysocks
import socks
from sockshandler import SocksiPyHandler


def get_user_agent(idx=-1):
    user_agent = [
        'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20130619 Firefox/17.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    ]
    if idx < 0:
        idx = random.randint(0, len(user_agent) - 1)
    return user_agent[idx]


def url_downloader(url, data=None, path=None, cookie=None,
                   timeout=5, retry=1, retry_ivl=5, agent=None, proxy=None):
    """Download URL link
    url:    url to download
    data:   post data
    path:   download to local file
    timeout:    socket timeout
    retry:  retry times to download url
    retry_ivl:  interval time when retry
    agent:  http user agent
    proxy:  socks5://127.0.0.1:1080
    """
    while True:
        try:
            if isinstance(data, dict):
                data = urlencode(data).encode('ascii')
            request = Request(url, data=data)
            request.add_header('User-Agent', agent or get_user_agent())
            if data:
                request.add_header(
                    'Content-Type',
                    'application/x-www-form-urlencoded;charset=utf-8')
            response = None
            handlers = []
            if proxy:
                scheme, host, port = proxy.split(':')
                host = host.strip('/')
                proxy_handler = SocksiPyHandler(
                    socks.PROXY_TYPES[scheme.upper()], host, int(port)
                )
                handlers.append(proxy_handler)
            if cookie is None:
                cookie = CookieJar()
            cookie_handler = HTTPCookieProcessor(cookie)
            handlers.append(cookie_handler)

            opener = build_opener(*handlers)
            response = opener.open(request, timeout=timeout)
            content_encoding = response.info().get('content-encoding')
            if content_encoding:
                r_data = gzip.decompress(response.read())
            else:
                r_data = response.read()
            if path:
                with open(path, 'wb') as f:
                    f.write(r_data)
                r_data = None
            response.close()
            mime = response.info().get('content-type')
            real_url = response.geturl()
            err_msg = 'Ok'
            break
        except (URLError, IOError, OSError) as err:
            response and response.close()
            retry -= 1
            err_msg = str(err)
            if retry > 0:
                time.sleep(retry_ivl)
                retry_ivl += retry_ivl
                timeout += timeout
            else:
                mime = r_data = real_url = None
                break
    return {
        'mime': mime,
        'path': path,
        'data': r_data,
        'url': real_url,
        'cookie': cookie,
        'error': err_msg,
    }
