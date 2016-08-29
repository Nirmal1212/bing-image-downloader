## Python program to download the images given an URL and destination location on a JSON file
#
# python im_downloader.py input.json des_folder/
# 
# Author : Nirmalkumar Sathiamurthi
# Date : Aug 19 2016
#
import sys
if 'threading' in sys.modules:
    del sys.modules['threading']
import os
import urllib2
import traceback
import hashlib
import json
import gevent
from gevent import monkey
from gevent.fileobject import FileObjectThread

monkey.patch_all()
failed_imgs = []

def download_image(url, fname, local_path):

    try:
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        r = urllib2.urlopen(req, timeout=10)
        ctype = r.info().getheader('Content-Type')

        if r.code == 200:
            img_path = '/'.join(fname.split('/')[:-1])  # remove fname.jpg from path
            img_path = local_path + img_path
            fname = local_path + fname
            if not os.path.exists(img_path):
                print "CREATED DIRECTORY ::: " + img_path
                os.makedirs(img_path.decode('utf-8').encode('ascii', 'ignore'), 0755);
                print "path created"
            # success
            with open(fname, 'wb') as fd:
                f = FileObjectThread(fd, "wb")
                f.write(r.read())
                f.close()
                return True
    except:
        global failed_imgs
        failed_imgs.append((url, fname))
        print "Error: {}".format(url)
        print traceback.format_exc()
        return False

print 'Got input params {}'.format(sys.argv)
inputFile, des_folder = sys.argv[1], sys.argv[2]
if not des_folder.endswith('/'):
    des_folder+="/"
batch_num = 0
with open(inputFile) as f:
    images = json.load(f)
    batch_urls = []
    images_len = len(images)
    for i, url in enumerate(images):
        if os.path.exists(url[1]):
            continue
        batch_urls.append(url)
        if (i%100 == 0) or (i == images_len-1):
            batch_num += 1
            print "processing batch num", batch_num
            download_files = [gevent.spawn(lambda x: download_image(x[0], x[1], des_folder), x) for x in batch_urls]
            gevent.joinall(download_files)
            batch_urls = []

            print "total failed: %s" % (len(failed_imgs))
json.dump(failed_imgs, open(des_folder+'failed.json', 'w'), indent=4)
