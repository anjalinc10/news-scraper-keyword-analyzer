import string

from bs4 import BeautifulSoup
import requests
import lxml
import re


def get_article_urls(website_url):
    source = requests.get(website_url).text
    soup = BeautifulSoup(source, "lxml")
    articles_all = soup.find_all("article")
    articles_list = []
    for article in articles_all:
        article_url = article.find("h2").find("a", href=True)
        articles_list.append(str(article_url['href']))
    return articles_list

# # website_url = "https://thewaltdisneycompany.com/investor-relations-news/"
# articles_list = get_article_urls(website_url)
# for url in articles_list:
#     print(url)


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
    # removing all the tables
    for table_div in content_div.find_all("div", class_="bw-release-table"):
        table_div.decompose()
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


article_url = "https://thewaltdisneycompany.com/mark-parker-to-be-named-chairman-of-the-walt-disney-company/"
text = get_article_text(article_url)
words = clean_and_tokenize_text(text)
print(words)



events = ['COVID-19', 'coronavirus', 'virus', 'pandemic', 'social', 'justice', 'floyd', 'george', 'racism',
              'police', 'brutality', 'injustice', 'inequality']
events = [word.lower() for word in events]

negative = ['cancelled', 'disruptions', 'suspend', 'suspended', 'cancellation', 'decrease', 'closed', 'loss',
            'mandates']
negative = [word.lower() for word in negative]

positive = ['contribution', 'donation', 'support', 'promote', 'promoting', 'commitment', 'opening', 'reopening',
            'increased', 'increase']
positive = [word.lower() for word in positive]

# Creating dictionary of keyword groups
keyword_grp_dict = {'events': events, 'negative': negative, 'positive': positive}


def generate_keyword_frequency(words, keyword_grp_dict):
    keyword_freq = {key: 0 for key in keyword_grp_dict.keys()}
    for word in words:
        for key in keyword_grp_dict.keys():
            if word in keyword_grp_dict[key]:
                keyword_freq[key] += 1
    return keyword_freq


generate_keyword_frequency()



# cleaning
# # Removing newline characters
# text_all = re.sub(r'\n', ' ', text_all)
# # Remove punctuations
# translator = str.maketrans('', ' ', string.punctuation)
# text_all = text_all.translate(translator)


