from flask import Flask,request,render_template, redirect,session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="root"
app.config['MYSQL_DB']="restaurant"
mysql = MySQL(app)
app.secret_key = "bdmvbhfmvbfvjbvmdnfbmdfnbmbn"

@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/',methods =["GET","POST"])
def login():
    if request.method == "POST":
        email=request.form['email']
        pswd=request.form['pswd']
        cur=mysql.connection.cursor()
        cur.execute(f'select * from customer_details where email ="{email}"')
        cusData = cur.fetchall()
        print(cusData)
        if cusData:
            if cusData[0][4] == pswd:
                session['userId'] = cusData[0][0]
                session['userName'] = cusData[0][1]
                session['userEmail']=cusData[0][2]
                print(session['userId'])
                return redirect('/home')

            else:
                    print("Fail")
                    return render_template('login.html')
        else:
                print("No uSer")
        
        
    return render_template('login.html')


@app.route('/logout')
def logout():

    
    session.pop('userId') 
    session.pop('userName')
    session.pop('userEmail')
    #print(session['userId'))

        
    return render_template('login.html')

@app.route('/giveReview',methods =["GET","POST"])
def review():

    cur = mysql.connection.cursor()
    cur.execute("select * from restaurant_details")
    data = cur.fetchall()
    # return render_template('giveReview.html',data=data)

    if request.method == "POST":
        
       
        resid=request.form['restaurant']
        review = request.form['review']
        rate = request.form['rate']
        cur = mysql.connection.cursor()
        cur.execute(f'''insert into review_restaurant values("{resid}","{session['userId']}","{review}","{rate}")''')
        mysql.connection.commit()
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute("select * from restaurant_details")
        data = cur.fetchall()
    return render_template('giveReview.html',data=data)





@app.route('/foodCritic',methods=["GET","POST"])
def details():
    if request.method == "POST":
       
        name = request.form['name']
        email = request.form['email']
        pswd = request.form['pswd']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute(f'insert into customer_details(customer_name,email,phone_no,password) values("{name}","{email}","{phone}","{pswd}")')
        mysql.connection.commit()
        cur.close()
    return render_template("foodCritic.html")

@app.route('/enterResenterRestaurantDetails',methods=["GET","POST"])
def index():
    if request.method == "POST":
        restname = request.form['name']
        loc = request.form['location']
        cuisine = request.form['cuisine']
        typee = request.form['type']
        price = request.form['price']
        trry = request.form['try']
        avg=3
       # print(restname)

    
        cur=mysql.connection.cursor() #create a cursor
        cur.execute(f'insert into restaurant_details(restaurant_name,address,average_ratings,cuisine,type,price_for_two,must_try) values("{restname}","{loc}","{avg}","{cuisine}","{typee}","{price}","{trry}")')
        mysql.connection.commit()
        cur.close()
    return render_template('enterRestaurantDetails.html')
    

if __name__ == "__main__":
    app.run(debug=True, port=5000)
