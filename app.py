from flask import Flask,redirect,render_template,request
import psycopg2
app=Flask(__name__)

conn = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="Postgres",
                        port="5432")

@app.route("/")
def home():
     cursor=conn.cursor()
     cursor.execute(f"select * from expense order by id")
     row=cursor.fetchall()  
     income=history("income")
     expense=history("expense")
     return render_template("home.html",data=row, income=income,expense=expense)

def history(trans):
    cursor=conn.cursor()
    cursor.execute(f"select * from expense where transaction_type='{trans}'")
    row1=cursor.fetchall()
    trans=0
    for i in row1:
        trans+=int(i[3])
    return trans
     
    

@app.route("/addtransaction", methods=["POST"])
def task():
    data=request.form
    name=data.get("name")
    typeval=data.get("typeval")
    amount=data.get("amount")
    cursor=conn.cursor()
    cursor.execute(f"insert into expense(name,transaction_type,amount) values('{name}','{typeval}','{amount}')")
    conn.commit()
    return redirect("/")

@app.route("/delte", methods=["GET"])
def dele():
    id=request.args.get("id")
    cursor=conn.cursor()
    cursor.execute(f"delete from expense where id={id}")
    conn.commit()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)