from tkinter import *
from tkinter import ttk

from time import sleep

import requests as req
from bs4 import BeautifulSoup as beau
import genanki as gnk


# 視窗
def win_set(title):
    win.title(title)
    win.geometry('400x100')
    win.resizable(0,0)
    win.config(bg="#323232")
    win.attributes("-alpha",0.8)

# 標籤
def lbl_set(lbl):
    lbl.pack(side=TOP)
    lbl.config(bg="#323232")

# 按鈕 command
url = ''
def termiwin():
    global url 
    url = enter.get()
    sleep(0.5)
    win.destroy() 

#Programs to open a window to get the url

global win
win = Tk()
win_set("hackmd web page to user's anki")
lbl = Label(win,fg= 'white',text="Enter the URL:", font = ("Tahoma", 15))
lbl_set(lbl)

# 輸入框
enter =  Entry(win)
enter.config(bg="grey")
enter.pack()

# 按鈕
btn = Button(text = 'download',font = ("Tahoma", 10),command = termiwin)
btn.pack(padx=20, pady=10)

win.mainloop() # 視窗常開

# Program ends to open a window to get the url


# Program to process the text which we get from the web

text1 = "start to download...."
text2 = 'complete download...'
text3 = 'start to process'
text4 = 'complete process'
text5 = 'start tp transit'
text6 = 'complete transit'
text7 = 'working tree clean'



# 開一個status視窗 想隨進度更新 失敗
win = Tk()
win_set('status')

web = req.get(url)
soup = beau(web.text,"html.parser")
get_web = soup.find("div",class_ = "markdown-body container-fluid")
for i in get_web:
    element = i

# 標題提取
title = ""
status = 0 #1 read , 0 quick
for char in element:
    if(char == '\n'):
        break
    if(status == 1):
        title = title + char
    if (char == '#'):
        status = 1
title = title.strip()

# 解釋提取
mean = ""
meanstatus = 0
meanlist_sub = ''
meanlist =[]
def meanex():
    global mean 
    global meanstatus 
    global meanlist_sub
    global meanlist 
    if(char == '\n' and mean != ''):
        meanstatus = 0
        meanlist_sub = meanlist_sub.lstrip() + mean.strip() +'<br>' # anki讀的是html
        mean = ''
    elif(char =='-' and len(meanlist_sub) != 0):
        meanlist.append(meanlist_sub)
        meanlist_sub = ''
    elif(char =='>'):
        meanstatus = 1
    elif(meanstatus == 1):
        mean = mean + char

# 單字提取
word = ""
wordstatus = 0
wordlist =[]
def wordex():
    global word 
    global wordstatus 
    global wordlist 
    if(char == '\n' and word != ""):
        wordstatus = 0
        wordlist.append(word.strip())
        word = ""
    elif(char == '-'):  
        wordstatus = 1
    elif(wordstatus == 1):
        word = word + char

# 例外處理 (最後一個)
def spemean():
    global mean 
    global meanstatus 
    global meanlist_sub
    global meanlist 
    meanlist_sub = meanlist_sub + mean.strip()
    mean = ''
    meanlist.append(meanlist_sub)
    meanlist_sub = ''

#每一行分別取完 .strip()後 在append
for char in element :
    wordex()
    meanex()
spemean()

# Program ends to process the text which we get from the web

# Program to send the processed text to anki
# anki model 樣式設定
my_model = gnk.Model(
  1091735104,'基本型',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',          
      'afmt': '{{Question}}<hr id="answer">{{Answer}}',
    }],
    css = '.card {font-family: arial;font-size: 20px;text-align: center;color: black;background-color: white;}')

# 排組設定
my_deck = gnk.Deck(2059400110,title)

# note 新增卡片
# 不會新增重複的
# 不同次新增 相同的Question 不會覆蓋 會多一個出來
# 同一次新增 相同的Question 以最新的為主
for (a,b) in zip(wordlist,meanlist):
    my_note = gnk.Note(model = my_model,
        fields = [a,b])
    my_deck.add_note(my_note)

my_package = gnk.Package(my_deck)
my_package.write_to_file("anki_voc.apkg")

lbl = Label(win,fg= 'white',text="Done", font = ("Tahoma", 15))
lbl_set(lbl)

win.mainloop()