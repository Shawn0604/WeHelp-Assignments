import csv
import urllib.request as req
import bs4
from urllib.error import URLError, HTTPError
from datetime import datetime

def get_page_html(url):
    headers = {
        "Cookie": "over18=1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
    request = req.Request(url, headers=headers)
    try:
        with req.urlopen(request) as response:
            html_content = response.read().decode('utf-8')
    except HTTPError as http_error:
        print(f"HTTP error occurred: {http_error}")
        return None
    except URLError as url_error:
        print(f"URL error occurred: {url_error}")
        return None
    except Exception as error:
        print(f"Other error occurred: {error}")
        return None
    
    soup = bs4.BeautifulSoup(html_content, "html.parser")
    return soup

def get_titles_and_likes(soup):
    titles_with_tag = soup.find_all("div", class_="title")
    titles = [item.a.string for item in titles_with_tag if item.a != None]

    likes_with_tag = soup.find_all("div", class_="r-ent")
    likes = []
    for i, item in enumerate(likes_with_tag):
        if item.div.span == None:
            if titles_with_tag[i].a == None:
                pass
            else:
                likes.append("0")
        else:
            likes.append(item.div.span.string)
    return titles, likes

def get_dates(soup):
    titles_with_tag = soup.find_all("div", class_="title")
    title_link_with_tag = [
        item.a for item in titles_with_tag if item.a != None]
    links = ["https://www.ptt.cc" + a.get("href") for a in title_link_with_tag]

    dates = []
    for i, link in enumerate(links):
        article = get_page_html(link)
        date_with_tag = article.select_one(
            ".article-metaline:nth-of-type(4) .article-meta-value")
        if date_with_tag == None:
            dates.append(" ")
        else:
            dates.append(date_with_tag.string)
    return dates

def get_previous_link(soup):
    previous_link_with_tag = soup.find("a", string="‹ 上頁")
    previous_link = "https://www.ptt.cc" + previous_link_with_tag["href"]
    return previous_link

def process_data(soup):
    titles, likes = get_titles_and_likes(soup)
    dates = get_dates(soup)
    result = [{"標題": title, "按讚數": like, "發文時間": date}
              for title, like, date in zip(titles, likes, dates)]
    return result

src = "https://www.ptt.cc/bbs/Lottery/index.html"

all_data = []

for i in range(3):
    soup = get_page_html(src)
    data = process_data(soup)[::-1]
    all_data.extend(data)
    previous_link = get_previous_link(soup)
    src = get_previous_link(soup)

with open("article.csv", "w", encoding="utf-8", newline="") as file:
    fieldnames = ["標題", "按讚數", "發文時間"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for row in all_data:
        writer.writerow(row)
