from stylelens_crawl.stylens_crawl import StylensCrawler

sty = StylensCrawler('HC0001')

# If the crawling task completed
if sty.start():

    # Get a crawling result data.
    sty.get_items()

    # Save a crawling result data to Stylens Server
    sty.save_items()
