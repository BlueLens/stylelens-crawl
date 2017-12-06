from stylelens_crawl.stylens_crawl import StylensCrawler

options = {
    'host_code': 'HC0007'
}

sty = StylensCrawler(options)

# If the crawling task completed
if sty.start():

    # Get a crawling result data.
    print(len(sty.get_items()))
