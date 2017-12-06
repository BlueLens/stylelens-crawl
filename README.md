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
The crawling task time is vary up to your internet speed.<br/>
It will be returned '<b>True</b>' when successfully completed. 

    sty.start():

### Step 5: Get a crawled result data.
    sty.get_items()

### Step 6: Remove crawled result file. 
    styl.delete_temp_file()
    
List of supported shopping malls
------------------
1. [De-bow](http://de-bow.co.kr) / HC0002
2. [육육걸즈](http://66girls.co.kr) / HC0001
3. [Imvely](http://www.imvely.com/) / HC0003
4. [Stylenanda](http://stylenanda.com/) / HC0004
5. [Thedaze](http://thedaze.kr) / HC0005
6. [Gogosinf](http://ggsing.com/) / HC0006
7. [Merongshop](http://merongshop.com) / HC0007
8. [Angtoo](http://angtoo.com) / HC0008