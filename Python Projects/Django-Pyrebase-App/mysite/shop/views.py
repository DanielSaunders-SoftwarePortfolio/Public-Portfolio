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
    try:
        uid = request.session["uid"]
        
    except:
        uid = False
    
    print()
    print(f"uid: {uid}")
    if uid:
        user = database.child("Users").child(uid)
        userdict = {}
        for entry in user.get().each():
            key = entry.key()
            val = entry.val()
            userdict[key] = val
            
        username = userdict["Username"]
        money = userdict["Money"]
    else:
        username = ""
        money = ""
    shop = database.child("Shop").child("Aliens").get()
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
    return render(request, "shop.html", {
                                         "shop": results,
                                         "username": username,
                                         "money": money
                                        })

def logIn(request):
    return render(request, "login.html")

def signUp(request):
    return render(request, "registration.html")

def postsignUp(request):
     email = request.POST.get('email')
     passs = request.POST.get('pass')
     name = request.POST.get('name')
     error_message = "Unable to create account"
     try:
        # creating a user with the given email and password
        user=authe.create_user_with_email_and_password(email,passs)
        uid = user['localId']
        idtoken = request.session['uid']
        print(uid)
        error_message = "Unable to create Database entry"
        if not database.child("Users").child(uid).shallow().get().val():
            user_object = {
                    "Username": name,
                    "Inventory": {"Alien": 0},
                    "Money": 3500,
                    "Race": "Human"
                }
            database.child("Users").child(uid).set(user_object)
     except:
        return render(request, "Registration.html", {
                                                    "message": error_message,
                                                    "redirect": True
                                                    })
     return render(request,"Login.html", {
                                          "redirect" : True
                                         })

def postsignIn(request):
    email=request.POST.get('email')
    pasw=request.POST.get('pass')
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,pasw)
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"login.html",{
                                            "message":message,
                                            "redirect": True
                                            
                                            })
    session_id=user['localId']
    request.session['uid']=str(session_id)
    return render(request, "shop.html", {"redirect": True})

def purchase(request):
    if request.method == 'POST':
        itemName = request.POST.get('itemName')
        itemPrice = float(request.POST.get('itemPrice'))
        try:
            uid = request.session["uid"]
        except:
            uid = False
        
        print()
        print(f"uid: {uid}")
        print()
        if uid:
            user = database.child("Users").child(uid)
            userdict = {}
            for entry in user.get().each():
                key = entry.key()
                val = entry.val()
                userdict[key] = val
                
            username = userdict["Username"]
            money = float(userdict["Money"])
        else:
            username = ""
            money = ""
        
        # print(type(itemPrice))
        
        if itemPrice < money:
            # print(type(funds.get().val()))
            inv_dict = userdict["Inventory"]
            # print("\n\n", inv_dict, "\n\n")
            # print(f"Money: {money}\nPrice: {itemPrice}")
            database.child("Users").child(uid).update({"Money": (money - itemPrice)})
            
            if itemName in inv_dict:
                inv_dict[itemName] += 1
            else:
                inv_dict[itemName] = 1
            
            database.child("Users").child(uid).update({"Inventory": inv_dict})
            
        print()
        print(f"You purchased {itemName} for {itemPrice}")
        print()
        return render(request, "shop.html", {"redirect": True})
    else:
        return render(request, "shop.html", {"redirect": True})
        