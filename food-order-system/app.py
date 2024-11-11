from flask import Flask, render_template, redirect, request, url_for, session, abort
import os
from werkzeug.utils import secure_filename
from database import Database
db = Database()


def checkAppropriateFile(file):
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
    for f in ALLOWED_EXTENSIONS:
        if file.endswith(f):
            return True
    return False




app = Flask(__name__)
app.secret_key = '7457hhhyuft26442'

app.config['UPLOAD_FOLDER'] = 'static/images'


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if "Useremail" and "Userpassword" not in session:
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            username = request.form['username']
            Useremail = request.form['Useremail']
            Userpassword = request.form['Userpassword']
            phone = request.form['phone']
            address = request.form['address']

            session['first_name'] = first_name
            session['last_name'] = last_name
            session['username'] = username
            session['Useremail'] = Useremail
            session['Userpassword'] = Userpassword
            session['phone'] = phone
            session['address'] = address

            check = db.checkIfCustomerAlreadyExistForSignUp(Useremail, Userpassword)
            if not check:
                db.insertIntoCustomer(
                    first_name, last_name, username, Useremail, Userpassword, phone, address)
                return redirect(url_for('home'))
            else:
                session.pop('Useremail', None)
                session.pop('Userpassword', None)
                return render_template('signup.html', flag=True)
        else:
            return render_template('signup.html')
    return redirect(url_for('home'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if "Useremail" and "Userpassword" not in session:
        if request.method == 'POST':
            Useremail = request.form['Useremail']
            Userpassword = request.form['Userpassword']
            session["Useremail"] = Useremail
            session["Userpassword"] = Userpassword
            # we can not pass values withouot confirming that user is in the session so
            # return render_template("admin.html", email=email, password=password)
            check = db.checkIfCustomerAlreadyExistForLogin(Useremail, Userpassword)
            if (check == True):
                return redirect(url_for('home'))
            else:
                session.pop("Useremail", None)
                session.pop("Userpassword", None)
                return render_template("login.html", flag=True)
        else:
            return render_template("login.html")
    else:
        return redirect(url_for('home'))


@app.route('/')
def frontPage():
    return render_template('frontPage.html')


@app.route('/home')
def home():
    # db.create_table_admin()
    # db.CreateTableCustomer()
    # db.CreateTableFood()
    # db.CreateTableServer()
    # db.CreateTablePayment()
    # db.CreateTableORDERED()
    # db.CreateTableReviews()
    if "Useremail" and "Userpassword" in session:
        return render_template('home.html')
    return redirect(url_for('login'))


@app.route('/menu')
def menu():
    if "Useremail" and "Userpassword" in session:
        foods = db.returnFoods()
        foodnosAndRates = db.returnAllReviewsRatesAndFood_nos()
        return render_template("menu.html", foods=foods, foodnosAndRates=foodnosAndRates)
    return redirect(url_for('login'))


@app.route('/account')
def account():
    if "Useremail" and "Userpassword" in session:
        useremail = session["Useremail"]
        userpassword = session["Userpassword"]
        customer = db.returnCustomerAccordingToSession(useremail, userpassword)
        return render_template('useraccount.html', customer=customer)
    return redirect(url_for('login'))


@app.route('/menu/<filter>')
def filter(filter):
    if "Useremail" and "Userpassword" in session:
        if filter == 'filterByPrice':
            foods = db.FoodsFilterBy("food_price")
            foodnosAndRates = db.returnAllReviewsRatesAndFood_nos()     
            return render_template('menu.html', foods=foods, foodnosAndRates=foodnosAndRates)

        elif filter == 'filterByRating':
            foods = db.FoodsFilterByOrderRatings()
            foodnosAndRates = db.returnAllReviewsRatesAndFood_nos()
            return render_template('menu.html', foods=foods, foodnosAndRates=foodnosAndRates)
        return redirect(url_for('menu'))
    return redirect(url_for('login'))

@app.route('/update_orderMarked/<int:or_id>')
def markAsDone(or_id):
    if "email" and "password" in session:
        db.updateOrderStatusToServed(or_id)
        return redirect(url_for('allOrders'))
    return redirect(url_for('adminLogin'))

@app.route('/remove_order/<int:or_id>')
def removeOrder(or_id):
    if "email" and "password" in session:
        db.deleteOrderWithOrderId(or_id)
        return redirect(url_for('allOrders'))
    return redirect(url_for('adminLogin'))

@app.route('/menu/customer_orders')
def orderDetails(flag=None):
    if "Useremail" and "Userpassword" in session:
        useremail = session["Useremail"]
        userpassword = session["Userpassword"]
        customer = db.returnCustomerAccordingToSession(useremail, userpassword)
        customerId = customer[0]
        orderDetails = db.returnOrderDetailsOfCustomerWithJoins(customerId)
        getFlag = flag
        return render_template('orderDetails.html', orderDetails=orderDetails, getFlag=getFlag)
    return redirect(url_for('login'))

@app.route('/allcustomer_orders')
def allOrders():
    if "email" and "password" in session:
        orderDetails = db.returnAllOrderDetailsOfCustomerWithJoins()
        return render_template('AllorderDetails.html', orderDetails=orderDetails)
    return redirect(url_for('adminLogin'))

@app.route('/menu/<int:food_id>', methods=['POST', 'GET'])
def product(food_id):
    if "Useremail" and "Userpassword" in session:
        if request.method == 'POST':
            quantity = request.form['quantity']
            pay_number = request.form['pay_number']
            pay_amount = request.form['pay_amount']
            useremail = session["Useremail"]
            userpassword = session["Userpassword"]
            customer = db.returnCustomerAccordingToSession(useremail, userpassword)
            customerId = customer[0]

            already, pay_id = db.insertIntoPaymentThenOrders(pay_number,customerId, food_id, quantity, pay_amount)

            if already == None:
                return redirect(url_for('orderDetails', flag=False))
            elif already[0] == 'already' and pay_id == None:
                return render_template('already.html')
            # we can cancel order here so we have to delete those things
            #db.updateCustomerWithPayId(customerId, payId)
        else:
            if db.foodIdExists(food_id):
                food = db.returnFoodById(food_id)
                reviewsAndCount = db.returnReviewsOfFood_noWithJoins(food_id)
                allRevs = db.returnAllReviewsOfFood_noWithJoins(food_id)
                return render_template("productdetails.html", food=food, reviewsAndCount=reviewsAndCount, allRevs=allRevs)
            else:
                abort(404)
    return redirect(url_for('login'))

@app.route('/admin/login', methods=['POST', 'GET'])
def adminLogin():
    if "email" and "password" not in session:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            session["email"] = email
            session["password"] = password
            # we can not pass values withouot confirming that user is in the session so
            # return render_template("admin.html", email=email, password=password)
            check = db.checkInAdmin(email, password)
            if (check == True):
                return redirect(url_for('admin'))
            else:
                session.pop("email", None)
                session.pop("password", None)
                return render_template("adminLogin.html", flag=True)
        else:
            return render_template("adminLogin.html")
    else:
        return redirect(url_for('admin'))


@app.route('/admin/home')
def admin():
    if "email" and "password" in session:
        foods = db.returnFoods()
        foodnosAndRates = db.returnAllReviewsRatesAndFood_nos()
        return render_template('admin.html', foods=foods, foodnosAndRates=foodnosAndRates)
    return redirect(url_for('adminLogin'))


@app.route('/addfood', methods=['POST', 'GET'])
def addFood():
    if "email" and "password" in session:
        if request.method == 'POST':
            foodTitle = request.form['foodTitle']
            foodPrice = request.form['foodPrice']
            foodDesc = request.form['food_desc']
            imageFile = request.files['imageFile']

            if imageFile.filename == '':
                return redirect(request.url)
            if imageFile and checkAppropriateFile(imageFile.filename):
                Securefilename = secure_filename(imageFile.filename)
                imageFile.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], Securefilename))
                db.InsertIntoFood(Securefilename,
                                  foodPrice, foodTitle, foodDesc, 1)
            return redirect(url_for('admin'))
        else:
            return render_template('addFood.html')
    return redirect(url_for("adminLogin"))


@app.route('/delete/<int:id>')
def delFood(id):
    if "email" and "password" in session:
        if db.foodIdExists(id):
            db.deleteFood(id)
            return redirect(url_for('admin'))
        else:
            abort(404)
    return redirect(url_for("adminLogin"))

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def editFood(id):
    if "email" and "password" in session:
        if db.foodIdExists(id):
            if request.method == 'POST':
                foodTitle = request.form['foodTitle']
                foodPrice = request.form['foodPrice']
                foodDesc = request.form['food_desc']
                imageFile = request.files['imageFile']
                if imageFile.filename == '':
                    return redirect(request.url)
                if imageFile and checkAppropriateFile(imageFile.filename):
                    Securefilename = secure_filename(imageFile.filename)
                    imageFile.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], Securefilename))
                db.updateFood(id, foodTitle, foodPrice, foodDesc, Securefilename)
                return redirect(url_for('admin'))

            food = db.returnFoodById(id)
            return render_template('updateFood.html', food=food)
        else:
            abort(404)
    return redirect(url_for("adminLogin"))

@app.route('/deleteall')
def deleteAll():
    if "email" and "password" in session:
        db.deleteAllFoods()
        return redirect(url_for('admin'))
    return redirect(url_for("adminLogin"))

@app.route('/allCustomers')
def allCustomers():
    if "email" and "password" in session:
        customers = db.returnCustomers()
        return render_template('userdetails.html', customers=customers)
    return redirect(url_for("adminLogin"))

@app.route('/allServers')
def allServers():
    if "email" and "password" in session:
        print("entered all servers")
        servers = db.returnServer()
        return render_template('serverdetails.html', servers= servers)
    return redirect(url_for("adminLogin"))

@app.route('/delServer/<int:id>')
def delServer(id):
    print("reached route del server")
    if "email" and "password" in session:
        if db.serverIdExists(id):
            print("server id exists")
            db.deleteServer(id)
            return redirect(url_for('allServers'))
        else:
            abort(404)
    return redirect(url_for("adminLogin"))

@app.route('/delCustomer/<int:id>')
def delCustomer(id):
    if "email" and "password" in session:
        if db.customerIdExists(id):
            db.deleteCustomer(id)
            return redirect(url_for('allCustomers'))
        else:
            abort(404)
    return redirect(url_for("adminLogin"))

@app.route('/review/<int:order_id>', methods=['POST', 'GET'])
def Review(order_id):
    if "Useremail" and "Userpassword" in session:
        if db.OrderIdExists(order_id):
            if request.method == 'POST':
                review_rate = request.form['review_rate']
                review_desc = request.form['review_desc']

                uflag = db.InsertIntoReviews(review_rate, review_desc, order_id)
                if(uflag==True):
                    return redirect(url_for('orderDetails'))
                else:
                    return render_template('reviewForm.html', order_id = order_id, flag= True)
            else:
                return render_template('reviewForm.html', order_id = order_id)
        else:
            abort(404)
    return redirect(url_for("login"))

@app.route('/menufor_review')
def reviewMenu():
    if "email" and "password" in session:
        foods = db.returnFoods()
        return render_template('menuForReview.html', foods=foods)
    return redirect(url_for("adminLogin"))

@app.route('/allreviews/<int:food_no>')
def allReviews(food_no):
    if "email" and "password" in session:
        allreviews = db.returnAllReviewsOfFood_noWithJoins(food_no)
        reviewsAndCount = db.returnReviewsOfFood_noWithJoins(food_no)
        return render_template('allReviews.html', allreviews=allreviews, reviewsAndCount=reviewsAndCount)
    return redirect(url_for("adminLogin"))

@app.route('/logout')
def userLogout():
    if "Useremail" and "Userpassword" in session:
        session.pop('Useremail', None)
        session.pop('Userpassword', None)
        return redirect(url_for('frontPage'))
    return redirect(url_for("frontPage"))

@app.route('/admin/logout')
def adminLogout():
    if "email" and "password" in session:
        session.pop('email', None)
        session.pop('password', None)
        return redirect(url_for('frontPage'))
    return redirect(url_for("frontPage"))


#############################################################################################################################################

@app.route('/server/login', methods=['POST', 'GET'])
def serverLogin():
    session.pop('Serveremail', None)
    session.pop('Serverpassword', None)
    if "Serveremail" and "Serverpassword" not in session:
        if request.method == 'POST':
            Useremail_server = request.form['Serveremail']
            Userpassword_server = request.form['Serverpassword']
            session["Serveremail"] = Useremail_server
            session["Serverpassword"] = Userpassword_server
            print(Useremail_server)
            print(Userpassword_server)
            # we can not pass values withouot confirming that user is in the session so
            # return render_template("admin.html", email=email, password=password)
            check = db.checkIfServerAlreadyExistForLogin(Useremail_server, Userpassword_server)
            if (check == True):
                return redirect(url_for('serverHome'))
            else:
                session.pop("Serveremail", None)
                session.pop("Serverpassword", None)
                return render_template("serverLogin.html", flag=True)
        else:
            return render_template("serverLogin.html")
    else:
        return redirect(url_for('frontPage'))
    
@app.route('/server/signup', methods=['POST', 'GET'])
def serverSignup():
    if "Serveremail" and "Serverpassword" not in session:
        if request.method == 'POST':
            first_name_server = request.form['first_name_server']
            last_name_server = request.form['last_name_server']
            username_server = request.form['username_server']
            Useremail_server = request.form['Serveremail']
            Userpassword_server = request.form['Serverpassword']
            phone_server = request.form['phone_server']
            address_server = request.form['address_server']

            session['first_name_server'] = first_name_server
            session['last_name_server'] = last_name_server
            session['username_server'] = username_server
            session['Serveremail'] = Useremail_server
            session['Serverpassword'] = Userpassword_server
            session['phone_server'] = phone_server
            session['address_server'] = address_server

            check = db.checkIfServerAlreadyExistForSignUp(Useremail_server, Userpassword_server)
            if not check:
                db.insertIntoServer(
                    first_name_server, last_name_server, username_server, Useremail_server, Userpassword_server, phone_server, address_server)
                return redirect(url_for('serverHome'))
            else:
                session.pop('Serveremail', None)
                session.pop('Serverpassword', None)
                return render_template('serverSignup.html', flag=True)
        else:
            return render_template('serverSignup.html')
    return redirect(url_for('serverHome'))

@app.route('/server/home')
def serverHome():
    if "Serveremail" and "Serverpassword" in session:
        return render_template('serverHome.html')
    return redirect(url_for('serverLogin'))

@app.route('/server/available_orders')
def availableOrders():
    if "Serveremail" and "Serverpassword" in session:
        orderDetails = db.returnAvailableOrders()
        if orderDetails == []: 
            return render_template('noIssued.html')
        else:
            return render_template('availableOrders.html', orderDetails=orderDetails)
    return redirect(url_for('serverLogin'))

@app.route('/server/history')
def serverHistory():
    if "Serveremail" and "Serverpassword" in session:
        useremail = session["Serveremail"]
        userpassword = session["Serverpassword"]
        server = db.returnServerAccordingToSession(useremail, userpassword)
        server_id = server[0]
        orderDetails = db.returnOrderHistory(server_id)
        return render_template('serverHistory.html', orderDetails=orderDetails)
    return redirect(url_for('serverLogin'))

@app.route('/server/account')
def serverAccount():
    if "Serveremail" and "Serverpassword" in session:
        useremail = session["Serveremail"]
        userpassword = session["Serverpassword"]
        print(useremail)
        print(userpassword)
        server = db.returnServerAccordingToSession(useremail, userpassword)
        return render_template('serverAccount.html', server=server)
    return redirect(url_for('serverLogin'))

@app.route('/server/logout')
def serverLogout():
    if "Serveremail" and "Serverpassword" in session:
        session.pop('Serveremail', None)
        session.pop('Serverpassword', None)
        return redirect(url_for('frontPage'))
    return redirect(url_for("frontPage"))

@app.route('/choose_orderMarked/<int:or_id>')
def chooseOrderAsPending(or_id):
    if "Serveremail" and "Serverpassword" in session:
        Serveremail = session["Serveremail"]
        Serverpassword = session["Serverpassword"]
        server = db.returnServerAccordingToSession(Serveremail, Serverpassword)
        db.updateOrderStatusToPending(or_id)
        db.updateServerId(or_id, server[0])
        return redirect(url_for('availableOrders'))
    return redirect(url_for('serverLogin'))

@app.route('/update_orderMarked_Server/<int:or_id>')
def markAsDoneServer(or_id):
    if "Serveremail" and "Serverpassword" in session:
        db.updateOrderStatusToServed(or_id)
        return redirect(url_for('serverHistory'))
    return redirect(url_for('serverLogin'))

#############################################################################################################################################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)