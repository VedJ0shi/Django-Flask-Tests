from bs4 import BeautifulSoup
import requests

source = requests.get("https://www.scrapethissite.com/pages/forms").text


soup = BeautifulSoup(source, "lxml")
#print(soup, type(soup))

bulk = soup.find("section", id = "hockey")

divs = bulk.find_all("div", class_="row") #returns iterable of div Tags
table = bulk.table #returns a table Tag

title = divs[0].text.strip()
subtitle = divs[1].text.strip()

print(title)
print(subtitle)

teams=[]
for row in table.find_all("tr", class_="team"):
    teams.append({"name": row.find("td", class_="name").text.strip(), "wins": row.find("td", class_="wins").text.strip()})

print(teams)
