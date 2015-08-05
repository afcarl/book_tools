from app import app
from flask import render_template,request,jsonify
import pickle


@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/add_data",methods=["POST"])
def add():
    print "posted data to the server"
    name = request.form.get("name")
    email = request.form.get("email")
    try:
        datastore = pickle.load(open("datastore","rb"))
    except IOError:
        pickle.dump([],open("datastore","rb"))
        datastore = []
    datastore.append((name,email))
    pickle.dump(datastore,open("datastore","wb"))
    return "succesffuly added data"
    
@app.route("/load_data",methods=["GET"])
def load():
    return render_template("index.html",data=pickle.load(open("datastore","rb")))
