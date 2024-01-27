# Abstractive summarization

import nltk
# newspaper3k package
from newspaper import Article

url = ("https://edition.cnn.com/2024/01/26/us/alligator-kills-woman-florida-"
       "lawsuit/index.html")

article = Article(url)

article.download()
article.parse()
article.nlp()

print(f"Title: {article.title}")
print(f"Authors: {article.authors}")
print(f"Publication date: {article.publish_date}")
print(f"Summary: {article.summary}")

# Extractive summarization
