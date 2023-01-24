import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import re
import lxml
import json
from datetime import datetime


def get_article_urls(website_url):
    # get the HTML content of the website and parse it using BeautifulSoup
    source = requests.get(website_url).text
    soup = BeautifulSoup(source, "lxml")
    # find all the <article> tags on the page
    articles_all = soup.find_all("article")

    # loop through each article and fetch article url
    articles_list = []
    for article in articles_all:
        # find the <a> tag within the <h2> tag
        article_url = article.find("h2").find("a", href=True)
        articles_list.append(str(article_url['href']))
    return articles_list


def get_article_text(article_url):
    source = requests.get(article_url).text
    soup = BeautifulSoup(source, "lxml")

    # Extract text from all the headings present in the article
    header = soup.find("header", class_="entry-header")
    heading_text = ""
    for heading in header.find_all(["h1", "h2", "h3"]):
        heading_text = heading_text + " " + str(heading.text)
    # Extract text from the article body
    body_text = ""
    content_div = soup.find('div', class_='entry-content')
    # find all the tables and remove them
    for table_div in content_div.find_all("div", class_="bw-release-table"):
        table_div.decompose()
    # loop through all the <p> tags in the content_div
    # And add the text of the <p> tag to the body_text string
    for paragraph in content_div.find_all('p'):
        body_text = body_text + " " + str(paragraph.text)
    text_all = heading_text + " " + body_text
    return text_all


def clean_and_tokenize_text(text):
    # Normalizing case
    text_all = text.lower()
    # Convert to word tokens
    words = re.findall('[\w-]+', text_all)
    return words


def calculate_keyword_frequency(tokens, keyword_themes):
    keyword_freq = {key: 0 for key in keyword_themes.keys()}
    for token in tokens:
        for key in keyword_themes.keys():
            if token in keyword_themes[key]:
                keyword_freq[key] += 1
    return keyword_freq


def get_page_metadata(url):
    """ This function takes weburl as input , scrapes webpage metadata such as title and posted-on date from url
    and returns dictionary object containing Title and Posted-on date """

    source = requests.get(url).text
    b_soup = BeautifulSoup(source, "lxml")

    page_metadata = {}
    # Scraping page title
    title = b_soup.find("title")
    page_metadata['title'] = title.text

    # Scraping webpage posted-on date
    posted_date = b_soup.find("span", class_="posted-on")
    time_div = posted_date.find_all("time")
    # if this section has multiple time tags, selecting text from last time tag as
    # it would be having the latest update date
    page_metadata['posted_date'] = time_div[len(time_div) - 1].text
    return page_metadata


def plot_keyword_freq_bargraph(keyword_freq):
    """ This function takes keyword freq dictionary object as input and plot
    bar-graph using matplotlib library and returns matplotlib.pyplot object """

    labels = keyword_freq.keys()
    values = list(keyword_freq.values())

    xpos = list(range(len(labels)))

    plt.title("Keyword Frequency Analysis")
    plt.style.use("ggplot")
    plt.bar(xpos, values, align='center', color='green')
    plt.xticks(xpos, labels)
    plt.ylabel("Frequency", fontsize=12)
    plt.xlabel("Keywords", fontsize=12)
    return plt


def run_scraping_and_kw_analysis(url, output_filename):
    print(f"Processing News Article - {url}")
    # Reading keyword themes from config file
    with open("news_scraper/config.json", "r") as f:
        config = json.load(f)

    keyword_themes = config['themes_and_keywords']
    # Converting all keywords to lowercase
    for theme in keyword_themes.keys():
        keyword_themes[theme] = [kw.lower() for kw in keyword_themes[theme]]

    # Scrape Article page metadata and print it on stdout
    page_metadata = get_page_metadata(url)
    print("Title :{} \nPosted Date :{} ".format(page_metadata['title'], page_metadata['posted_date']))
    # convert posted_date to datetime format
    posted_date = page_metadata['posted_date'].strip()  # removing leading and trailing process
    posted_date = datetime.strptime(posted_date, "%B %d, %Y").date()

    # Scrape Article text
    text = get_article_text(url)

    # Clean and tokenize text
    tokens = clean_and_tokenize_text(text)
    if len(tokens) < 200:
        print("Skipping the article as number of words in the article are less than 200")
        return

    # calculate keyword frequency
    keyword_freq = calculate_keyword_frequency(tokens, keyword_themes)

    # Plotting bar graph and saving plot to pdf file
    bar_graph = plot_keyword_freq_bargraph(keyword_freq)
    output_filename = output_filename + "_" + str(posted_date) + ".pdf"
    bar_graph.savefig(output_filename)
    print(f"Processing completed, Bar graph is plotted and saved to {output_filename} in output directory ")
    # bar_graph.show()

