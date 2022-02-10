import re
import pickle
import spacy 
import unicodedata
from keras.models import load_model
from germansentiment import SentimentModel
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import pyreadr
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from datetime import date
import streamlit as st

def plot_by_party(party):
    tweets = pyreadr.read_r('candidates_17.rds')
    tweets = tweets[None]
    tweets = tweets[tweets['tw_id'].notnull()]
    tweets = tweets[tweets['party_name_fb1'].notnull()]
    party_tweets = tweets[(tweets['party_name_fb1'] == party)]
    tweet_profession = party_tweets['profession'].tolist()
    plot_profession(tweet_profession)
    party_sex = party_tweets['sex'].value_counts()
    plot_sex(party_sex)
    party_age = party_tweets['age'].tolist()
    plot_age(party_age)
	
def plot_profession(tweet_profession):
    unique_string = (" ").join(tweet_profession)
    wordcloud = WordCloud(width=1800, height=1000, background_color="white", colormap="twilight_shifted").generate(unique_string)
    wordcould_plot = plt.imshow(wordcloud)
    wordcould_plot = plt.axis("off")
    return st.pyplot()
	
def plot_sex(party_sex):
    labels = [ 'Männlich', 'Weiblich']
    plt.pie(party_sex, autopct='%1.1f%%')#,labeldistance=0.2
    plt.legend(labels, loc = "upper right")
    return st.pyplot()
	
def plot_age(party_age):
    party_age_calculated = [calculate_age(age) for age in party_age]
    plt.hist(party_age_calculated, bins=15, color='blue', edgecolor='k')
    plt.xlim([20, 80])
    plt.ylim([0, 30])
    plt.axvline(np.mean(party_age_calculated), color='k', linestyle='dashed', linewidth=1)
    #plt.axvline(np.median(party_age_calculated), color='k', linestyle='dashed', linewidth=1)
    plt.xlabel("Alter")
    plt.ylabel("Altersverteilung")
    plt.title("Altersverteilung der Partei")
    min_ylim, max_ylim = plt.ylim()
    plt.text(np.mean(party_age_calculated)*1.1, max_ylim*0.9, 'Durchschnittsalter: {:.2f}'.format(np.mean(party_age_calculated)))
    return st.pyplot()
	
def calculate_age(born):
    born = datetime.strptime(born, "%Y").date()
    today = date.today()
    return today.year - born.year

def plot_differences(party_list):
    tweets = pyreadr.read_r('candidates_17.rds')
    tweets = tweets[None]
    tweets = tweets[tweets['tw_id'].notnull()]
    tweets = tweets[tweets['party_name_fb1'].notnull()]
    party_tweets_1 = tweets[(tweets['party_name_fb1'] == party_list[0])]
    party_tweets_2 = tweets[(tweets['party_name_fb1'] == party_list[1])]
    party_age_1 = party_tweets_1['age'].tolist()
    party_age_2 = party_tweets_2['age'].tolist()
    #titanic[titanic["Age"] > 35]
    party_sex_1_man = party_tweets_1[party_tweets_1["sex"] == "0"].shape[0]
    party_sex_1_woman = party_tweets_1[party_tweets_1["sex"] == "1"].shape[0]
    party_sex_2_man = party_tweets_2[party_tweets_2["sex"] == "0"].shape[0]
    party_sex_2_woman = party_tweets_2[party_tweets_2["sex"] == "1"].shape[0]
    party_age_calculated_1 = [calculate_age(age) for age in party_age_1]
    party_age_calculated_2 = [calculate_age(age) for age in party_age_2]
    median_party_1 = np.median(party_age_calculated_1)
    median_party_2 = np.median(party_age_calculated_2)
    mean_party_1 = np.mean(party_age_calculated_1)
    mean_party_2 = np.mean(party_age_calculated_2)
    
    result = f"""Der Altersdurchschnitt der Partei **_{party_list[0]}_** beträgt: **_{str(round(mean_party_1, 2))}_** Jahre.
Der Alterduchschnitt der Partei **_{party_list[1]}_** beträgt hingegen **_{str(round(mean_party_2, 2))}_** Jahre.
Die Differenz betragt somit **_{round(abs(mean_party_1-mean_party_2), 2)}_** Jahre.
Auf eine Frau kommen im Verhältnis **_{round(party_sex_1_woman/party_sex_1_man, 1)}_** Männer in der Partei **_{party_list[0]}_**.
In der Partei **_{party_list[1]}_** kommen auf eine Frau im Verhältnis hingegen **_{round(party_sex_2_woman/party_sex_2_man, 1)}_** Männer."""

    return st.markdown(result)