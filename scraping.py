# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# create a function to 
## Initialize the browser.
## Create a data dictionary.
## End the WebDriver and return the scraped data. 
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # set news title and paragraph variables:
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_images(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # set up the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    # return the title and paragraph
    return news_title, news_p

# ### Featured Images

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except (AttributeError):
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

def mars_facts():

    # Add try/except for error handling
    try:
        # use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        
    except BaseException:
        return None

    # assign columns to the new DataFrame 
    df.columns=['Description', 'Mars', 'Earth']

    # turn the Description column into the DataFrame's index
    df.set_index('Description', inplace=True)

    # conver the df to HTML format, add bootstrap
    return df.to_html()

def hemisphere_images(browser):

    # Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Add try/except for error handling
    try:
        
        # Write code to retrieve the image urls and titles for each hemisphere.
        # Find the relative image url
        descriptions = img_soup.find_all('div', class_='description')

    except BaseException:
        return None
        
        # Retrieve the urls to the websites of each hemisphere image
        # and use the base URL to create absolute URLs
    img_site_urls = []
    for description in descriptions:
        img_site = description.a['href'] 
        img_site_urls.append(f'https://marshemispheres.com/{img_site}')

    # loop through the websites contaning the full-resolution images,
    for img_site_url in img_site_urls:
        # create an empty dictionary to hold the image url and title
        hemispheres = {}
        # click the link
        browser.visit(img_site_url)
        # Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')
        # find the "Sample" image anchor tag, and get the "href"
        href = img_soup.find('li').a['href']
        # complete the absolute url and save it as the value for the 'img_url' key in the dictionary
        hemispheres['img_url'] = f'https://marshemispheres.com/{href}'
        # find the title of the image and save it as the value 
        # for the 'title' key in the dictionary
        hemispheres['title'] = img_soup.find('h2', class_ = 'title').text
        # add the dictionary to the list created in step 2
        hemisphere_image_urls.append(hemispheres)
        # navigate back to the beginning to get the next hemisphere image
        browser.back()        

    # Return the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
