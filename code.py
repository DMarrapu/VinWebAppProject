from __future__ import print_function
import json
import pandas as pd  
import datetime
import os
import requests
import sys
from flask import Flask,render_template,request
#from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="C:\\Users\\dhanv\\Downloads\\project") 

@app.route("/")
def form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def getfile():
    if request.method == 'POST':    
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
        
        return render_template('frame.html',  tables=[df.to_html(classes='data')], titles=df.columns.values,  tables1=[df2.to_html(classes='data')], titles1=df2.columns.values)
    
    return 'hi'
 
app.run(host='0.0.0.0', port=5000)   
