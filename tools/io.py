import os
import gzip
import logging
import requests

def getContentFromDisk(fname_csv, max_lines=-1):
    if fname_csv[-3:] == '.gz':
        with gzip.open(fname_csv, 'rb') as f:
            if max_lines>-1:
                file_content = ''
                c =0
                for line in f:
                    file_content += line
                    c+=1
                    if c > max_lines:
                        break
            else:
                file_content = f.read()

    else:
        with open(fname_csv, 'rU') as f:
            if max_lines:
                file_content = ''
                for line in f.readlines(max_lines):
                    file_content += line
            else:
                file_content = f.read()

    return file_content


def getContentFromWeb(url, max_lines=100):
    # save file to local directory

    if max_lines >- 1:
        input = requests.get(url, stream=True).iter_lines()
        c =0

        content = ''
        lines = []
        for line in input:
            lines.append(line)
            c +=1
            if c > max_lines:
                break
        content = '\n'.join(lines)
    else:
        content = requests.get(url).read()

    return content

def getContentAndHeader(fName=None, url=None, download_dir=None, max_lines=None):
    logger = logging.getLogger(__name__)
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
    if url:
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
            logger.warning("(%s) %s", id, e)
            logger.debug("(%s) %s", id, e, exc_info=True)

            exception = e
            status_code = 701

    return {'content':content,
            'header':header,
            'status_code':status_code,
            'exception':exception}
        #, file_extension, status_code, local_file
