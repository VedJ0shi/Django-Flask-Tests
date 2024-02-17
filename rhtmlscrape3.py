from requests_html import HTML, HTMLSession


session = HTMLSession()
response = session.get("https://books.toscrape.com/") #uses requests library
html = response.html 
print(type(html)) #of HTML class
#print(html.html)
#print(html.text)

items = html.find("section > div > ol > li")
print(items, len(items))

titles = []
for item in items:
    imageinfo= item.find("img.thumbnail", first=True)
    #print(imageinfo.html)
    print(imageinfo.attrs) #returns dictionary of img Tag's attributes
    titles.append(imageinfo.attrs["alt"])
    print()

print(titles)

    