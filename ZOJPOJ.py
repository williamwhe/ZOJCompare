# -*- coding: utf-8 -*-
'''
Created on 2012-2-12

@author: William He
'''

import sys, httplib, traceback, re

reload(sys)
sys.setdefaultencoding('utf8')

class Downloader:    
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

zoj_host = "acm.zju.edu.cn"
zoj_path = "/onlinejudge/showProblems.do?contestId=1&pageNumber="
zoj_max = 26
zoj_problems = {}

poj_host = "poj.org"
poj_path = "/problemlist?volume="
poj_max = 31
poj_problems = {}

common_titles = set([])

class problem:
    def __init__(self):
        self.title = ""
        self.zoj_id = ""
        self.zoj_ac = ""
        self.zoj_rate = ""
        self.poj_id = ""
        self.poj_ac = ""
        self.poj_rate = ""
        
    def toString(self):
        print "zoj_id:", self.zoj_id, ", poj_id:", self.poj_id, ", title:", self.title, ", zoj_ac:", self.zoj_ac, ", zoj_rate:", self.zoj_rate, ", poj_ac:", self.poj_ac, ", poj_rate:", self.poj_rate

if __name__ == '__main__':
    matched = []
    dl = Downloader()
    
    zoj_total = 0
    zoj_pattern = re.compile(r"<td\sclass=\"problemId\">.*?<font\scolor=\"blue\">(\d{4})</font>.*?<td\sclass=\"problemTitle\">.*?<font\scolor=\"blue\">(.*?)</font>.*?<td\sclass=\"problemStatus\">(.*?%)\s*\((<a\shref='.*?'>(\d+)</a>|0)/", re.U|re.M|re.S)
    for pageid in range(1, zoj_max + 1):
        status, content = dl.fetch_content(zoj_host, zoj_path + str(pageid))
        if status == 200:
            zoj_matches = zoj_pattern.findall(content)
            if zoj_matches:
                for zoj_match in zoj_matches:
                    pro = problem()
                    pro.title = zoj_match[1]
                    pro.zoj_id = zoj_match[0]
                    pro.zoj_rate = zoj_match[2]
                    if zoj_match[4] != '':
                        pro.zoj_ac = zoj_match[4]
                    common_titles.add(zoj_match[1])
                    zoj_problems[zoj_match[1]] = pro
                zoj_total += len(zoj_matches)
                print len(zoj_problems), "/", zoj_total
   
    poj_pattern = re.compile(r"<tr\salign=center><td>(\d{4})</td><td\salign=left><a\slang=\"en-US\".*?>(.*?)</a></td><td>(\d+%)\(<a\shref=.*?>(\d+)</a>/", re.U|re.M|re.S)
    for pageid in range(1, 2):
        status, content = dl.fetch_content(poj_host, poj_path + str(pageid))
        if status == 200:
            poj_matches = poj_pattern.findall(content)
            if poj_matches:
                for poj_match in poj_matches:
                    if poj_match[1] in common_titles:
                        pro = zoj_problems[poj_match[1]]
                        if pro is None:
                            print "Miss ZOJ Problems:", poj_match[1]
                            continue
                        pro.poj_id = poj_match[0]
                        pro.poj_rate = poj_match[2]
                        pro.poj_ac = poj_match[3]
                        matched.append(pro)
                        print len(matched)
                        
    for match in matched:
        match.toString()