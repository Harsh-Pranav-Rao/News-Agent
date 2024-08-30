import streamlit as st
import spacy
import json

news_sites_categories = {
    "A": [
        ("The Times of India", 5),
        ("Hindustan Times", 5),
        ("The Hindu", 5),
        ("Economic Times", 5),
        ("Business Standard", 5),
        ("Hindustan Times Tech", 5),
        ("India Today Tech", 5),
        ("Financial Express Tech", 5),
        ("News 18 Tech", 5),
        ("Wall Street Journal", 5)
        ("south_china_morning_post", 5),
        ("nbc_news", 5)
    ],
    "B": [
        ("CNBC", 4),
        ("Yahoo Finance", 4),
        ("Business Insider", 4),
        ("CNN Business Tech", 4),
        ("Financial Times Tech", 4),
        ("DNA India Tech", 4),
        ("The Hindu Business Line", 4)
        ("indian_express_tech_news", 4),
        ("dealstreet_asia", 4),
        ("mint", 4),
        ("Krasia",4)
    ],
    "C": [
        ("PYMNTS", 3),
        ("TechMeme", 3),
        ("TNW", 3),
        ("Arstechnica", 3),
        ("Readwrite", 3),
        ("Tech in Asia", 3),
        ("Tech Crunch", 3),
        ("Venture Beat", 3),
        ("Tech Crunch Enterprise", 3),
        ("Tech Funding News", 3),
        ("Tech EU", 3),
        ("Macworld", 3),
        ("Nikkei", 3),
        ("The Verge", 3),
        ("Quartz", 3),
        ("Tech Times", 3),
        ("VC Circle", 3),
        ("China Daily", 3),
        ("Zdnet", 3),
        ("the_register", 3)
    ],
    "D": [
        ("EntrackR", 2),
        ("Pandaily", 2),
        ("UK Tech News", 2),
        ("Cloud Computing News", 2),
        ("CGTN Tech", 2),
        ("CGTN business", 2),
        ("Money Control Tech", 2),
        ("Money Control business", 2),
        ("Startup Reporter", 2),
        ("Tech Node", 2),
        ("AsiaTech", 2),
        ("Healthcare Dive", 2),
        ("FirstPost Tech", 2)
    ],
    "E": [
        ("amazon news", 1),
        ("Finextra", 1),
        ("Tech In Africa", 1)
    ]
}

# Load SpaCy model
nlp = spacy.load("en_core_web_trf")

# Load word scores from JSON file
with open('word_scores.json', 'r') as file:
    word_scores = json.load(file)

def preprocess_and_score_titles(title, word_scores):
    title = title.lower()
    # Process the title using spaCy
    doc = nlp(title)
    # Lemmatize and clean up the title
    lemmatized_words = [token.lemma_ for token in doc if not token.is_punct and not token.is_stop]
    # Calculate the score for the title
    score = 0
    for word in lemmatized_words:
        if word in word_scores:
            score += word_scores[word]
    return score

def analyze_title(title, word_scores):
    title = title.lower()
    doc = nlp(title)
    lemmatized_words = [token.lemma_ for token in doc if not token.is_punct and not token.is_stop]
    
    analysis = []
    total_score = 0
    
    for word in lemmatized_words:
        score = word_scores.get(word, 0)
        analysis.append(f"{word} : is in dictionary and it has a score of : {score}")
        total_score += score
    
    return analysis, total_score, lemmatized_words

# Streamlit App
st.title("News Title Scoring App")
st.write("Enter a news title to calculate its score based on predefined word scores.")

# Input box for news title
news_title = st.text_input("News Title")

if st.button("Calculate"):
    if news_title:
        score = preprocess_and_score_titles(news_title, word_scores)
        st.write(f"The score for the news title is: {score}")
    else:
        st.write("Please enter a news title.")

if st.button("Analyze"):
    if news_title:
        analysis, total_score, lemmatized_words = analyze_title(news_title, word_scores)
        st.write(f"Original title: {news_title}")
        st.write(f"Processed title: {' '.join(lemmatized_words)}")
        for line in analysis:
            st.write(line)
        st.write(f"Total score: {total_score}")
    else:
        st.write("Please enter a news title.")



'''
1)Get json of name and ticker, valuation
2)creaete histogram on dict to show dist of score
3)Financial Figure 
3)in st pass 1000 diff news article title, get scores and plot histogram here as well
4)Categorize the news articles 5 categories in terms of readership count
5)Similarity - 3 days - jellyfish,Levenshtein, Jaro

take all scores, divide by 100, any score which crosses 1 is set to 1
number of news sources iun every category histogram
figure out how to separate the news site from the embedding of the title
generate the news site score for all titles and add it to their original score and display histogram


exclude other articles by same publisher
split the embedding function 
80% and above for similarity


Sentiment Analysis: Use a simple sentiment analysis to identify very positive or negative words. Apply a small bonus (1.1x multiplier) for strong sentiment in either direction. -> FinBERT , Roberta-large , 10 news titles compare the scores
Context Window: For longer titles, consider implementing a sliding window approach to capture context around important keywords. -> take all the titles, find 2 gram ,3,4,5 that occur more than once. Keep a count of instances.
Timeliness Factor: If the title contains words indicating recency (e.g., "breaking", "just announced", "today"), add a score to the total score.
Abbreviation expansion. -> ai -> artificial intelligence
Make a more effecient way to compare title similarity

Takes the content of all the news sites and generate a summary




Not doing:
Title Length Adjustment: Multiply the total score by (1 + 0.1 * (word count / 10)) to give a slight boost to longer, potentially more informative titles. 

for content:
Keyword Density: If more than 30% of the words in the title are scored keywords, apply a 1.2x multiplier to the total score.


divide all scores by 61.0 (anything above 1 becomes 1)
Plot a bar chart of the final scores - cap it by 100


2 gram words dictionary
duplication removal

Documentation
What it does , how it does, by how much

Deploy on st publically



'''
