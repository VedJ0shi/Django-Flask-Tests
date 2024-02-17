import requests 

response = requests.get("https://xkcd.com/")
img_response = requests.get("https://imgs.xkcd.com/comics/research_account_2x.png")

print(response.status_code) #returns 200 OK from underlying HTTP Response Header
print(response.headers) #returns HTTP Response Header as a dict
print()

print(response, type(response)) #of Response class
print(img_response, type(img_response)) #of Response class
print(dir(response)) #returns all the attributes and methods accessible by Response objects
print()

#print(response.text) #text attribute contains the unicode content of Response object
source = response.text #str that can be later used for HTML parsing
#print(img_response.content) #content attribute contains the byte content of Response object
bytesource = response.content #bytes that can be later used for image analysis

