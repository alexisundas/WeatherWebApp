import requests
from flask import Flask, render_template , request , flash ,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['DEBUG']


def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=5a4a56af87f3783c549a967db80da961"
    r = requests.get(url.format(city)).json()
    return r

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        err_msg = ''
        city = request.form.get('city')
        r = get_weather_data(city)
        print(r)
        if r['cod'] == 200:
            weather = {
            'city': city,
            'temperature': round(r['main']['temp']), 
            'wind': r['wind']['speed'], 
            'clouds': r['clouds']['all'], 
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            }
            return render_template('index.html',weather=weather)
        else:
            flash('City not found','error')
            return redirect(url_for('index'))
        
    else:
        r = get_weather_data('London')
    
        weather = {
            'city': 'London',
            'temperature': round(r['main']['temp']), 
            'wind': r['wind']['speed'], 
            'clouds': r['clouds']['all'], 
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        return render_template('index.html',weather=weather)

    


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run()
    