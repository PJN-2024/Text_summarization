# Extractive summarization

# newspaper3k package
from newspaper import Article
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

url = ("https://edition.cnn.com/2024/01/26/us/alligator-kills-woman-florida-"
       "lawsuit/index.html")

article = Article(url)

article.download()
article.parse()
article.nlp()

# Summarizing with score
def text_summarizer(text):
    # Removing stop words
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    # Table with word frequency
    freq_table = dict()
    for word in filtered_words:
        if word in freq_table:
            freq_table[word] += 1
        else:
            freq_table[word] = 1

    # Assigning values to sentences
    sentences = sent_tokenize(text)
    sentence_value = dict()
    for sentence in sentences:
        for word, freq in freq_table.items():
            if word.lower() in sentence.lower():
                if sentence in sentence_value:
                    sentence_value[sentence] += freq
                else:
                    sentence_value[sentence] = freq

    sum_values = sum(sentence_value.values())
    average = int(sum_values / len(sentence_value))
    # Summarization
    summary = ""
    for sentence in sentences:
        if sentence in sentence_value and sentence_value[sentence] > average:
            summary += " " + sentence

    return summary


# Extractive summarization
extractive_summary = text_summarizer(article.text)
with open("original_text.txt", "w", encoding="utf-8") as file:
    file.write(article.text)

with open("extractive_summary.txt", "w", encoding="utf-8") as file:
    file.write(f"Summary newspaper3k:\n{article.summary}\n\nArticle Summary:\n{extractive_summary}")

# Summary
print(f"Title: {article.title}")
print(f"Authors: {article.authors}")
print(f"Publication date: {article.publish_date}")
print(f"Summary: {article.summary}")
print("\nExtractive Summary:")
print(extractive_summary)

# Abstractive summarization

