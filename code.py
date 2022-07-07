from __future__ import print_function
from google_images_download import google_images_download
import json
import pandas as pd  
import datetime
import os
import requests
import sys
from flask import Flask,render_template,request
from bing_image_downloader import downloader
#from werkzeug.utils import secure_filename

fullDict = {}
with open('data.json') as json_file:
    fullDict = json.load(json_file)
        
app = Flask(__name__, template_folder="C:\\Users\\dhanv\\Downloads\\project")


yearSelect = ''
makeSelect = ''

@app.route("/")
def form():
    global fullDict
    global yearSelect
    global makeSelect  

    return render_template('form.html', years = list(fullDict.keys()))
    
@app.route("/selectingMake", methods=['POST'])
def makeSelect():
    global fullDict
    global yearSelect
    global makeSelect
    
    yearSelect = request.form['yearSelect']
    
    return render_template('form1.html', years = list(fullDict.keys()), makes = list(fullDict[yearSelect].keys()), selectedYear = yearSelect)
    
@app.route("/selectingModel", methods=['POST'])
def modelSelect():
    global yearList
    global makeList
    global modelList
    global yearSelect
    global makeSelect
    
    makeSelect = request.form['makeSelect']
    
        
    return render_template('form2.html', years = list(fullDict.keys()), makes = list(fullDict[yearSelect].keys()), models = fullDict[yearSelect][makeSelect], selectedYear = yearSelect, selectedMake = makeSelect)
    
 
@app.route('/VinResults', methods=['POST'])
def getfile():
    if request.method == 'POST':    
        global yearList
        url = 'https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/' + request.form['text'] + '?format=json'
        #url = 'https://api.nhtsa.gov/complaints/complaintsByVehicle?make=Chevrolet&model=Tahoe&modelYear=2018'
        
        vinDict = requests.get(url).json().get('Results')
         
        df = pd.DataFrame.from_dict(vinDict).transpose()
        df.columns = ['Value']
        a = df.loc[df['Value'] == '']
        b = df.loc[df['Value'] != '']
        df = pd.concat([b, a])
        
        
        url2 = 'https://api.nhtsa.gov/complaints/complaintsByVehicle?make=' + vinDict[0]['Make'] + '&model='+vinDict[0]['Model']+'&modelYear='+vinDict[0]['ModelYear']
        df2 = pd.DataFrame.from_dict(requests.get(url2).json()['results']).head(10)
        #df2 = pd.DataFrame.from_dict(requests.get(url2).json())
        url2 = 'https://api.nhtsa.gov/recalls/recallsByVehicle?make=' + vinDict[0]['Make'] + '&model='+vinDict[0]['Model']+'&modelYear='+vinDict[0]['ModelYear']
        
        df3 = pd.DataFrame.from_dict(requests.get(url2).json()['results'])
        
        searchTerm = vinDict[0]['ModelYear'] + ' ' + vinDict[0]['Make'] + ' ' + vinDict[0]['Model']
        
        
        downloader.download(searchTerm, limit=1, adult_filter_off=True, force_replace=False, timeout=60,output_dir="static")

        picFolder = os.path.join('static', searchTerm)
        pic1 = os.path.join(picFolder, 'Image_1.jpg')
        
        return render_template('frame.html',  tables=[df.to_html(classes='data')], titles=df.columns.values,  tables1=[df2.to_html(classes='data')], titles1=df2.columns.values,  tables2=[df3.to_html(classes='data')], titles2=df3.columns.values, user_image = pic1, years = list(fullDict.keys()))
    
    return 'hi'
    
@app.route('/SearchResults', methods=['POST'])
def getsearch():
    if request.method == 'POST':
        global yearList
        global yearSelect
        global makeSelect
        modelSelect = request.form['modelSelect']
        df = pd.DataFrame()
        df['Name'] = ['Year', 'Make', 'Model']
        df['Value'] = [yearSelect, makeSelect, modelSelect]
        
        
        url2 = 'https://api.nhtsa.gov/complaints/complaintsByVehicle?make=' + makeSelect + '&model='+modelSelect+'&modelYear='+yearSelect
        df2 = pd.DataFrame.from_dict(requests.get(url2).json()['results']).head(10)
        #df2 = pd.DataFrame.from_dict(requests.get(url2).json())
        url2 = 'https://api.nhtsa.gov/recalls/recallsByVehicle?make=' + makeSelect + '&model='+modelSelect+'&modelYear='+yearSelect
        
        df3 = pd.DataFrame.from_dict(requests.get(url2).json()['results'])
        
        searchTerm = yearSelect + ' ' + makeSelect + ' ' + modelSelect
        
        
        downloader.download(searchTerm, limit=1, adult_filter_off=True, force_replace=False, timeout=60,output_dir="static")

        picFolder = os.path.join('static', searchTerm)
        pic1 = os.path.join(picFolder, 'Image_1.jpg')
        
        return render_template('frame.html',  tables=[df.to_html(classes='data')], titles=df.columns.values,  tables1=[df2.to_html(classes='data')], titles1=df2.columns.values,  tables2=[df3.to_html(classes='data')], titles2=df3.columns.values, user_image = pic1, years = list(fullDict.keys()))
    
    return 'hi'
 
app.run(host='0.0.0.0', port=5000)
