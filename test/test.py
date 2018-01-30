from stylelens_crawl.stylens_crawl import StylensCrawler

options = {
    # 'host_code': 'HC0016'
    'host_code': 'HC1013'
}

# Enable Job Directory
options['job_dir'] = False

# Create the StylensCrawler
sty = StylensCrawler(options)

# If the crawling task completed
if sty.start():
    # Get a crawling result data.
    print('Done crawling.')
    print('count: ' + str(len(sty.get_items())))
    # print('start')