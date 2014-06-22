#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__ = "GPL v3"
__author__ = "Yuta Hayashibe"

import codecs
import sys
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

MAX_BIG_CATEGORY_NUM = 7


CATEGORIES = {}
ID2MIDCATEGORY = {}
ID2CATEGORY = {}


def getCategories(big_category, iterator):
    line = it.next().lstrip().rstrip()
    middle_category = None
    while len(line) != 0:
        if line[0] == u'【':
            middle_category = line[1:-1]
        else:
            items = line.split()
            myid = int(items[0])
            myname = items[1]

            CATEGORIES[myid] = myname
            ID2MIDCATEGORY[myid] = middle_category
            ID2CATEGORY[myid] = big_category


        line = it.next().lstrip().rstrip()

import collections
LEAF_CATS = collections.defaultdict(list) #categoru => []
CONTENS = []
import re
REFPATTERN = re.compile(r'[0-9][0-9][0-9][0-9]\.?[0-9]*')
KAKKO_PATTERN = re.compile(r'\(.+?\)')
KAKKO_PATTERN2 = re.compile(r'\[.+?\]')
KAKKO_PATTERN3 = re.compile(u'【.+?】')


def getItems(line, it):
    num = line.split()[0]
    leaf_category = line.split()[1].split(u'［')[0]

    category = int(num.split(u'.')[0])
    detail_category = int(num.split(u'.')[1])
    tmp = u"%s\t%s" % (detail_category, leaf_category)
    LEAF_CATS[category].append(tmp)

    line = it.next().lstrip().rstrip()

    mode = None
    while len(line) != 0:
        if line.startswith(u'【'):
            items = line[1:].split(u'】')
            mode = items[0]
            #TODO do something for related information
        else:
            if mode is not None:
                #TODO do something for related information
                break
            else:
                line = REFPATTERN.sub(u'', line)
                line = KAKKO_PATTERN.sub(u'', line)
                line = KAKKO_PATTERN2.sub(u'', line)
                line = KAKKO_PATTERN3.sub(u'', line)
                for item in line.rstrip(u'；').split():
                    if item.startswith(u'〔'):
                        pass
                    elif item.startswith(u'→'):
                        pass
                    else:
                        tmp = u'%s\t%s\t%s\n' % (category, detail_category, item)
                        CONTENS.append(tmp)

        line = it.next().lstrip().rstrip()


def output(out_prefix):
    f = codecs.open(out_prefix + '.category.tsv', 'w', 'utf8')
    for myid in sorted(CATEGORIES.keys()):
        myname = CATEGORIES[myid]
        middle_category = ID2MIDCATEGORY[myid]
        big_category = ID2CATEGORY[myid]
        line =  u'%s\t%s\t%s\t%s' % (big_category, middle_category, myid, myname)

        for leaf in LEAF_CATS[myid]:
            f.write(line)
            f.write(u'\t%s' % leaf)
            f.write(u'\n')
    f.close()

    f = codecs.open(out_prefix + '.contents.tsv', 'w', 'utf8')
    f.write(u''.join(CONTENS))
    f.close()




import os.path
if __name__ == '__main__':
    fname =  sys.argv[1]
    out_prefix =  sys.argv[2]

#    for lid, line in enumerate(codecs.open(fname, 'r', 'utf8')):
#        print line


    it =codecs.open(fname, 'r', 'Shift_JIS')
    now_big_category_num = 0
    while True:
        try:
            line = it.next()
        except StopIteration:
            break

        if line.startswith(u"I") or line.startswith(u"V"):
            if now_big_category_num <= MAX_BIG_CATEGORY_NUM:
                now_big_category_num += 1
                getCategories(now_big_category_num, it)

        elif line.startswith(u'日本語索引'):
            break

        elif line.startswith(u"0") or  line.startswith(u"1"):
            if u'.' not in line: #ignore this block
                while len(line) != 0:
                    line = it.next().rstrip()
            else:
                getItems(line, it)
 
        else:
            pass
#        print line

    output(out_prefix)
   
