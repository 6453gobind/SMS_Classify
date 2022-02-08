from django.shortcuts import render
import requests
import pickle
from nltk.stem import SnowballStemmer
import string
import re
import nltk


def sms(request):
    return render(request,'home.html',{'data':"NEW"})

def output(request):
    output_result = {}
    data = "HELLO GOBIND"
    data = request.GET['sms']
    print(data)
    output_result["data"]=data
    

    filename = 'trained_model.sav'
    filename_2 = 'trained_vectorizer.sav'

    # load the model from disk
    loaded_model = pickle.load(open(filename, 'rb'))
    loaded_vectorizer = pickle.load(open(filename_2, 'rb'))

    def cleaning (text):
        stopwords = nltk.corpus.stopwords.words('english')
        stemmer = SnowballStemmer('english')
        text = text.lower()
        text = "".join([i for i in text if i not in string.punctuation])
        text = re.split('W+',text)
        text = [stemmer.stem(word) for word in text]
        text= [i for i in text if i not in stopwords]
        text = " ".join(text)
        return(text) 

# "You available now? I'm like right around hillsborough &amp;  &lt;#&gt; th"   
    testing = data
    #Pre-processing the new string
    testing = [cleaning (testing)]

    #converting words to numerical data using tf-idf
    X_vector = loaded_vectorizer.transform(testing)

    #use the best model to predict 'target' value for the new dataset 
    y_predict = loaded_model.predict(X_vector)      
    y_prob = loaded_model.predict_proba(X_vector)[:,1]
    
    if(y_prob[0]>0.7):
        y_predict=1
        
    if(y_predict):
        y_predict="SPAM"
    else:
        y_predict="NOT A SPAM"
    
    
    output_result["prob"] = str(y_prob[0]) 
    output_result["pred"] = str(y_predict) 
    return render(request,'home.html',{'data':output_result})