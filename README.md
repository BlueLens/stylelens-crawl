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

### Step 1: Import the stylelens crawl library
    from stylelens_crawl.stylens_crawl import StylensCrawler

### Step 2: Set the crawling option
    options = {
        'host_code': 'HC0001'
    }
 

### Step 3: Create a stylelens crawl object
    sty = StylensCrawler(options)


### Step 4: Call a start function
The crawling task time is vary up to your internet speed.
It will be returned 'True' when successfully completed. 

    sty.start():

### Step 5: Get a crawling result data.
    sty.get_items()
        
### Step 6: Save a crawling result data to Stylens Server
    sty.save_items()
        
List of supported shopping malls
------------------
1. [De-bow](http://de-bow.co.kr) / HC0002
2. [육육걸즈](http://66girls.co.kr) / HC0001
