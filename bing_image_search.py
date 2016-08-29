## Python program to scrape images based using search query in Bing Image search
# Signup for a free developer account from Bing and get API key from here https://datamarket.azure.com/dataset/bing/search
#
# Author : Nirmalkumar Sathiamurthi
# Date : June 3 2016
#
from py_bing_search import PyBingImageSearch        # pip install py-bing-search
from collections import OrderedDict
import json
import os
import time

ACCOUNT_KEY = 'YOUR_API_KEY'          #Set your own API key or Account Key here
DEST_FOLDER = 'bingImages'
NUM_RESULTS = 50
FILE_NAME = 'bing_results'   #.json is automattically appended to the file name
search_terms = [
                    "men Formal Shirt",
                    "hats and caps",
                    "women jewellery",
                    "mens belt"
                ]

search_results = []
download_files = []
for term in search_terms:
    print 'Searching for ..',term
    bing = PyBingImageSearch(ACCOUNT_KEY,term)
    res = []
    for n in xrange(50,NUM_RESULTS+1,50):
        res.extend(bing.search(limit=NUM_RESULTS,format='json'))
    
    print 'Got {} items from bing'.format(len(res))
    # Populate the results onto JSON array
    for item in res:
        itm = { 'id':item.id,
                'title':item.title,
                'media_url':item.media_url,
                'source_url':item.source_url,
                'width':item.width,
                'height':item.height,
                'file_size':item.file_size,
                'content_type':item.content_type,
                'search_term':term}
        search_results.append(itm)
        url = item.media_url
        des_path,fname = os.path.join(DEST_FOLDER,term),url.split('/')[-1]
        download_files.append((url,os.path.join(des_path,fname)))
    # break

# Create the destination folder if it does not exist
if os.path.exists(DEST_FOLDER) == False:
    os.makedirs(DEST_FOLDER)

with open(DEST_FOLDER+'/'+FILE_NAME+'.json','w') as outfile:
    json.dump(download_files,outfile,indent=2)
print '\nFile saved at '+DEST_FOLDER+'/'+FILE_NAME+'.json with '+str(len(download_files)) + ' number of files'
with open(DEST_FOLDER+'/'+FILE_NAME+'_search_res.json','w') as outfile:
    json.dump(search_results,outfile,indent=2)
print '\nSearch results saved at '+DEST_FOLDER+'/'+FILE_NAME+'_search_res.json with '+str(len(search_results)) + ' number of search results'

# Remove any repetition in file names in URLs by appending timestamp to the image names
noDupes = []
urls = []
paths = []
for i in download_files:
    url = i[0]
    path = i[1]
#     print url,path
    if url not in urls:
        if path in paths:
            time_stamp = str(int(time.time()*10000)%1000000)+'.'
            path = path.split('.')[0]+time_stamp+path.split('.')[-1]        #Append Timestamp to the file to avoid overwriting of duplicate file names
        noDupes.append([url,path])
        urls.append(url)
        paths.append(path)

with open(DEST_FOLDER+'/nodupes_'+FILE_NAME+'.json','w') as out:
    json.dump(noDupes,out,indent=1)
print 'Processed file saved at '+'nodupes_'+FILE_NAME+'.json'
print '\n*********\nsample search result = '
print search_results[0]
print '\n*********\nsample converted result for downloading = '
print noDupes[0]
print '\n\n'