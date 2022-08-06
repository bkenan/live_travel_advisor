from flask import Flask
from flask import request
from flask import render_template
import torch
import librosa
import string
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import requests
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
import spacy
import pandas as pd
import numpy as np
import json
from word2number import w2n
from api import keys

#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('wordnet')
#spacy.cli.download("en_core_web_lg")

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload():
    f = request.files['audio_data']
    

    tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")


    speech, _ = librosa.load(f,sr=16000)
    input_values = tokenizer(speech, return_tensors = 'pt').input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim =-1)
    transcriptions = tokenizer.decode(predicted_ids[0])
    print(transcriptions)

    #sentence = "Cheapest hotel for two people in Paris from September eleventh until October second"
    categories_list_ui=['ascending stars', 'descending stars', 'popular', 'distance', 'reviews', 'cheapest']

    categories_list=['class_ascending', 'class_descending', 'popularity', 'distance', 'review_score', 'price']

    criterias=['low star', 'high star', 'popular', 'close to center', 'score based', 'cheapest']

    months = {
        'january': 1, 
        'february': 2,
        'march': 3,
        'april': 4, 
        'may': 5, 
        'june': 6, 
        'july': 7, 
        'august': 8, 
        'september': 9, 
        'october': 10, 
        'november': 11, 
        'december': 12
        }

    numbers = ['one', 
                'two',
                'three',
                'four',
                'five',
                'six',
                'seven',
                'eight',
                'nine',
                'ten'
                ]

    year = [2022,2022]

    def city():
        nlp = spacy.load('en_core_web_lg')

        doc = nlp(transcriptions)

        for ent in doc.ents:
            if ent.label_=='GPE':
                return ent.text

    def token():
    
        #tokenization
        tokens = nltk.word_tokenize(transcriptions)

        stop_words = set(stopwords.words('english'))

        #the list of stopwords
        punctuations = string.punctuation

        # Filter out stop words and punctuation
        tokens = [w for w in tokens if w.lower() not in stop_words and w not in punctuations]

        #lemmatize
        wordnet_lemmatizer = WordNetLemmatizer()
        tokens = [wordnet_lemmatizer.lemmatize(word).lower().strip() for word in tokens]
        return tokens

    def token_by_adjusted_day():
        tokens = token()
        for d in tokens:
            if d in ['twenty', 'thirty']:
                dd=tokens.index(d)
                g = tokens[dd]+tokens[dd+1]
                tokens[dd]= g
                tokens.pop(dd+1)
        return tokens

    def people():
        p = list(set(token_by_adjusted_day()) & set(numbers))[0]
        p_num = w2n.word_to_num(p)
        return p_num

    def category():
        c = list(set(token_by_adjusted_day()) & set(categories_list_ui))[0]
        order_by = categories_list[categories_list_ui.index(c)]
        return order_by

    def check_months():
        tokens =  token_by_adjusted_day()
        months_list = list(months.keys())
        final_months = list(set(tokens).intersection(months_list))
        mm_list=[]
        for f in final_months:
            mm = months[f]
            mm_list.append(mm)
        if len(mm_list)==1:
            mm_list=mm_list*2
        if mm_list[0] > mm_list[1]:
            mm_list.reverse()
        return mm_list

    def check_days():
        tokens = token_by_adjusted_day()
        days = pd.read_excel('./assets/days.xlsx')
        day_names = days['Word'].to_list()
        final_days = list(set(tokens).intersection(day_names))
        if len(final_days)==1:
            final_days=final_days*2
        if tokens.index(final_days[0]) > tokens.index(final_days[1]):
            final_days.reverse()
        dd_list=[]
        for d in final_days:
            dd = days.loc[days['Word'] == d, 'Number']
            l_dd=dd.to_list()
            dd_list.append(l_dd) 
        return [dd_list[0][0], dd_list[1][0]]


    def check_year():
        for m in check_months():
            if m<8:
                year[check_months().index(m)] = 2023
        return year     

    headers,url_locations,url_search=keys()

    def destination():
        querystring_locations = {"locale":"en-us","name":f"{city()}"}
        response_locations = requests.request("GET", url_locations, headers=headers, params=querystring_locations)
        dest = json.loads(response_locations.text)
        #df = pd.DataFrame(data)
        return dest[0]['dest_id']


    checkin_date = f"{check_year()[0]}-{check_months()[0]}-{check_days()[0]}"
    checkout_date = f"{check_year()[1]}-{check_months()[1]}-{check_days()[1]}"
    dest_id = destination()
    adults_number = f"{people()}"
    order_by = category()
    
    global checkin
    global checkout
    global number
    global order
    global location

    checkin = checkin_date
    checkout = checkout_date
    number = adults_number
    order = criterias[categories_list.index(order_by)]
    location = city()

    print(checkin_date, checkout_date, dest_id, adults_number, order_by)

    def request_api():

        querystring_search = {
            "checkout_date":checkout_date,
            "units":"metric",
            "dest_id":dest_id,
            "dest_type":"city",
            "locale":"en-us",
            "adults_number":adults_number,
            "order_by":order_by,
            "filter_by_currency":"USD",
            "checkin_date":checkin_date,
            "room_number":"1"}
            
        response_search = requests.request("GET", url_search, headers=headers, params=querystring_search)
        return response_search


    def error_check():
        try:
            request_api()
            print('Success!')
        except:
            print("An exception occurred")

    print(error_check())


    def results():
        
        try:
            data_search = json.loads(request_api().text)
            df = pd.DataFrame(data_search['result'])
            df = df[['hotel_name',
                    'class',
                    'accommodation_type_name',
                    'review_score_word',
                    'distance_to_city_centre_formatted',
                    'address',
                    'url']]
            df = df.rename(columns={'hotel_name': 'Name',
                            'class': 'Star',
                            'accommodation_type_name': 'Type',
                            'review_score_word': 'Review',
                            'distance_to_city_centre_formatted': 'Distance',
                            'address': 'Address',
                            'url': 'URL'})
            df.index += 1 
            df['Star'].replace(0, 'N/A', inplace=True)
            df['Review'].replace('', 'N/A', inplace=True)
            return df
        except:
            print("Try again!")

    
    
    global df2
    df2 = results().head(10)

    def make_clickable(val):
        return f'<a target="_blank" href="{val}">{val}</a>'

    df2.head(10).style.format({'URL': make_clickable})


    return render_template('index.html')



@app.route('/submit')
def submit():

    try:
        if df2.shape[0] ==10:
            return render_template('results.html',  
                                    title=f"Top 10 {order} hotels in {location} for {number} person(s) from {checkin} until {checkout}", 
                                    tables=[df2.to_html(header="true", 
                                    table_id="table", 
                                    render_links=True, 
                                    escape=False)])
        else:
            return render_template('error.html') 
    except NameError:
        return render_template('error.html') 



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)


