stylelens-crawl
========
Shopping mall crawling library for stylens.

Requirements
------------------
* Python 3.6+

Installation
------------------
    pip install stylelens-crawl

Getting Started
------------------
[The Example code](test/test.py):

    # If the crawling task completed
    if sty.start():
        # Get a crawling result data.
        sty.get_items()
        # Save a crawling result data to Stylens Server
        sty.save_items()
        
List of supported shopping malls
------------------
1. [De-bow](http://de-bow.co.kr) / HC0002
2. [육육걸즈](ttp://66girls.co.kr) / HC0001
