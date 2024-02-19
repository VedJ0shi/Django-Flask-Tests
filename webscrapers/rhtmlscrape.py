from requests_html import HTML

with open("samples/articles2.html") as wrapper:
    source = wrapper.read()
    html = HTML(html=source)
    print(type(html)) #of HTML class

print(html.html) #returns string of html code 
print(html.text) #returns string of all text segments in html code
print()

#use find() to acquire a tag by its CSS selector:
articles = html.find(".article") #returns list of Tags of class=article
footers = html.find("#footer") #returns list of Tags of id=footer
print(type(articles), len(articles))
print(type(footers), len(footers))
print()
print(articles[0].html)
print()
print(articles[1].html)
print()
print(footers[0].html)
print(footers[0].text)
print()
anchors = html.find("div > h2 > a") #returns list of anchor Tags
print(anchors[0].text)
print(anchors[1].html)
print(anchors[1].text)

