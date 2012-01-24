# -*- coding: utf-8 -*-
'''
Created on 2012-1-20

@author: William He
'''

import sys, httplib, traceback, re

reload(sys)
sys.setdefaultencoding('utf8')

class Downloader:
    def getSubContent(self, content, starttag, endtag):
        startpos = content.find(starttag)
        if startpos == -1:
            return None
        endpos = content.find(endtag, startpos)
        if endpos == -1:
            return None
        return content[startpos:endpos]
    
    def decodeString(self, data):
        try:
            data = unicode(data, 'utf-8')
        except:
            try:
                data = unicode(data, 'gbk')
            except:
                traceback.print_exc(file=sys.stdout)
        return data

    def fetch_content(self, host, url):
        try:
            conn = httplib.HTTPConnection(host)
            conn.request("GET", url)
            res = conn.getresponse()
            status = res.status
            data = res.read()
            data = self.decodeString(data)
            conn.close()
            return status, data
        except:
            traceback.print_exc(file=sys.stdout)
            return 0, None

host = "acm.zju.edu.cn"
path = "/onlinejudge/showUserStatus.do?userId="
myuserid = "5272"
myac = set([])
otherac = set([])

if __name__ == '__main__':
    dl = Downloader()
    status, content = dl.fetch_content(host, path + myuserid)
    if status == 200:
        content = dl.getSubContent(content, "Solved", "</blockquote>")
        pattern = re.compile(r'(\d{4})')
        match = pattern.findall(content)
        for one in match:
            myac.add(int(one))
        print "MY ACs:", len(myac)
        otheruserid = sys.argv[1]
        status, content = dl.fetch_content(host, path + otheruserid)
        if status == 200:
            content = dl.getSubContent(content, "Solved", "</blockquote>")
            pattern = re.compile(r'(\d{4})')
            match = pattern.findall(content)
            for one in match:
                otherac.add(int(one))
            otherac = list(otherac)
            otherac.sort()
            print "Other ACs:", len(otherac)
            diff = 0
            for one in otherac:
                if one not in myac:
                    print one,
                    diff += 1
            print
            print "Diff:", diff