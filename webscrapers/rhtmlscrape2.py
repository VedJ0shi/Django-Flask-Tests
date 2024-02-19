from requests_html import HTML

with open("samples/articles2.html") as wrapper:
    source = wrapper.read()
    html = HTML(html=source)
    print(type(html)) #of HTML class

articles = html.find(".article")
print(articles, len(articles))
print()

for article in articles:
    print(article.html)
    headline = article.find("a", first=True).text
    summary = article.find("p", first=True).text
    print(headline)
    print(summary, end="\n\n")
