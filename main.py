import tkinter as tk
from textblob import TextBlob
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from newspaper import Article


# Functions
def text_summarizer(text):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]

    freq_table = dict()
    for word in filtered_words:
        if word in freq_table:
            freq_table[word] += 1
        else:
            freq_table[word] = 1

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

    summary = ""
    for sentence in sentences:
        if sentence in sentence_value and sentence_value[sentence] > average:
            summary += " " + sentence

    return summary


def generate_abstractive_summary(text, sentences_count=10):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count)
    return " ".join(str(sentence) for sentence in summary)


def summarize_and_display(article):
    article.download()
    article.parse()
    article.nlp()

    title.config(state="normal")
    author.config(state="normal")
    publication.config(state="normal")
    summary.config(state="normal")
    sentiment.config(state="normal")

    title.delete("1.0", "end")
    author.delete("1.0", "end")
    publication.delete("1.0", "end")
    summary.delete("1.0", "end")
    sentiment.delete("1.0", "end")

    title.insert("1.0", article.title)
    author.insert("1.0", article.authors)
    publication.insert("1.0", article.publish_date)
    summary.insert("1.0", article.summary)

    analysis = TextBlob(article.text)
    sentiment.insert("1.0", f"Polarity: {analysis.polarity}, Sentiment: {'positive' if analysis.polarity > 0 else 'negative' if analysis.polarity < 0 else 'neutral'}")

    abstractive_summary = generate_abstractive_summary(article.text)

    second_summary.config(state="normal")
    second_summary.delete("1.0", "end")
    second_summary.insert("1.0", abstractive_summary)
    second_summary.config(state="disabled")

    # Move extractive summarization to the end
    extractive_summary = text_summarizer(article.text)
    with open("original_text.txt", "w", encoding="utf-8") as file:
        file.write(article.text)

    with open("summaries.txt", "w", encoding="utf-8") as file:
        file.write(
            f"Extractive summary newspaper3k:\n{article.summary}\n\nExtractive summary through function:\n{extractive_summary}\n\nAbstractive summary:\n{abstractive_summary}")

    # Update the third summary
    extractive_summary_custom = text_summarizer(article.text)
    third_summary.config(state="normal")
    third_summary.delete("1.0", "end")
    third_summary.insert("1.0", extractive_summary_custom)
    third_summary.config(state="disabled")


def get_article_and_summarize():
    url = url_text.get("1.0", "end").strip()
    article = Article(url)
    summarize_and_display(article)


# Interface
root = tk.Tk()
root.title("News Summarizer")
root.geometry("1200x1000")  # Increased height to accommodate the third summary

title_label = tk.Label(root, text="Title")
title_label.pack()
title = tk.Text(root, height=1, width=140)
title.config(state='disabled', bg="#dddddd")
title.pack()

author_label = tk.Label(root, text="Author")
author_label.pack()
author = tk.Text(root, height=1, width=140)
author.config(state='disabled', bg="#dddddd")
author.pack()

publication_label = tk.Label(root, text="Publication Date")
publication_label.pack()
publication = tk.Text(root, height=1, width=140)
publication.config(state='disabled', bg="#dddddd")
publication.pack()

summary_label = tk.Label(root, text="Extractive summary (newspaper3k)")
summary_label.pack()
summary = tk.Text(root, height=10, width=140)
summary.config(state='disabled', bg="#dddddd")
summary.pack()

second_summary_label = tk.Label(root, text="Abstractive summary")
second_summary_label.pack()
second_summary = tk.Text(root, height=10, width=140)
second_summary.config(state='disabled', bg="#dddddd")
second_summary.pack()

third_summary_label = tk.Label(root, text="Extractive Summary (Custom Function)")
third_summary_label.pack()
third_summary = tk.Text(root, height=10, width=140)
third_summary.config(state='disabled', bg="#dddddd")
third_summary.pack()

sentiment_label = tk.Label(root, text="Sentiment Analysis")
sentiment_label.pack()
sentiment = tk.Text(root, height=1, width=140)
sentiment.config(state='disabled', bg="#dddddd")
sentiment.pack()

url_label = tk.Label(root, text="URL")
url_label.pack()
url_text = tk.Text(root, height=1, width=140)
url_text.pack()

summarize_button = tk.Button(root, text="Summarize", command=get_article_and_summarize)
summarize_button.pack()

root.mainloop()
