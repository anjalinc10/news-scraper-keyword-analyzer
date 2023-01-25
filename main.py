import os.path

from news_scraper.scraping import get_article_urls, run_scraping_and_kw_analysis
from news_scraper.email_utils import send_email_with_attachment

if __name__ == "__main__":
    wd_news_website = "https://thewaltdisneycompany.com/investor-relations-news/"
    output_dir = "output/"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    article_urls = get_article_urls(wd_news_website)
    for index, url in enumerate(article_urls):
        output_file = output_dir + f"article{index + 1:02}_kw_freq"
        sender_email = "anjalinathe7@gmail.com"
        sender_password = "mngktfuykwddfyzh"
        recipient_email = "anjalinathe7@gmail.com"
        subject = "Test Email Subject"
        output_filepath = run_scraping_and_kw_analysis(url, output_file)
        if output_filepath:
            send_email_with_attachment(sender_email, sender_password, recipient_email, subject, output_filepath)
        print("=======================================================================================================")
