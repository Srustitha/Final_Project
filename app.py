import streamlit as st
import pandas as pd
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
nltk.download('punkt')
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style='white')
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import xgboost as xgb
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix, precision_score, recall_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.model_selection import KFold

import warnings
warnings.filterwarnings('ignore')

def generate_summary(teacher_feedback):
    # Tokenize the feedback into sentences
    sentences = sent_tokenize(teacher_feedback)

    if len(sentences) == 0:
        st.text("No feedback available.")

    # Encode sentences into BERT embeddings
    sentence_embeddings = model.encode(sentences)

    # Calculate the mean embedding of all sentences
    mean_embedding = sentence_embeddings.mean(axis=0, keepdims=True)

    # Calculate cosine similarity between each sentence embedding and the mean embedding
    cos_similarities = cosine_similarity(sentence_embeddings, mean_embedding)

    # Sort sentences by cosine similarity in descending order
    sorted_indices = cos_similarities.flatten().argsort()[::-1]

    # Select the top two sentences as representative
    num_sentences = min(1,2) # Adjust the number of sentences as needed
    representative_sentences = [sentences[idx] for idx in sorted_indices[:num_sentences]]

    # Generate summary
    summary = ' '.join(representative_sentences)
    return summary

st.header('RAMACHANDRA COLLEGE OF ENGINEERING')
st.title('STUDENT FEEDBACK ANALYZER')
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

csv=st.file_uploader('Upload Feedback File here')
if csv:
    df = pd.read_csv(csv)
# Load the dataset
# Specify the range of teachers to consider
    def preprocess_text(text):
        text = text.lower()

    # Remove URLs, hashtags, mentions, and special characters
        text = re.sub(r"http\S+|www\S+|@\w+|#\w+", "", text)
        text = re.sub(r"[^\w\s]", "", text)

    # Remove numbers/digits
        text = re.sub(r'\b[0-9]+\b\s*', '', text)

    # Remove punctuation
        text = ''.join([char for char in text if char not in string.punctuation])

    # Tokenize the text
        tokens = word_tokenize(text)

    # Remove stop words
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]

    # Lemmatize the words
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Join tokens back into a single string
        return ' '.join(tokens)

    df['Processed_Feedback 1'] = df["Teacher 1"].apply(preprocess_text)
    df['Processed_Feedback 2'] = df["Teacher 2"].apply(preprocess_text)
    df['Processed_Feedback 3'] = df["Teacher 3"].apply(preprocess_text)
    df['Processed_Feedback 4'] = df["Teacher 4"].apply(preprocess_text)
    df['Processed_Feedback 5'] = df["Teacher 5"].apply(preprocess_text)

    def sentiment_analyzer(score):
        if score > 0.049889:
            return 'positive'

        elif score < 0.049889:
            return 'negative'
        else:
            return 'neutral'
    df['Sentiments 1'] = df['Sentiment_Scores 1'].apply(sentiment_analyzer)
    df['Sentiments 2'] = df['Sentiment_Scores 2'].apply(sentiment_analyzer)
    df['Sentiments 3'] = df['Sentiment_Scores 3'].apply(sentiment_analyzer)
    df['Sentiments 4'] = df['Sentiment_Scores 4'].apply(sentiment_analyzer)
    df['Sentiments 5'] = df['Sentiment_Scores 5'].apply(sentiment_analyzer)
    total_reviews = len(df)

# Count the number of negative sentiment labels
    negative_count = df['Sentiments 1'].value_counts().get('negative', 0)
    positive_count=  df['Sentiments 1'].value_counts().get('positive', 0)

# Check if more than half of the reviews are negative
    if positive_count > total_reviews / 2:
        print("Majority Students feedback on Teacher 1  is Positive.")
    elif positive_count==negative_count:
        print("Majority Students feedback on Teacher 1  is Neutral.")
    else:
      print("Majority Students feedback on Teacher 1  is Negative.")
        
   
    start_teacher = 1
    end_teacher = 5  # Adjust as needed
    # Generate summary for each teacher in the specified range
    for i in range(start_teacher, end_teacher + 1):
        if 'Teacher '+str(i) in df.columns and not df['Teacher '+str(i)].isnull().all():
            teacher_feedback = df['Teacher '+str(i)].dropna().str.cat(sep=' ')
            st.text("Summary of feedback for :"+'Teacher '+str(i))
            st.text(generate_summary(teacher_feedback))

        else:
            st.text("No feedback available for Teacher"+str(i))
