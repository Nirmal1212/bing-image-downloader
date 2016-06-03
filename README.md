# bing-image-downloader
This repo contains the python script for programatic bing image search and saving all the results in a set of JSON files suitable to download

## Sample Response by running the bing_image_search.py script
```
Nirmals-MacBook-Pro:bing-image-downloader nirmal$ python bing_image_search.py
Searching for .. men Formal Shirt
Searching for .. hats and caps
Searching for .. women jewellery
Searching for .. mens belt

File saved at bingImages/bing_results.json with 200 number of files

Search results saved at bingImages/bing_results_search_res.json with 200 number of search results
Processed file saved at nodupes_bing_results.json

*********
sample search result =
{'height': u'1000', 'width': u'1000', 'file_size': u'156225', 'content_type': u'image/jpeg', 'title': u"Bluemint Men's Formal Shirts 2014 (3)", 'search_term': 'men Formal Shirt', 'source_url': u'http://thebestfashionblog.com/mens-fashion/bluemint-mens-formal-shirts-2014', 'id': u'1cadcd14-c858-45e2-af95-60a881cdbb3f', 'media_url': u'http://thebestfashionblog.com/wp-content/uploads/2014/03/Mens-Formal-Shirts-2014-3.jpg'}

*********
sample converted result for downloading =
[u'http://thebestfashionblog.com/wp-content/uploads/2014/03/Mens-Formal-Shirts-2014-3.jpg', u'bingImages/men Formal Shirt/Mens-Formal-Shirts-2014-3.jpg']

```

Installation
=====
#####for python 2.7.* 

```pip install py-bing-search```

#####for python 3.*

```pip3 install py-bing-search```

*Requires the requests library.

Usage
=====

Remember to set the `API_KEY` as your own.

####For Web Results:

```py
from py_bing_search import PyBingWebSearch
search_term = "Python Software Foundation"
bing_web = PyBingWebSearch('Your-Api-Key-Here', search_term, web_only=False) # web_only is optional, but should be true to use your web only quota instead of your all purpose quota
first_fifty_result= bing_web.search(limit=50, format='json') #1-50
second_fifty_result= bing_web.search(limit=50, format='json') #51-100

print (second_fifty_result[0].description)
u'Python Software Foundation Home Page. The mission of the Python Software Foundation is to promote, protect, and advance the Python programming language, and to ...'

```

What you get is a list of WebResult() instances, each comes with the following values:

```py
self.title: title of the result
self.url: the url of the result
self.description: description for the result
self.id: bing id for the page

#Meta info:
self.meta.uri: the search uri for bing
self.meta.type: for the most part WebResult
```

####For Image Results:

```py
from py_bing_search import PyBingImageSearch
bing_image = PyBingImageSearch('Your-Api-Key-Here', "x-box console")
first_fifty_result= bing_image.search(limit=50, format='json') #1-50
second_fifty_result= bing_image.search(limit=50, format='json') #51-100
print (second_fifty_result[0].media_url)
```

What you get is a list of ImageResult() instances, each comes with the following values:

```py
self.id: id of the result
self.title: title of the resulting image
self.media_url: url to the full size image
self.source_url: url of the website that contains the source image
self.width: width of the image
self.height: height of the image
self.file_size: size of the image (in bytes) if available
self.content_type the MIME type of the image if available
self.meta: meta info

#Meta info#:
meta.uri: the search uri for bing
meta.type: for the most part ImageResult
```

####For Video Results:

```py
from py_bing_search import PyBingVideoSearch
bing_video = PyBingVideoSearch('Your-Api-Key-Here', "cats")
first_fifty_result= bing_video.search(limit=50, format='json') #1-50
second_fifty_result= bing_video.search(limit=50, format='json') #51-100
print (second_fifty_result[0].media_url)
```

What you get is a list of VideoResult() instances, each comes with the following values:

```py
self.id: id of the result
self.title: title of the resulting Video
self.media_url: url to the full size Video
self.display_url: url to display on the search result.
self.run_time: run time of the video
self.meta: meta info

#Meta info#:
meta.uri: the search uri for bing
meta.type: for the most part VideoResult
```

####For News Results:

```
from py_bing_search import PyBingNewsSearch
bing_news = PyBingNewsbSearch('Your-Api-Key-Here', "US Election")
first_fifty_result= bing_news.search(limit=50, format='json') #1-50
second_fifty_result= bing_news.search(limit=50, format='json') #51-100
print (second_fifty_result[0].url)
```

What you get is a list of NewsResult() instances, each comes with the following values:

```py
self.id: id of the result
self.title: title of the resulting News
self.url: url to the News
self.description: description of the article
self.date: date of the News
self.meta: meta info

#Meta info#:
meta.uri: the search uri for bing
meta.type: for the most part NewsResult
```

## Searching for a specific number of results.

You can also run __*search_all*__ to keep searching until it fills your required quota. Note that this will make an unpredictable number of api calls (hence drains your credits).

```py
from py_bing_search import PyBingWebSearch
bing_web = PyBingNewsbSearch('Your-Api-Key-Here', "Python Software Foundation")
result_list = bing_web.search_all(limit=130, format='json') #will return result 1 to 130
len(result_list) == 130
True
result_list = bing_web.search_all(limit=130, format='json') #will return result 131 to 260
```