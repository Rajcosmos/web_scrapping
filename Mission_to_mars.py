
# coding: utf-8

# # Step#1 - Scrapping

# In[3]:


from bs4 import BeautifulSoup as bs
import requests


# In[68]:


url='https://mars.nasa.gov/news/'


# In[69]:


html=requests.get(url)


# In[70]:


print(html)


# In[71]:


soup= bs(html.text,'html.parser')


# # NASA Mars News

# In[72]:


news_title=soup.title.text


# In[84]:


news_p=soup.find('p').text


# In[82]:


print(news_title)


# In[85]:


print(news_p)


# # JPL Mars Space Images = Featured Image

# In[983]:


get_ipython().system('pip install splinter ')


# In[984]:


from splinter import Browser


# In[986]:


executable_path = {'executable_path':'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[987]:


url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[988]:


html=browser.html
soup= bs(html,'html.parser')


# In[989]:


soup.title.text


# In[990]:


#soup.body


# In[991]:


soup.find_all('div',class_='carousel_items')


# In[992]:


soup.find_all('a', class_="button fancybox")


# In[993]:


browser.click_link_by_partial_text('FULL IMAGE')


# In[994]:


html = browser.html
soup = bs(html, 'html.parser')


# In[995]:


browser.click_link_by_partial_text('more info')


# In[996]:


html = browser.html
soup = bs(html, 'html.parser')
soup.find_all('figure',class_="lede")


# In[997]:


x=0
for i in soup.find_all('a',limit=60):
    x+=1
    if x==59:
        y=i['href']
     
        


# In[998]:


url = 'https://www.jpl.nasa.gov'
featured_image_url = url + y


# ##Assigning featured_image_url variable

# In[999]:


featured_image_url


# # MARS WEATHER 

# In[60]:


from bs4 import BeautifulSoup as bs
from splinter import Browser


# In[61]:


executable_path = {'executable_path':'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[62]:


url='https://twitter.com/marswxreport?lang=en'


# In[63]:


browser.visit(url)
html=browser.html
soup= bs(html,'html.parser')


# In[64]:


import re
tweets=soup.find_all('p',class_='tweet-text')
for tweet in tweets:
    if tweet.find(text=re.compile('daylight')):
        mars_weather=tweet.find(text=re.compile('daylight'))
        break


# In[65]:


mars_weather


# In[66]:


browser.quit()


# # Mars Facts

# In[1010]:


import pandas as pd


# In[1011]:


url='https://space-facts.com/mars/'


# In[1012]:


tables=pd.read_html(url)


# In[1013]:


tables


# In[1014]:


type(tables)


# In[1015]:


tables[0]


# In[1016]:


df =tables[0]


# In[1017]:


df.columns=['Facts','Values']


# In[1018]:


df


# ***Converting to HTML***

# In[1019]:


html_table=df.to_html()


# In[1020]:


html_table


# In[1021]:


html_table.replace('\n','')


# In[1022]:


df.to_html('mars_facts.html')


# In[8]:


soup= bs(open("mars_facts.html"),"html.parser")


# In[65]:


## Stripping the soup data and saving in dictionary
mars_info=[]
mars_facts={}
for z in soup.table('td'):
    #print(z.text)
    mars_info.append(z.text.strip(':'))
#mars_info
mars_facts=dict([(k, v) for k,v in zip (mars_info[::2], mars_info[1::2])])
mars_facts


# In[52]:


#!open mars_facts.html


# # Mars Hemisperes

# In[1024]:


from bs4 import BeautifulSoup as bs
from splinter import Browser


# In[1032]:


executable_path = {'executable_path':'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[1033]:


url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


# In[1034]:


browser.visit(url)
html=browser.html
soup= bs(html,'html.parser')


# In[1035]:


soup.find_all('h3')


# In[1036]:


### Key to cracking this problem was use below code
###link_text = soup.find(class_="description").find('h3').get_text()
###browser.click_link_by_partial_text(link_text)
### Thank Dylan for helping me to crack it....
### Then I tested it with below to get the link from next page
### browser.find_link_by_partial_href('download')['href']


# In[1037]:


hemisphere_image_urls=[]
temp_dict={'title':[],'img_url':[]}
capture_text=soup.find_all('h3')
for i in capture_text:
    y=i.get_text()
    val1=y.strip('Enhanced')
    browser.click_link_by_partial_text(y)
    val2=browser.find_link_by_partial_href('download')['href']
    temp_dict={'title':val1,'img_url':val2}
    hemisphere_image_urls.append(temp_dict)
    #img_url.append(browser.find_link_by_partial_href('download')['href'])
    browser.visit(url)


# In[1038]:


hemisphere_image_urls


# In[1039]:


browser.quit()

