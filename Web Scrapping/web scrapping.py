import requests
import urllib.request
from bs4 import BeautifulSoup as bs
import re

url = 'https://web.archive.org/web/20171117230616/http://lanyrd.com/speakers/'
slide_url='https://web.archive.org/web/20171117230609/http://lanyrd.com/slides/'
response = requests.get(url)
slide_response = requests.get(slide_url)

soup = bs(response.content, 'html.parser')
slide = bs(slide_response.content, 'html.parser')
sld= slide.find_all('div',{'class':"coverage-item coverage-slides"})
all =soup.find_all("span",{"class":"name"})
img=soup.find_all("div",{"class":"avatar avatar-med"})
x=soup.find_all("div",{"avatar avatar-profile"})
for i in range(len(x)):
    img.append(x[i])
l=[]
for i in range(len(img)): 
    d={}
    k={}
    name=[]
    date=[]
    d['Speaker']=all[i].find("a").text
    d['Display Image url'] = img[i].find("img",attrs={"src" : re.compile("^https://")}).get("src").replace("\'","")
    
    pro_url= ('https://web.archive.org'+img[i].find('a',attrs={'href': re.compile("^/web")}).get('href'))
    d['Website']=pro_url
    profile =requests.get(pro_url)
    pro_soup=bs(profile.content,"html.parser")
    
    pro_video= pro_soup.find_all('h3',{"class":"title"})
    
    pro_title=pro_soup.find_all('div',{"class":"big-profile"})
    twitter=pro_soup.find_all('p',{"class":"twitter icon"})
    facebook=pro_soup.find_all('p',{"class":"facebook icon"})
    linkedin=pro_soup.find_all('p',{'class':"linkedin icon"})
    
    twitter1=pro_soup.find_all('span',{"class":"name"})
    
    event=pro_soup.find_all('li',{"class":"conference vevent interactive-listing"})
    try:
        d['Location']=(pro_title[0].find("p",{"class":"location"}).text).replace('\n','').replace("in",",")
        d['Title']=(pro_title[0].find("p",{"class":"tagline"}).text).replace('\n','').replace(" ","")   
    except:
        d['Location']=None
        d['Title']='Independent designer; GIF sommelier. Started that whole “responsive web design” thing. (@RWD) Has a bukk.it. ⭐️ &gt; ❤️.'
    
    try:
        sur= sld[i].find("p",{"class":"meta"}).text.replace('at',',').replace("\n","").replace("\t","").replace("from ","")
    except:
        sur=None
    
    try:
        surl =(sld[i].find("a",attrs={'rel': re.compile("^nofollow")}).get('href'))
    except:
        surl=None
    
    try:
        d['Linkedin'] =(linkedin[0].find("a",attrs={'rel': re.compile("^me")}).get('href'))
    except:
        d['Linkedin']=None
    try:    
        d['Twitter'] =(twitter[0].find("a",attrs={'rel': re.compile("^me")}).get('href'))
    except:
        try:
            d['Twitter']=(twitter1[0].find("a",attrs={'rel': re.compile("^me")}).get('href'))
        except:
            d['Twitter']=None
    try:    
        d['Facebook'] =(facebook[0].find("a",attrs={'rel': re.compile("^me")}).get('href'))
    except:
        d['Facebook']=None
        
    for j in range(len(event)):
        try:
            name.append(event[j].find("a",{"class":"summary url"}).text)
            name.append(event[j].find("p",{"class":"date"}).text)
            name.append(event[j].find("p",{"class":"location"}).text.replace('\t','').replace('\n',' '))
        except:
            name.append('None')
    date.append(name)
    k['Name','City,Country','Date']=date
    d['Attended Event']=k
    d['Slide Decks']= sur +", "+ surl 
    
    try:
        video_url= ('https://web.archive.org'+pro_video[0].find('a',attrs={'href': re.compile("^/web")}).get('href'))
    except:
        None
      
    Vid =requests.get(video_url)
    video_soup=bs(Vid.content,"html.parser")
    video=video_soup.find_all('div',{"class":"coverage-item coverage-video"})
    video1=video_soup.find_all('p',{"class":"meta"})
    loc=[]
    dat=[]
    v={}
    for om in range(len(video)):
        try:
            loc.append(video[om].find("a",attrs={'rel':re.compile("^nofollow")}).text)
            loc.append(video[om].find("a",attrs={'rel':re.compile("^nofollow")}).get('href'))
            loc.append(video1[om].find("a",attrs={'href':re.compile("^/web")}).text)
            loc.append(video1[om].find("a",attrs={'href':re.compile("^/http")}).text.replace('\t','').replace('\n',' '))
        except:
            None
    dat.append(loc)
    v['Title','Url','Event Name',]=dat
    d['All Videos']=v
    l.append(d)
import pandas as pd
df=pd.DataFrame(l)
df =df[['Speaker','Display Image url','Title','Location','Attended Event','All Videos','Slide Decks','Linkedin','Twitter','Facebook','Website']]
df= df.set_index('Speaker')
df.to_csv(r"C:\Users\YuSuf AnSari\Desktop\Web Scrapping\Speaker Details.csv")
df
df_new = pd.read_csv(r'C:\Users\YuSuf AnSari\Desktop\Web Scrapping\Speaker Details.csv')
writer = pd.ExcelWriter(r'C:\Users\YuSuf AnSari\Desktop\Web Scrapping\Speaker Details In excel.xlsx')
df_new.to_excel(writer,index=False)
writer.save()
