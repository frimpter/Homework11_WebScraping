# HW 11 - Web Scraping - Mission to Mars

from bs4 import BeautifulSoup as bs
import requests
import os
from splinter import Browser
import pandas as pd


def scrape():

    mars = {}

    ##################
    # NASA Mars News #
    ##################

    nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    nasa_html = requests.get(nasa_url)
    nasa_news = bs(nasa_html.text, 'html.parser')

    try:
        title = nasa_news.find('div', class_="content_title").text
        para = nasa_news.find("div", class_="article_teaser_body")
        #news_title = title.text
        #news_para = para.text
        if title:
            mars["news_title"] = title
        if para:
            mars["news_para"] = para

    except AttributeError as e:
        print(e)


    ##########################################
    # JPL Mars Space Images - Featured Image #
    ##########################################

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(jpl_url)

    jpl_html = browser.html
    jpl_images = bs(jpl_html, 'html.parser')

    browser.click_link_by_partial_text(
        'FULL IMAGE')  # Go to the FULL IMAGE page

    # Locate the relevant html code
    latest_image = jpl_images.find('a', class_="button fancybox")

    # Pull the URL for the full image
    full_image = latest_image['data-fancybox-href']
    # Returns a snippet, eg: /spaceimages/images/mediumsize/PIA17900_ip.jpg

    jpl_image = "https://www.jpl.nasa.gov" + full_image  # Make the full URL

    mars["jpl_image"] = jpl_image


    ################
    # Mars Weather #
    ################

    mw_twitter = "https://twitter.com/marswxreport?lang=en"
    mw_html = requests.get(mw_twitter)
    mw_weather = bs(mw_html.text, 'html.parser')
    latest_tweet = mw_weather.find(
        'p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weather = latest_tweet.text

    mars["weather"] = mars_weather


    ##############
    # Mars Facts #
    ##############

    facts_url = "https://space-facts.com/mars/"

    # There is only 1 table, turn it from list item to DataFrame
    tables_df = pd.read_html(facts_url)[0]

    # Clean it up
    tables_df.columns = ["Attribute", "Value"]
    tables_df.set_index("Attribute", inplace=True)
    #tables_df.head()

    # Convert to HTML and clean out \n
    tables_html = tables_df.to_html()
    tables_html = tables_html.replace('\n', '')
    #tables_html

    mars["facts"] = tables_html


    ####################
    # Mars Hemispheres #
    ####################

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(usgs_url)

    usgs_html = browser.html
    usgs_hemis = bs(usgs_html, 'html.parser')

    # Get the link extensions for each hemisphere page
    hemi_links = usgs_hemis.find_all('div', class_="item")

    usgs_base = "https://astrogeology.usgs.gov/"

    # Create full links for each hemisphere page
    links = [usgs_base + link.a['href'] for link in hemi_links]
    #links

    hemis = []  # Create a list object to hold the dictionary of outputs for each hemisphere

    for link in links:

        browser.visit(link)
        html = browser.html
        info = bs(html, 'html.parser')

        # Pull the name of the hemisphere from the title
        name = info.find('h2', class_="title")
        # Remove the "Enhanced" word from the title string
        name = name.text.split(" ")[:-1]
        # Put the name of the hemisphere back together
        hemi_name = " ".join(name)

        browser.click_link_by_text('Sample')  # Click on the image link

        image_link = browser.url  # Take the URL from the image page

        # Add the name and image link as a dictionary to the hemis list
        hemis.append({"title": hemi_name, "image_url": image_link})

    #print(hemis)

    mars["hemi_info"] = hemis

    return mars

# Output mars:

#{'facts': '<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>Value</th>    </tr>    <tr>      <th>Attribute</th>      <th></th>    </tr>  </thead>  <tbody>    <tr>      <th>Equatorial Diameter:</th>      <td>6,792 km</td>    </tr>    <tr>      <th>Polar Diameter:</th>      <td>6,752 km</td>    </tr>    <tr>      <th>Mass:</th>      <td>6.42 x 10^23 kg (10.7% Earth)</td>    </tr>    <tr>      <th>Moons:</th>      <td>2 (Phobos &amp; Deimos)</td>    </tr>    <tr>      <th>Orbit Distance:</th>      <td>227,943,824 km (1.52 AU)</td>    </tr>    <tr>      <th>Orbit Period:</th>      <td>687 days (1.9 years)</td>    </tr>    <tr>      <th>Surface Temperature:</th>      <td>-153 to 20 °C</td>    </tr>    <tr>      <th>First Record:</th>      <td>2nd millennium BC</td>    </tr>    <tr>      <th>Recorded By:</th>      <td>Egyptian astronomers</td>    </tr>  </tbody></table>',
# 'hemi_info': [{'image_url': 'https://astrogeology.usgs.gov//search/map/Mars/Viking/cerberus_enhanced',
#                'title': 'Cerberus Hemisphere'},
#               {'image_url': 'https://astrogeology.usgs.gov//search/map/Mars/Viking/schiaparelli_enhanced',
#                'title': 'Schiaparelli Hemisphere'},
#               {'image_url': 'https://astrogeology.usgs.gov//search/map/Mars/Viking/syrtis_major_enhanced',
#                'title': 'Syrtis Major Hemisphere'},
#               {'image_url': 'https://astrogeology.usgs.gov//search/map/Mars/Viking/valles_marineris_enhanced',
#                'title': 'Valles Marineris Hemisphere'}],
# 'jpl_image': 'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA14417_ip.jpg',
# 'news_title': '\n\nNASA Invests in Visionary Technology \n\n',
# 'weather': 'Sol 2039 (May 02, 2018), Sunny, high 0C/32F, low -74C/-101F, pressure at 7.28 hPa, daylight 05:23-17:20'}
