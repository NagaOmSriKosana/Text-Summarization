from flask import Flask, render_template, request
import re
import nltk
import heapq

app = Flask(__name__)

nltk.download('stopwords')

def summarize_text(article_text):
    # Convert the input text to lowercase
    article_text = article_text.lower()

    # Clean the text
    clean_text = re.sub('[^a-zA-Z]', ' ', article_text)
    clean_text = re.sub('\s+', ' ', clean_text)

    # Tokenize sentences
    sentence_list = nltk.sent_tokenize(article_text)

    # Get English stopwords
    stopwords = nltk.corpus.stopwords.words('english')

    # Calculate word frequencies
    word_frequencies = {}
    for word in nltk.word_tokenize(clean_text):
        if word not in stopwords:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    # Find the maximum word frequency
    maximum_frequency = max(word_frequencies.values())

    # Normalize word frequencies
    for word in word_frequencies:
        word_frequencies[word] = word_frequencies[word] / maximum_frequency

    # Calculate sentence scores
    sentence_scores = {}
    for sentence in sentence_list:
        for word in nltk.word_tokenize(sentence):
            if word in word_frequencies and len(sentence.split(' ')) < 30:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]

    # Get the top 5 sentences as the summary
    summary = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)

    # Return the summary as a string
    return " ".join(summary)

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_summary = None

    if request.method == 'POST':
        # Get the user input from the form
        user_text = request.form['user_text']

        # Generate the summary
        generated_summary = summarize_text(user_text)

    return render_template('index.html', generated_summary=generated_summary)

if __name__ == '__main__':
    app.run(debug=True)
