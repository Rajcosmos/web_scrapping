
    # Scraping script in Python for Mission to Mars

    ## Initialization of dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
## Importing time to add sleep for browser slow response or else it errors out
import time
 ## For regular expression required in capturing tweets
import re

def init_browser():
    executable_path = {'executable_path':'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scraping():
    print("test")

    listings={}
    url='https://mars.nasa.gov/news/'
    html=requests.get(url)
    soup= bs(html.text,'html.parser')

    #  NASA Mars News ****************************************************
    #print("*************Starting Nasa Mars News")
    news_title=soup.title.text
    news_p=soup.find('p').text
    
   # print("news_title=", news_title)
   # print("news_p=" ,news_p)

    # JPL Mars Space Images = Featured Image *********************************
   # print("**************Starting JPL Mars Space Images")
    
    browser = init_browser()

    url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(2)

    html=browser.html
    soup= bs(html,'html.parser')
    soup.title.text
    soup.find_all('div',class_='carousel_items')
    soup.find_all('a', class_="button fancybox")
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)

    html = browser.html
    soup = bs(html, 'html.parser')

    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = bs(html, 'html.parser')
    soup.find_all('figure',class_="lede")

    x=0
    for i in soup.find_all('a',limit=60):
        x+=1
        if x==59:
            y=i['href']

    ### Capturing featured image*
    url = 'https://www.jpl.nasa.gov'
    featured_image_url = url + y
    #print("featured_image_url=",featured_image_url)
    browser.quit()



    ## MARS WEATHER ************************************
   # print("**********Starting Mars Weather")
    
    browser = init_browser()

    url='https://twitter.com/marswxreport?lang=en'

    browser.visit(url)
    html=browser.html
    soup= bs(html,'html.parser')

    tweets=soup.find_all('p',class_='tweet-text')
    for tweet in tweets:
        if tweet.find(text=re.compile('daylight')):
            
            ## Assigning mars_weather variable
            mars_weather=tweet.find(text=re.compile('daylight'))
            break

    print("mars_weather=" ,mars_weather)
    browser.quit()


    ## Mars Facts**************************************************
   # print("************ Collecting Mars facts and saving in html")
    url='https://space-facts.com/mars/'
    tables=pd.read_html(url)

    df=tables[0]
    df.columns=['Facts','Values']
    
    # ***Converting to HTML***
    html_table=df.to_html()
    html_table.replace('\n','')

    #** Saving to html file
   # print("** saving df to mars_facts.html file***")
    df.to_html('mars_facts.html')
    soup=bs(open("mars_facts.html"),"html.parser")
    ## Stripping the soup data and saving in mars_facts disctionary, mars_info is a temperory list used
    mars_info=[]
    mars_facts={}
    for z in soup.table('td'):
        #print(z.text)
        mars_info.append(z.text.strip(':'))
    mars_facts=dict([(k, v) for k,v in zip (mars_info[::2], mars_info[1::2])])
    print(mars_facts)
    ## Mars Hemisperes *****************************************
   # print("*************Starting Mars Hemisphere")

    browser = init_browser()
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)
    html=browser.html
    soup= bs(html,'html.parser')

    soup.find_all('h3')

    ### Key to cracking this problem was use below code
    ###link_text = soup.find(class_="description").find('h3').get_text()
    ###browser.click_link_by_partial_text(link_text)
    ### Thank Dylan for helping me to crack it....
    ### Then I tested it with below to get the link from next page
    ### browser.find_link_by_partial_href('download')['href']


    hemisphere_image_urls=[]
    temp_dict={'title':[],'img_url':[]}
    capture_text=soup.find_all('h3')
    title=[]
    img=[]
    for i in capture_text:
        y=i.get_text()
        val1=y.strip('Enhanced')
        browser.click_link_by_partial_text(y)
        val2=browser.find_link_by_partial_href('download')['href']
        ## Assigning to dictionary
        temp_dict={'title':val1,'img_url':val2}
        hemisphere_image_urls.append(temp_dict)
        ## Assigning to lists for html presentation purpose
        title.append(val1)
        img.append(val2)
        browser.visit(url)
    browser.quit()

    #print("hemisphere_image_urls=", hemisphere_image_urls)

    listings['news_title']=news_title
    listings['news_p']=news_p
    listings['featured_image_url']=featured_image_url
    listings['mars_weather']=mars_weather
    listings['mars_facts']=mars_facts
    #listings['hemisphere_image_urls']=hemisphere_image_urls
    listings['title1']=title[0]
    listings['title2']=title[1]
    listings['title3']=title[2]
    listings['title4']=title[3]
    listings['imgurl1']=img[0]
    listings['imgurl2']=img[1]
    listings['imgurl3']=img[2]
    listings['imgurl4']=img[3]
    
    print(listings)
    return listings

#scraping()