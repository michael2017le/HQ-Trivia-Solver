import io
import os
import requests
from bs4 import BeautifulSoup

from google.cloud import vision
from googlesearch import search

vision_client = vision.ImageAnnotatorClient()

image_file_name = 'a.png'
with io.open(image_file_name,'rb') as image_file:
  content = image_file.read()

image = vision.types.Image(content=content)

response = vision_client.text_detection(image=image)
texts = response.text_annotations

question = "  "
answers = {}
for text in texts:
  if question[-2]=='?':
    answers[text.description] = 0
  else:
    question+=text.description + ' '
maxKey = list(answers.keys())[0]

for i in search(question, tld="com", lang="en", num=3, stop=1, pause=1):
  page = requests.get(i)
  soup = BeautifulSoup(page.text, "html.parser")
  item_list = soup.find_all('p', limit=20)
  for item in item_list:
    for key, val in answers.items():
      if key in item:
        val+=1
        print(val)
      if answers[maxKey]<val:
        maxKey=key
        print(maxKey)
  print(maxKey)
