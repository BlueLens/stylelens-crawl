from urllib.parse import urlparse


def make_url(domain, location):
    url = urlparse(location)
    if url.scheme == '' and url.netloc == '':
        if len(url.query):
            return domain + url.path + '?' + url.query
        else:
            return domain + url.path
    elif url.scheme == '':
        if len(url.query):
            return 'http://' + url.netloc + url.path + '?' + url.query
        else:
            return 'http://' + url.netloc + url.path
    else:
        return url.geturl()
