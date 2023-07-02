from django.shortcuts import render
from django.http import HttpResponse
import pyrebase

# Firebase configuration
config = {
  "apiKey": "AIzaSyCt7BynQ1_6JT_25CqENOxrTyLWCu5AhZU",
  "authDomain": "pollappfromtutorial1.firebaseapp.com",
  "projectId": "pollappfromtutorial1",
  "storageBucket": "pollappfromtutorial1.appspot.com",
  "messagingSenderId": "793892573179",
  "appId": "1:793892573179:web:0aa6023658fcac1c01855e",
  "measurementId": "G-WT3G8YNZ0Q",
  "databaseURL": "https://pollappfromtutorial1-default-rtdb.firebaseio.com"
}

firebase = pyrebase.initialize_app(config)
authe    = firebase.auth()
database = firebase.database()

def index(request):
    name = database.child("Data").child("Name").get().val()
    stack = database.child('Data').child('Stack').get().val()
    framework = database.child('Data').child('Framework').get().val()

    context = {
        'name':name,
        'stack':stack,
        'framework':framework
    }
    
    return render(request, 'index.html', context)

def shop(request):
    shop = database.child("Shop").child("All-Aliens").get()
    results = []
    for alien in shop.each():
        
        details = alien.val()
        stats = ""
        for key, val in details["Stats"].items():
            stats += f"<strong>{key[:3]}:</strong> {val} <br>"
        results.append({
            "alien":  alien.key(),
            "race":  details['Race'],
            "price": details['Price'],
            "stats": stats
        })
    return render(request, "shop.html", {"data": results})
    