import streamlit as st
import numpy as np
import json
import pandas as pd
from tweepy import OAuthHandler, API, Stream, Cursor

import encrypt
import analytics
import streamlit_helper

st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(
layout="wide"
)

# Connection Twitter API
creds = encrypt.decrypt_file('twitter.key', 'twitter_credentials.json')
creds = json.loads(creds.decode('utf-8'))

auth = OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
api_twitter = API(auth)


def main():
  st.sidebar.title('Twitter Analysis')
  page = st.sidebar.selectbox('Choose a page', ["Homepage", "Parteien im Vergleich"])

  if page == 'Homepage':
    streamlit_helper.set_png_as_page_bg('./background.png')

    st.write("#")
    
    st.title('Big Data Consulting Project')
    st.header("FOM SS21")

    st.write("#")

    expander = st.beta_expander("Willkommen beim TwittOmat!")
    expander.write("Der TwittOmat ist eine Plattform, auf der du dich für die nächste Bundestagswahl in Deutschland über die Parteien deiner Wahl informieren kannst. Wir bieten dir die Möglichkeit, dich abseits der Wahlprogramme und Wahlkampfauftritte anhand der Tweets der Politiker und ihrer Parteien über ihre Themen, Standpunkte und das öffentliche Auftreten der Parteien ein Bild zu machen.")

    expander = st.beta_expander("Wer sind wir?")
    expander.write("Wir sind vier Studenten, die sich gefragt haben, ob man nicht anhand der vielen Tweets der Politiker ein ehrlicheres Bild der Politik der Parteien bekommen könnte als in den Wahlkampfprogrammen drinsteht.")

    expander = st.beta_expander("Was bieten wir an?")
    expander.write("Wir haben für dich die Tweets der Politiker der letzten Monate gesammelt und analysiert. Jetzt kannst du dir die Ergebnisse nach Partei unterteilt ansehen. Du kannst dir zwei Parteien vergleichend ansehen, schauen mit wem sie auf Twitter in Kontakt treten, oder herausfinden über welche Themen die Parteien am häufigsten getwittert haben.")

    expander = st.beta_expander("Was ist ‘Parteien im Vergleich’?") 
    expander.write("Im ‘Parteien im Vergleich’-Bereich kannst du dir die Analysen, die dich interessieren auswählen und ansehen. Wählen kannst du zwischen einer Analyse der Wahlkampfthemen, der Kommunikationswege und der Parteistrukturen.") 

    expander = st.beta_expander("Was wollen wir?") 
    expander.write("Wir wollen allen Interessierten ein Hilfsmittel an die Hand geben, um sich selbst in der vielfältigen Welt der Politik ein wenig besser zurecht zu finden und dabei vielleicht sogar etwas Spaß zu haben!") 
  
  elif page == 'Parteien im Vergleich': 
    streamlit_helper.set_png_as_page_bg('./background2.png')

    st.write("#")
    st.title('Vergleich von Parteien')
    st.write("#")

    options = st.sidebar.multiselect('Welche Analysen möchtest du durchführen?',
    ['Analyse von Wahlkampfthemen', 'Analyse von Kommunikationswegen', 'Analyse von Parteistruktur'])

    st.write("#")

    if ("Analyse von Wahlkampfthemen" in options):

      streamlit_helper.explainatory_text("Analyse von Wahlkampfthemen", "Topic Modeling ist ein Text-Mining-Tool zur Entdeckung von abstrakten Themen, die in einer Sammlung von Dokumenten vorkommen. Diese Visualisierung soll die Orientierung in den von Bundestags-Politiker besprochenen Themen ermöglichen.")
      st.write("##")
      streamlit_helper.deloy_html("./Fig_topics_per_class.html", 1000, 1500)
      
      st.write("##")
      st.write("##")

      streamlit_helper.explainatory_text("Topic Modeling Timeline", "Diese Visualisierung soll dir die Orientierung in den besprochenen Themen abhängig von der Zeit ermöglichen. Wenn du mit deiner Maus über die jeweiligen Linien fährst, siehst du, wann wie oft welches Thema besprochen wurde.")
      st.write("##")
      streamlit_helper.deloy_html("./Fig_over_time.html", 600, 1500)
      
      st.write("##")
      st.write("##")

      streamlit_helper.explainatory_text("Topic Modeling Timeline", "Topic Modeling ist ein Text-Mining-Tool zur Entdeckung von abstrakten Themen, die in einer Sammlung von Dokumenten vorkommen. Diese Visualisierung soll die Orientierung in den von Bundestags-Politiker besprochenen Themen abhängig von der Zeit ermöglichen.")
      st.write("##")
      streamlit_helper.deloy_html("./Fig_topics.html", 1000, 1000)

    if "Analyse von Kommunikationswegen" in options:

      streamlit_helper.explainatory_text("Analyse von Kommunikationswegen", "Hier kannst du dir ein Bild machen über die Zusammenhänge und den Dynamiken innerhalb und zwischen den Parteien. Wer kommuniziert mit wem? Wenn du mit deiner Maus über die Kreise der einzelnen Politiker fährst, erfährst du noch einige weitere Informationen über sie.")
      st.write("##")
      streamlit_helper.deloy_html("./alleszusammen.html", 2100, 2150)
  
    if "Analyse von Parteistruktur" in options:

      input_partei = st.sidebar.multiselect("Welche Partei möchtest du dir näher anschauen?", ['AfD', 'CDU', 'CSU', 'SPD', 'Linke', 'Grüne', 'FDP'])

      input_liste=[]
      

      if input_partei:
        for element in input_partei:

          input_liste.append(element)

        if len(input_liste) == 2:
          
          title = "Parteienvergleich von " + input_liste[0] + " und " + input_liste[1]
          streamlit_helper.explainatory_text(title, "")
          analytics.plot_differences(input_liste)
          
          col1, col2 = st.beta_columns(2)
          #st.title("Was unterscheidet sie?")
          
          #c1, c2, c3, c4 = st.beta_columns((2, 1, 1, 1))
          with col1:
            st.title(input_liste[0])
            analytics.plot_by_party(input_liste[0])
          

          with col2:
            st.title(input_liste[1])
            analytics.plot_by_party(input_liste[1])


          
if __name__ == '__main__':
  main()