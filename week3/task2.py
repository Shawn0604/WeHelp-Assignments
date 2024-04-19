import urllib.request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import csv
from datetime import datetime

url = "https://www.ptt.cc/bbs/Lottery/index.html"
# headers 用於傳送已滿 18 歲的 cookie， User-Agent 用於模擬瀏覽器讓機器不回傳403
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "cookie": "over18=1"
}

#建立一個 Request 物件,將 URL 和 headers 傳遞給它。然後使用 urllib.request.urlopen 打開 URL。另外用 try-expect 來處理可能的錯誤
def get_page_content(url):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return response.read().decode("utf-8")
            else:
                print("無法獲取頁面內容")
                return None
    except HTTPError as e:
        print("HTTP Error:", e.code, e.reason)
        return None
    except URLError as e:
        print("URL Error:", e.reason)
        return None

def parse_articles(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    articles = []

    for r_ent in soup.find_all("div", class_="r-ent"):
        if r_ent.find("div", class_="title").text.strip() == "(本文已被刪除) [saquchhh]":
            continue

        title = r_ent.find("div", class_="title").text.strip()

        nrec = r_ent.find("div", class_="nrec").text.strip()
        if nrec.startswith("X"):
            like_dislike_count = -1 * int(nrec[1:])
        elif nrec:
            like_dislike_count = int(nrec)
        else:
            like_dislike_count = 0

        # 從title爬出文章連結，進去裡面爬時間
        article_link = r_ent.find("div", class_="title").find("a")["href"]
        article_url = "https://www.ptt.cc" + article_link
        article_html_content = get_page_content(article_url)

        if article_html_content:
            article_soup = BeautifulSoup(article_html_content, "html.parser")
            meta_lines = article_soup.find_all("div", class_="article-metaline")

            publish_time = ""
            for meta_line in meta_lines:
                if meta_line.find("span", class_="article-meta-tag").text.strip() == "時間":
                    publish_time = meta_line.find("span", class_="article-meta-value").text.strip()
                    break

            if publish_time:
                publish_time = datetime.strptime(publish_time, "%a %b %d %H:%M:%S %Y").strftime("%a %b %d %H:%M:%S %Y")
            else:
                publish_time = ""
        else:
            publish_time = ""

        articles.append({
            "title": title,
            "like_dislike_count": like_dislike_count,
            "publish_time": publish_time
        })

    return articles

# 翻到上一頁
def get_prev_page_url(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    paging_btns = soup.find("div", class_="btn-group-paging").find_all("a", class_="btn")

    for btn in paging_btns:
        if "上頁" in btn.text:
            return "https://www.ptt.cc" + btn["href"]

    return None

all_articles = []
current_url = url
for i in range(3):
    html_content = get_page_content(current_url)
    if html_content:
        articles = parse_articles(html_content)
        all_articles.extend(articles)
        current_url = get_prev_page_url(html_content)
        if not current_url:
            break
    else:
        break

with open("article.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["ArticleTitle", "Like/DislikeCount", "PublishTime"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for article in all_articles:
        writer.writerow({
            "ArticleTitle": article["title"],
            "Like/DislikeCount": article["like_dislike_count"],
            "PublishTime": article["publish_time"]
        })

print(f"成功將 {len(all_articles)} 篇文章寫入 article.csv")