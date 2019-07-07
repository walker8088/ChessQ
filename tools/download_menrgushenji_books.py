#coding:utf-8
import sys
import re
import requests
import json

from tinydb import TinyDB, where

sys.path.append("..\\")

from cchess import *

from bs4 import BeautifulSoup

url_base = 'http://www.dpxq.com/hldcg/share/chess_%E8%B1%A1%E6%A3%8B%E8%B0%B1%E5%A4%A7%E5%85%A8/%E8%B1%A1%E6%A3%8B%E8%B0%B1%E5%A4%A7%E5%85%A8-%E5%8F%A4%E8%B0%B1%E6%AE%8B%E5%B1%80/%E6%A2%A6%E5%85%A5%E7%A5%9E%E6%9C%BA/%E6%A2%A6%E5%85%A5%E7%A5%9E%E6%9C%BA/'

books = []

def open_url(url) :
        req = requests.get(url)
        if req.status_code != 200 :
                return None
        return req.content

def parse_books(html) :        
        books = []
        soup = BeautifulSoup(html)
        for td in soup.find_all('td') :
                if td.a == None or len(td.a.text) == 0: 
                        continue
                title = unicode(td.a.text)
                if title.encode('utf-8')[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        #print title, td.a['href'] 
                        books.append([title,  td.a['href']] )
        return books
        
def str_between(src, begin_str, end_str) :
        first = src.find(begin_str) + len(begin_str)
        last = src.find(end_str)
        if (first != -1) and (last != -1) :
                return src[first:last]
        else :
                return None
            
def parse_one_book(html) :  
        result_map = {u"红胜": "1-0",  u"红负": "0-1",  u"黑胜": "0-1",  u"红和": "1/2-1/2",  u"和棋": "1/2-1/2",'default' : '*'}      
        result_dict = {}
        soup = BeautifulSoup(html)
        divs = soup.find_all('div')
        text = unicode(divs[1].text).encode('utf-8')
        
        result_dict['event'] = str_between(text, '[DhtmlXQ_event]', '[/DhtmlXQ_event]')
        if result_dict['event'] :
                result_dict['event'] = result_dict['event'].decode('utf-8')
        
        result_dict['title'] = str_between(text, '[DhtmlXQ_title]', '[/DhtmlXQ_title]')
        if result_dict['title'] :
                result_dict['title'] = result_dict['title'].decode('utf-8')[3:7]
        
        game_result = str_between(text, '[DhtmlXQ_result]', '[/DhtmlXQ_result]')
        if game_result :
                game_result = game_result.decode('utf-8')
                if game_result in result_map :
                        result_dict['result'] =  result_map[game_result]
                else :
                        result_dict['result'] =  result_map['default']
                        
        result_dict['binit'] = str_between(text, '[DhtmlXQ_binit]', '[/DhtmlXQ_binit]')
        
        tds = soup.find_all('td')
        text = unicode(tds[4].text) .encode('utf-8')
        result_dict['bmoves'] = str_between(text, '[DhtmlXQ_movelist]', '[/DhtmlXQ_movelist]')
                
        return result_dict
        
        
html =  open_url(url_base+"1.html")
if html == None :
        sys.exit(-1)
books1 =  parse_books(html.decode("GB2312"))       

html =  open_url(url_base+"2.html")
if html == None :
        sys.exit(-1)
books2 =  parse_books(html.decode("GB2312"))       

books = books1 +books2

books.sort(key=lambda x: x[0])

db = TinyDB('mengrushenji.jdb')
 
for it in books[:] :
        
        html = open_url("http://www.dpxq.com" + it[1])
        if html == None :    
                print "got None"
                continue
        book = parse_one_book(html)
        #print book['event'], book['title'], book ['result'], book ['binit'], book['bmoves']
        loader = PlainLoader()
        book = loader.load_from(book)
        print book['title'],
        #del book['result']
        #print book['fen_str']
        #print book["moves"]        
        del book['event']
        del book['binit']
        del book["bmoves"]
        del book["moves_zh"]
        #book['index'] = index
        if book['result'] == '*' :
                print "unknown result "
                break
        #print json.dumps(book)
        result = db.search( where("fen") == book['fen'])
        if len(result) == 0:
                db.insert(book)
                print "new data"
        elif  len(result) == 1  and len(book['moves']) > 0 :
                old_book = result[0]
                if book['moves'][0] in old_book["moves"] :
                        print "old data"
                        continue
                old_book["moves"].extend(book['moves'])
                print "append moves"
                db.update( { 'moves' : old_book['moves'] }, eids = [old_book.eid] )          
        elif len(result) > 1:
                print "error"
                print  result
                break
                
db.close()
