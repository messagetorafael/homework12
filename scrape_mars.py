#####################################################################################
# Student: Rafael Santos
# Data and Visualisation Bootcamp - Cohort 3
# Homework 12
#####################################################################################

# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "c:/chromedrv/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    ### NASA Mars News
    
    # Visit URL
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Get the resuts for searched data
    results = soup.find_all('li', class_="slide")

    # Loop through returned results
    for result in results:
        # Error handling
        try:
            # Identify and return title
            news_title = result.find('div', class_="content_title").a.text

            # Identify and return paragraph
            news_paragraph = result.find('div', class_="rollover_description_inner").text
                
            # Print results only if title and paragraph are available
            if (news_title and news_paragraph):
                print('-------------')
                print(f'{news_title}')
                print(f'{news_paragraph}')
                
        except AttributeError as e:
            print(e)


    ### JPL Mars Space Images - Featured Image
    
    # Visit URL - 1st page
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Get the resuts for searched data
    for result in results:
        # Error handling
        try:
            featured_image_url = result.a['data-link']

        # Print results only if not empty
            if (featured_image_url):
                print('-------------')
                print(f'{featured_image_url}')

        except AttributeError as e:
            print(e)
        
        except KeyError as bug:
            print(bug)


    # Visit URL - 2nd page
    url="https://www.jpl.nasa.gov" + featured_image_url
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Get the resuts for searched data
    results = soup.find_all("figure",class_="lede")

    for result in results:
        # Error handling
        try:
            # Identify and return title of listing
            featured_image_url = result.a['href']
            # Print results only if available
            if (featured_image_url):
                print('-------------')
                print(f'{featured_image_url}')

        except AttributeError as e:
            print(e)
        
        except KeyError as bug:
            print(bug)
        
    featured_image_url ="https://www.jpl.nasa.gov" + featured_image_url

    print(featured_image_url)

    ### Mars Weather
    
    # Visit URL
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Get the resuts for searched data
    results = soup.find_all(class_="js-tweet-text-container")
    mars_weather = results[0].p.text
    print(mars_weather)
    
    
    ### Mars Facts
    
    # Visit URL
    url = 'http://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    

    # Use pandas to read tables on the page and get data
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Mars Planet Profile', 'Values']
    df.set_index("Mars Planet Profile", inplace=True)
    html_table = df.to_html()


    ### Mars Hemispheres
    
    # Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    # Get the results for searched data, 1st layer/page
    hemispheres = soup.find_all(class_='itemLink product-item')

    ##pre-define variables used in the loop to review the data
    base_url="https://astrogeology.usgs.gov"
    title_url_dic ={}
    hemisphere_image_urls=[]

    for hemisphere in hemispheres:
        # Error handling
        try:
            # Identify and return the title of listing
            image_url1 = hemisphere['href']
            title = hemisphere.text
                    
            ## Print results only if available
            if (image_url1 and hemisphere.text != ''):
                
                print('-------------')
                print(f'{title}')
                print(f'{image_url1}')
                print(base_url + str(image_url1))
                
                # Visit URL - 2nd page where image is available
                url = base_url + image_url1
                browser.visit(url)
                time.sleep(1)

                # Scrape page into Soup
                html = browser.html
                soup = BeautifulSoup(html, "html.parser")
                
                # Get the results for searched data, 2nd layer/page
                image_url = soup.find_all(target='_blank')
                image_url = image_url[0]['href']
                   
                print(f'{image_url}')

        
                title_url_dic = {'title':title,'img_url':image_url}
                hemisphere_image_urls.append(title_url_dic)    
            
            
        except AttributeError as e:
            print(e)
        
        except KeyError as bug:
            print(bug)

            
    print('This is the dictionary')
    print(hemisphere_image_urls)

    
    # Store data in a dictionary
    mars_data = {

        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "html_table": html_table,
        "hemisphere_image_urls":hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
