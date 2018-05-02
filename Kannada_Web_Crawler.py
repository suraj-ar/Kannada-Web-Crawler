# -*- coding: utf-8 -*-
from Tkinter import *
from aylienapiclient import textapi
from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib2, sys
import sqlite3

client = textapi.Client("7f309fef", " 28a1abb3d1536845ca01e8096a2d35b7")
db = sqlite3.connect("selfstudy8.sqlite")
db.execute("CREATE TABLE articles(name NVARCHAR(100),content NCLOB)")

option_values = []

arr_vk_links=[]
arr_kd_links=[]

arr_vk_titles = []
arr_kd_titles = []

vk="ವಿಜಯ ಕರ್ನಾಟಕ"
kd="ಕನ್ನಡ ದುನಿಯಾ"



def do_stuff():  #defining function to be performed by button
 for item in option_values:
     print item
 option_values[:] = []
    
 
def option_func_1(value):
    option_values.append(value.decode('utf8'))

def get_keyword(key):
    print key
    print option_values[0]
    if option_values[0] == "ವಿಜಯ ಕರ್ನಾಟಕ" :
        show_articles_vk()
    elif option_values[0] == "ಕನ್ನಡ ದುನಿಯಾ" :
        show_articles_kd()
        



def articles_window(keyword):

    articles = Tk()
    articles.title("list of articles")
    
    def show_articles_vk():
        url = "https://vijaykarnataka.indiatimes.com/topics/"
        s = keyword
        url+= s.encode('utf8')
        #print url
        #print keyword
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(url,headers=hdr)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page)  

        containers = soup.find_all("div")
        containers = soup.find_all('div',{"class":"content"})
        for i in range(0,14):
            link = soup.find_all('div',{"class":"content"})[i].find('a')["href"]
            text =  soup.find_all('div',{"class":"content"})[i].find('span').string
            arr_vk_links.append("https://vijaykarnataka.indiatimes.com"+link)
            arr_vk_titles.append(text)
        
        


        for x in range(len(arr_vk_titles)):
            q = Label(articles, text=x, textvariable=x)
            w = Label(articles, text=arr_vk_titles[x], textvariable=arr_vk_titles[x])
        #r = Label(app2)
        
            q.grid(column=0, row=x)
            w.grid(column=1, row=x)

    def show_articles_kd():
        url2 = "http://kannadadunia.com/?s="
        s2 = keyword
        url2+= s2.encode('utf8')
        
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(url2,headers=hdr)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page)


        containers2 = soup.find_all('div',{"class":"small-12 medium-12 large-12 columns postlist"})
        print len(containers2)
        for i in range(0,len(containers2)):
            link = soup.find_all('div',{"class":"small-12 medium-12 large-12 columns postlist"})[i].find('a')["href"]
            text =  soup.find_all('div',{"class":"small-12 medium-12 large-12 columns postlist"})[i].find('a').string
            arr_kd_links.append(link)
            arr_kd_titles.append(text)
            


        
        for x in range(len(arr_kd_titles)):
            q = Label(articles, text=x, textvariable=x)
            w = Label(articles, text=arr_kd_titles[x], textvariable=arr_kd_titles[x])
        #r = Label(app2)
        
            q.grid(column=0, row=x)
            w.grid(column=1, row=x)

    

    

    
    if option_values[0] == vk.decode('utf8'):
        show_articles_vk()
    elif option_values[0] == kd.decode('utf8') :
        show_articles_kd()
    

    button1 = Button(articles, text="proceed", width=20,command= extraction)
    button1.grid(column=3,padx=15,pady=15)

    
#    k=keyword


    






def extraction():

    extract = Tk()
    Label(extract, text="Article Number").grid(row=0, column=0)
    e1 = Entry(extract)
    e1.grid(row=0, column=1)

    



    def article_extraction_vk():
        art_nums=e1.get()
        list_comma=art_nums.split(",")
        list_of_articles=list(map(int, list_comma))
        for i in list_of_articles:
            url = arr_vk_links[i]
            extract = client.Extract({"url": url, "best_image": True})
            
            db.execute("INSERT INTO articles(name,content) VALUES(?,?)",(extract["title"],extract["article"]))
            cursor = db.cursor()
            cursor.execute("SELECT *  FROM articles")
            for name,matter in cursor:
                res_1 = name
                res_2 = matter

            print res_1
            print "------------------"
            print res_2


    def article_extraction_kd():
        art_nums=e1.get()
        list_comma=art_nums.split(",")
        list_of_articles=list(map(int, list_comma))
        for i in list_of_articles:
            url= arr_kd_links[i]
            extract = client.Extract({"url": url, "best_image": True})
            db.execute("INSERT INTO articles(name,content) VALUES(?,?)",(extract["title"],extract["article"]))
            cursor = db.cursor()
            cursor.execute("SELECT *  FROM articles")
            for name,matter in cursor:
                res_1 = name
                res_2 = matter

            print res_1
            print "------------------"
            print res_2
            

    if option_values[0] == vk.decode('utf8'):
        button2=Button(extract, text='Get Article', command=article_extraction_vk)
        button2.grid(row=0,column=3)
    elif option_values[0] == kd.decode('utf8') :
        button2=Button(extract, text='Get Article', command=article_extraction_kd)
        button2.grid(row=0,column=3)

    










master = Tk()           #Creating window

variable1 = StringVar(master)   #Setting up drop downs






#button = Button(master,text = "Enter",command = do_stuff) #Creating Enter button
#button = Button(master, text="get articles", width=20,command= lambda: get_keyword(e1.get()))
button = Button(master, text="get articles", width=20,command= lambda: articles_window(e1.get()))

label_source = Label(master,text = "Enter paper")   #Creating labels for drop downs

w1 = OptionMenu(master, variable1, "ವಿಜಯ ಕರ್ನಾಟಕ","ಕನ್ನಡ ದುನಿಯಾ",command = option_func_1) #Adding options to drop downs
Label(master, text="Keyword in Kannada").grid(row=1)
e1 = Entry(master)
e1.grid(row=1, column=1)

label_source.grid(row= 0,column =0)
w1.grid(row= 0,column =1)                   #Placing corresponding label and Dropdown

button.grid(row = 4,column = 1)
mainloop()


