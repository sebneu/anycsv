#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import logging
logger = logging.getLogger(__name__)
import os
import gzip

import requests
import io
import logging
from contextlib import closing
def getContentFromDisk(fname_csv, max_lines=-1):
    if fname_csv[-3:] == '.gz':
        with gzip.open(fname_csv, 'rb') as f:
            if max_lines > -1:
                file_content = b''
                c =0
                for line in f:
                    file_content += line
                    c+=1
                    if c > max_lines:
                        break
            else:
                file_content = f.read()

    else:
        with io.open(fname_csv, 'rb') as f:
            if max_lines:
                file_content = b''
                #for line in f:
                    #print('l', type(line))
                #    break
                for line in f.readlines(max_lines):
                    #print ('l',type(line))
                    file_content += line
                    #print('l', type(file_content))
            else:
                file_content = f.read()

    #print (type(file_content))
    return file_content


def getContentFromWeb(url, max_lines=100):
    # save file to local directory

    if max_lines >- 1:
        with closing(requests.get(url)) as r:
            input = r.iter_lines(chunk_size=1024, delimiter=b"\n")
            c =0

            content = b''
            lines = []
            l=[]
            for line in input:
                content+=line
                lines.append(line)
                l.append(len(line))
                c +=1
                if c >= max_lines:
                    break
            #print ('LINES', len(lines), 'SUM', sum(l))
            content = b'\n'.join(lines)
            #print ("CC", len(content))
    else:
        content = requests.get(url).read()

    return content

def getContentAndHeader(fName=None, url=None, download_dir=None, max_lines=None):

    id= url if url else fName
    logger.debug("(%s) sniff content, max_lines:%s", id, max_lines)

    content = None
    header = None
    status_code = None
    exception=None

    if fName:
        if os.path.exists(fName):
            #process local file
            content = getContentFromDisk(fName, max_lines=max_lines)
            logger.debug("(%s) got content from disk %s", id, fName)
        else:
            logger.debug("(%s) file not found %s", id, fName)
    if content is None and url:
        try:
            # head lookup
            logger.debug("(%s) perform head lookup on %s", id, url)
            head = requests.head(url)
            status_code = head.status_code
            header = dict(head.headers)
            if not content:
                content = getContentFromWeb(url, max_lines=max_lines)
                logger.debug("(%s) got content from Web", url)
        except Exception as e:
            print (e)
            logger.warning("(%s) %s", id, e)
            logger.debug("(%s) %s", id, e, exc_info=True)

            exception = e
            status_code = 701

    return {'content':content,
            'header':header,
            'status_code':status_code,
            'exception':exception}
