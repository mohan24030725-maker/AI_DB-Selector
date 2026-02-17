from flask import Flask,render_template,request,redirect,session
import pickle,sqlite3

app=Flask(__name__)
app.secret_key="secret"

model=pickle.load(open("model.pkl","rb"))

def db():
    return sqlite3.connect("database.db")

@app.route("/",methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form['username']
        p=request.form['password']
        con=db()
        cur=con.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p))
        if cur.fetchone():
            session['user']=u
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard",methods=["GET","POST"])
def dashboard():
    result=""
    if request.method=="POST":
        load=int(request.form['load'])
        result=model.predict([[load]])[0]
        con=db()
        con.execute("INSERT INTO history(load,result) VALUES(?,?)",(load,result))
        con.commit()
    return render_template("dashboard.html",result=result)

@app.route("/history")
def history():
    con=db()
    data=con.execute("SELECT * FROM history").fetchall()
    return render_template("history.html",data=data)

app.run(debug=True)
