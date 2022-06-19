# Goodreads Quotes Scraper

# Output Format
import csv

# Required Libraries
import requests
import lxml
import requests
from bs4 import BeautifulSoup, NavigableString


# Writes scrapped quotes to CSV file and saves it
def write_to_csv(quotes_list):

    new_data = open('j_k_rowling.csv', mode='a',
                    encoding='utf-8-sig', newline='')
    csv_writer = csv.writer(new_data)
    s_no = 1
    csv_writer.writerow(('S. No.', 'Quotation', 'Author', 'Book', 'Tags'))
    for [text, author, title, tags] in quotes_list:
        csv_writer.writerow((s_no, text, author, title, tags))
        s_no = s_no + 1


def quotes_by_author(author, page_num=None):

    quotes_list = []

# if page number not specified, get true page number
    if page_num is None:
        try:
            page = requests.get(
                "https://www.goodreads.com/quotes/search?commit=Search&page=1" + "&q=" + author + "&utf8=%E2%9C%93")
            soup = BeautifulSoup(page.text, 'html.parser')
            pages = soup.find(class_="smallText").text
            a = pages.find("of ")
            page_num = pages[a + 3:]
            page_num = page_num.replace(",", "").replace("\n", "")
            page_num = int(page_num)
            print("looking through", page_num, "pages")
        except:
            page_num = 1

    # for each page
    for i in range(1, page_num + 1, 1):

        try:
            page = requests.get("https://www.goodreads.com/quotes/search?commit=Search&page=" +
                                str(i) + "&q=" + author + "&utf8=%E2%9C%93")
            soup = BeautifulSoup(page.text, 'html.parser')
            print("scraping page", i)
        except:
            print("could not connect to goodreads")
            break

        try:
            quote = soup.find(class_="leftContainer")
            quote_list = quote.find_all(class_="quoteDetails")
        except:
            pass

        # get data for each quote
        for quote in quote_list:

            meta_data = []

            # Get quote's text
            try:
                outer = quote.find(class_="quoteText")
                inner_text = [element for element in outer if isinstance(
                    element, NavigableString)]
                inner_text = [x.replace("\n", "") for x in inner_text]
                final_quote = "\n".join(inner_text[:-4])
                meta_data.append(final_quote.strip())
            except:
                pass

            # Get quote's author
            try:
                author = quote.find(class_="authorOrTitle").text
                author = author.replace(",", "")
                # author = author.replace("\n", "")
                meta_data.append(author.strip())
            except:
                meta_data.append(None)

            # Get quote's book title
            try:
                title = quote.find(class_="authorOrTitle")
                title = title.nextSibling.nextSibling.text
                # title = title.replace("\n", "")
                meta_data.append(title.strip())
            except:
                meta_data.append(None)

            # Get quote's tags
            try:
                tags = quote.find(class_="greyText smallText left").text
                tags = [x.strip() for x in tags.split(',')]
                tags = tags[1:]
                meta_data.append(tags)
            except:
                meta_data.append(None)

            quotes_list.append(meta_data)

    write_to_csv(quotes_list)

# Call function
quotes_by_author("jk rowling", 2)
