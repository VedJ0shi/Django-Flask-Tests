from bs4 import BeautifulSoup
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/

with open("samples/articles.html") as wrapper:
    print(type(wrapper))
    soup = BeautifulSoup(wrapper, "lxml")
    print()

print(type(soup)) #BeautifulSoup objects have tree-like structure that can be queried in various ways
print(soup.body, type(soup.body)) #direct query returns a Tag object, which is also tree-like
print()

#can directly query for tags and text like object attributes, returns first match
print(soup.h1) #equivalently soup.body.h1 since first h1 tag is under body
print(soup.h2)
print(soup.h1.text)
print(soup.h2.a.text)
print()

print(soup.div)
#find specific tags using .find():
print(soup.find("div", class_= "footer"))
print()

article = soup.div
headline = article.h2.a.text
summary = article.p.text
print(headline)
print(summary)
print()

#returning an iterable of all tags that match query:
articles = soup.find_all("div", class_ = "article")
print(type(articles))
for article in articles:
    headline = article.h2.a.text
    summary = article.p.text
    print(articles.index(article))
    print(headline)
    print(summary)

