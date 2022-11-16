# Contributing to Eazy Reviews
To get started  with contributing to this project please follow this guide.If  you need any help regarding this project you can contact me at Discord- cyrixninja#0157.I will also provide you with API Keys if needed.
I would love if you guys would help me to make this app a best feedback platfrom for small businesses.

# To get started you'll need to set up following

- [Python](https://www.python.org/downloads/) >= 3.5
- [Firebase](https://firebase.google.com/)
- [Visual Studio Code](https://code.visualstudio.com/) 
- [Courier Developer Account](https://www.courier.com/docs/) 
- [Cohere Developer Account](https://cohere.ai/) 
- [Git](https://git-scm.com/) 

# Folder Overview
/guide (It contains all the user guide for the consumer)

/image (It contains image data of this project)

/screenshots (It contains screenshots of this project)

/static/assets (It contains all the assets used in the website)

/template (It contains all the html files)

app.py (Main Backend of this project.You must fill up all the api keys before using it)

# How to get started

To get started you can either fork this repo or clone it
```
git clone https://github.com/cyrixninja/Eazy-Reviews.git
```

To run the project you'll need Courier API Key,Cohere NLP Key and Firebase Realtime Database to be set up.

You can get started by visiting them at  [Courier](https://www.courier.com/docs/),[Firebase](https://firebase.google.com/),[Cohere](https://cohere.ai/) 

Once you obtain the API Key you need to the following lines
### Courier API Key
Please Add the Courier API Key at line 90 and 183 in app.py 
```
  headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer pk_test_<COURIER API KEY>"
            }

```
### Firebase Database URL and Json
Please the Firebase URL and Json on line 13 and 15 in app.py
You can get started with firebase using [this](https://www.freecodecamp.org/news/how-to-get-started-with-firebase-using-python/) tutorial 
```
cred_obj = firebase_admin.credentials.Certificate("<FIREBASE JSON>")
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':"<DATABASE URL>/"
	})

```

### Cohere API Key 
Please Add the Cohere API Key at line 11 in app.py
```
co = cohere.Client('<API KEY COHERE>')
```
## How to Run
Once you're done with setting up the API Key,run the the Code using 
```
flask run
```





