import mysql.connector

class Database:
    def __init__(self):
        self.config = {
            'user': 'root',
            'password': 'root',
            'host': 'localhost',
            'database': 'rms1'
        }

    def create_connection(self):
        return mysql.connector.connect(**self.config)

    @staticmethod
    def create_table_admin():
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE Admin (
            admin_id INT PRIMARY KEY,
            admin_email VARCHAR(30),
            admin_password VARCHAR(30)
        )
        ''')
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def insert_into_admin(id, email, password):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO Admin (admin_id, admin_email, admin_password) VALUES (%s, %s, %s)",
                           (id, email, password))
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()


    @staticmethod
    def checkInAdmin(email, password):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM Admin WHERE admin_email = %s AND admin_password = %s", (email, password))
        admin = cursor.fetchone()  # Fetch a single result
        
        return admin is not None  # Returns True if an admin was found, otherwise False

    @staticmethod
    def returnAdmins():
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * from Admin")
        admins = cursor.fetchall()
        return admins

    @staticmethod
    def CreateTableCustomer():
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE Customers(
        customer_id    INT AUTO_INCREMENT PRIMARY KEY,
        phone_no       varchar (25),
        user_name      VARCHAR (30),
        first_name     VARCHAR (30),
        last_name      VARCHAR (30),
        password        VARCHAR (30),
        address        VARCHAR (100),
        email          VARCHAR (50),
        admin_id        int not null,
        FOREIGN KEY (ADMIN_ID) REFERENCES ADMIN(ADMIN_ID)
        )
        '''
                       )
        connection.commit()
        connection.close()

    @staticmethod
    def insertIntoCustomer(first_name, last_name, username, Useremail, Userpassword, phone, address):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        cursor.execute("START TRANSACTION;")
        try:
            cursor.execute('''INSERT INTO CUSTOMERS(phone_no,user_name,first_name,last_name,password,address,email,admin_id) VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s)
            ''', (phone, username, first_name, last_name, Userpassword, address, Useremail, 1))
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    # @staticmethod
    # def updateCustomerWithPayId(cus_id, pay_id):
    #     db = Database()
        connection = db.create_connection()
    #     cursor = connection.cursor()
    #     cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    #     cursor.execute(
    #         f"UPDATE Customers SET pay_id = '{pay_id}' WHERE customer_id = {cus_id}")
    #     connection.commit()
    #     connection.close()

    @ staticmethod
    def customerIdExists(id):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT COUNT(*) FROM Customers WHERE customer_id = {id}")
        customerCountList = cursor.fetchone()
        return int(''.join([str(n) for n in customerCountList])) == 1

    @staticmethod
    def deleteCustomer(id):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        cursor.execute("START TRANSACTION;")
        try:
            cursor.execute(f"DELETE FROM Customers WHERE customer_id = {id}")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @staticmethod
    def checkIfCustomerAlreadyExistForLogin(Useremail, Userpassword):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * from Customers")
        Customers = cursor.fetchall()
        for customer in Customers:
             if customer[7] == Useremail and customer[5] == Userpassword:
                return True
        return False
    
    @staticmethod
    def checkIfCustomerAlreadyExistForSignUp(Useremail, Userpassword):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * from Customers")
        Customers = cursor.fetchall()
        if Customers==None or len(Customers)==0:
            return False
        for customer in Customers:
            if (Useremail and Userpassword) in customer:
                return True
            if (Useremail) in customer:
                return True
        return False

    @staticmethod
    def returnCustomerAccordingToSession(email, password):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT * from Customers where email = '{email}' and password = '{password}'")
        customer = cursor.fetchone()
        return customer

    @staticmethod
    def returnCustomers():
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * from Customers")
            customers = cursor.fetchall()
        except:
            connection.rollback()
        return customers

    
##########################################################################################################################################

    @staticmethod
    def CreateTableServer():
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE Servers(
        server_id    INT AUTO_INCREMENT PRIMARY KEY,
        phone_no       varchar (25),
        user_name      VARCHAR (30),
        first_name     VARCHAR (30),
        last_name      VARCHAR (30),
        password        VARCHAR (30),
        address        VARCHAR (100),
        email          VARCHAR (50),
        admin_id        int not null,
        FOREIGN KEY (ADMIN_ID) REFERENCES ADMIN(ADMIN_ID)
        )
        '''
                       )
        connection.commit()
        connection.close()

    @staticmethod
    def insertIntoServer(first_name_server, last_name_server, username_server, Useremail_server, Userpassword_server, phone_server, address_server):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        cursor.execute("START TRANSACTION;")
        try:
            cursor.execute('''INSERT INTO SERVERS(phone_no,user_name,first_name,last_name,password,address,email,admin_id) VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s)
            ''', (phone_server, username_server, first_name_server, last_name_server, Userpassword_server, address_server, Useremail_server, 1))
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @ staticmethod
    def serverIdExists(id):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT COUNT(*) FROM Servers WHERE server_id = {id}")
        serverCountList = cursor.fetchone()
        return int(''.join([str(n) for n in serverCountList])) == 1

    @staticmethod
    def deleteServer(id):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        cursor.execute("START TRANSACTION;")
        try:
            cursor.execute(f"DELETE FROM Servers WHERE server_id = {id}")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @staticmethod
    def checkIfServerAlreadyExistForLogin(Useremail_server, Userpassword_server):
        print(Useremail_server)
        print(Userpassword_server)
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * from Servers")
        Servers = cursor.fetchall()
        for server in Servers:
            print(server)
            if server[7] == Useremail_server and server[5] == Userpassword_server:
                return True
        return False

    @staticmethod
    def checkIfServerAlreadyExistForSignUp(Useremail, Userpassword):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * from Servers")
        Servers = cursor.fetchall()
        print(Servers)
        for server in Servers:
            # if (Useremail and Userpassword) in server:
            #     return True
            if (Useremail) in server:
                return True
        return False

    @staticmethod
    def returnServerAccordingToSession(email, password):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT * from Servers where email = '{email}' and password = '{password}'")
        server = cursor.fetchone()
        return server

    @staticmethod
    def returnServer():
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * from Servers")
        servers = cursor.fetchall()
        return servers

    @staticmethod
    def returnAvailableOrders():
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute(f'''
        SELECT Customers.first_name, Customers.last_name, ORDERED.Order_ID, FOOD.food_title, FOOD.food_price, FOOD.food_image, ORDERED.ordered_date,
        ORDERED.quantity, ORDERED.pay_amount, Payment.pay_number, ORDERED.order_status FROM ORDERED
        INNER JOIN CUSTOMERS
        ON ORDERED.customer_id = CUSTOMERS.customer_id
        INNER JOIN PAYMENT
        ON ORDERED.pay_id = PAYMENT.pay_id
        INNER JOIN FOOD
        ON ORDERED.food_no = FOOD.food_no
        WHERE ORDERED.order_status = 'Issued' OR order_status = 'Pending'                          
        order by ORDERED.Order_ID DESC
        ''')
        orderDetails = cursor.fetchall()
        return orderDetails
    
    @staticmethod
    def returnOrderHistory(server_id):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute(f'''
        SELECT Customers.first_name, Customers.last_name, ORDERED.Order_ID, FOOD.food_title, 
        FOOD.food_price, FOOD.food_image, ORDERED.ordered_date, ORDERED.quantity, ORDERED.pay_amount, 
        Payment.pay_number, ORDERED.order_status 
        FROM ORDERED
        INNER JOIN 
        CUSTOMERS ON ORDERED.customer_id = CUSTOMERS.customer_id
        INNER JOIN 
        PAYMENT ON ORDERED.pay_id = PAYMENT.pay_id
        INNER JOIN 
        FOOD ON ORDERED.food_no = FOOD.food_no
        WHERE ORDERED.server_id = {server_id} 
        AND (ORDERED.order_status = 'Pending' OR ORDERED.order_status = 'Served')
        ORDER BY 
        ORDERED.Order_ID DESC
        ''')
        orderDetails = cursor.fetchall()
        return orderDetails
    
    @staticmethod
    def updateOrderStatusToPending(order_id):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        try:
            cursor.execute(f"UPDATE ORDERED SET order_status = 'Pending' where Order_Id = {order_id}")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @staticmethod
    def updateServerId(order_id, server_id):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        try:
            cursor.execute(f"UPDATE ORDERED SET server_id = {server_id} where Order_Id = {order_id}")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

############################################################################################################################################
    
    @staticmethod
    def CreateTableFood():
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE Food
    (
        food_no          INT AUTO_INCREMENT PRIMARY KEY ,
        food_image       VARCHAR(300) ,
        food_price       int,
        food_title       VARCHAR (100) ,
        food_description VARCHAR (500) ,
        admin_id         int NOT NULL,
        FOREIGN KEY (ADMIN_ID) REFERENCES ADMIN(ADMIN_ID)
    )

        ''')
        connection.commit()
        connection.close()
 
    @staticmethod
    def InsertIntoFood(img, price, title, desc, admin_id):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        cursor.execute("START TRANSACTION;")
        try:
            cursor.execute("INSERT INTO Food(food_image,food_price,food_title,food_description,admin_id) VALUES(%s, %s, %s, %s, %s)", (img, price, title, desc, admin_id))
            connection.commit()
        except db.Error as e:
            print(f"Error inserting food item: {e}")
            connection.rollback()
        connection.close()

    @staticmethod
    def deleteFood(id):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        cursor.execute("START TRANSACTION;")
        try:
            cursor.execute(f"DELETE FROM Food WHERE food_no = {id}")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @staticmethod
    def updateFood(id, title, price, desc, img):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        cursor.execute("START TRANSACTION;")
        try:
            cursor.execute(
                f"UPDATE FOOD SET food_title = '{title}' WHERE food_no = {id}")
            
            cursor.execute(
                f"UPDATE FOOD SET food_price = '{price}' WHERE food_no = {id}")
            
            cursor.execute(
                f"UPDATE FOOD SET food_description = '{desc}' WHERE food_no = {id}")
            
            cursor.execute(
                f"UPDATE FOOD SET food_image = '{img}' WHERE food_no = {id}")
            connection.commit()

        except:
            connection.rollback()
        connection.close()

    @ staticmethod
    def FoodsFilterBy(filter):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Food ORDER BY " + filter)
        foods = cursor.fetchall()
        return foods

    @ staticmethod
    def returnFoodById(id):
        db = Database()
        connection = db.create_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Food WHERE food_no = %s", (id,))
            food = cursor.fetchone()
        finally:
            connection.close()
        print(food)
        return food

    @ staticmethod
    def foodIdExists(id):
        db = Database()
        connection = db.create_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM Food WHERE food_no = %s", (id,))
            foodcountList = cursor.fetchone()
        finally:
            connection.close()
        print(foodcountList)
        return int(''.join([str(n) for n in foodcountList])) == 1

    @staticmethod
    def returnFoods():
        db = Database()
        connection = db.create_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Food")
            foods = cursor.fetchall()
            return foods
        finally:
            connection.close()

    @staticmethod
    def deleteAllFoods():
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        cursor.execute("START TRANSACTION;")
        try:
            cursor.execute(f"DELETE FROM Food")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @ staticmethod
    def CreateTableORDERED():
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute('''
   CREATE TABLE Ordered (
    Order_Id        INT AUTO_INCREMENT PRIMARY KEY,
    customer_id	    INT NOT NULL,
    food_no	        INT NOT NULL,
    pay_id	        INT NULL,  -- Change to NULL
    ordered_date	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quantity	    INT DEFAULT 0,
    pay_amount	    INT NOT NULL CHECK(pay_amount > 0),
    order_status    VARCHAR(10) DEFAULT 'Issued' CHECK(order_status IN ('Pending', 'Served', 'Issued')), 
    server_id        INT NULL,   
    FOREIGN KEY (pay_id) REFERENCES Payment(pay_id) ON DELETE SET NULL,
    FOREIGN KEY (food_no) REFERENCES FOOD(food_no) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (server_id) REFERENCES Servers(server_id) ON DELETE SET NULL
);

        ''')
        connection.commit()
        connection.close()


    @staticmethod
    def InsertIntoORDERED(customerId, foodno, quantity, payId, pay_amount):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        try:
            cursor.execute('''
            INSERT INTO ORDERED(customer_id,food_no,quantity,pay_id, pay_amount) VALUES
            (?, ?, ?, ?, ?)
            ''', (customerId, foodno, quantity, payId, pay_amount))
            cursor.execute("ROLLBACK TO SAVEPOINT restart_from_payment")
            connection.commit()
        except:
            cursor.execute("ROLLBACK TO SAVEPOINT restart_from_payment")
        connection.close()

    @staticmethod
    def updateOrderStatusToServed(order_id):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        try:
            cursor.execute(f"UPDATE ORDERED SET order_status = 'Served' where Order_Id = {order_id}")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @staticmethod
    def deleteOrderWithOrderId(order_id):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        try:
            cursor.execute(f"delete from ORDERED where Order_Id = {order_id}")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @staticmethod
    def returnOrderDetailsOfCustomerWithJoins(customerId):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute(f'''
        SELECT ORDERED.Order_ID, FOOD.food_title, FOOD.food_price, FOOD.food_image, ORDERED.ordered_date,
        ORDERED.quantity, ORDERED.pay_amount, Payment.pay_number, ORDERED.order_status FROM ORDERED
        INNER JOIN CUSTOMERS
        ON ORDERED.customer_id = CUSTOMERS.customer_id
        INNER JOIN PAYMENT
        ON ORDERED.pay_id = PAYMENT.pay_id
        INNER JOIN FOOD
        ON ORDERED.food_no = FOOD.food_no
        where CUSTOMERS.customer_id = '{customerId}' AND (ORDERED.order_status = 'Issued' OR ORDERED.order_status = 'Pending' 
                                                                                         OR ORDERED.order_status = 'Served')
        order by ORDERED.Order_ID DESC
        ''')
        orderDetails = cursor.fetchall()
        return orderDetails

    @staticmethod
    def returnAllOrderDetailsOfCustomerWithJoins():
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute(f'''
        SELECT Customers.first_name, Customers.last_name, ORDERED.Order_ID, FOOD.food_title, FOOD.food_price, FOOD.food_image, ORDERED.ordered_date,
        ORDERED.quantity, ORDERED.pay_amount, Payment.pay_number, ORDERED.order_status FROM ORDERED
        INNER JOIN CUSTOMERS
        ON ORDERED.customer_id = CUSTOMERS.customer_id
        INNER JOIN PAYMENT
        ON ORDERED.pay_id = PAYMENT.pay_id
        INNER JOIN FOOD
        ON ORDERED.food_no = FOOD.food_no
        order by ORDERED.Order_ID DESC
        ''')
        orderDetails = cursor.fetchall()
        return orderDetails

    @ staticmethod
    def OrderIdExists(id):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT COUNT(*) FROM Ordered WHERE Order_ID = {id}")
        OrderCountList = cursor.fetchone()
        return int(''.join([str(n) for n in OrderCountList])) == 1

    @ staticmethod
    def returnORDERED():
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * from ORDERED")
        ORDERED = cursor.fetchall()
        return ORDERED
#############################################################################################
    @ staticmethod
    def CreateTablePayment():
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE PAYMENT
    (
        pay_id                INT AUTO_INCREMENT PRIMARY KEY,
        pay_number            VARCHAR (15),
        customer_id           INT NOT NULL,
        FOREIGN KEY(customer_id) REFERENCES CUSTOMERS(customer_id) on delete cascade
    )
        ''')

        connection.commit()
        connection.close()


    @staticmethod
    def insertIntoPaymentThenOrders(number, customer_id, foodno, quantity, pay_amount):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        cursor.execute("START TRANSACTION;")

        try:
            cursor.execute(f'''
            insert into PAYMENT (pay_number, customer_id)
            select %s, %s
            where not EXISTS (SELECT 1 from PAYMENT p where (p.customer_id <> %s or p.customer_id = %s) and p.pay_number = %s)
            ''',(number,customer_id,customer_id,customer_id,number))
            cursor.execute(f'''
            SELECT 'already'
            where EXISTS (SELECT 1 from PAYMENT p where p.customer_id <> %s and p.pay_number = %s)  
            ''',(customer_id,number))
            already = cursor.fetchone()
            # connection.commit()
            # cursor2 = connection.cursor()
            cursor.execute("SELECT pay_id from payment where pay_number = %s and customer_id = %s limit 1",(number,customer_id))
            StorePay_id = cursor.fetchone()
            StoreAlready = already
            
            if StoreAlready == None:
                # cursor2 = connection.cursor()
                # cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
                cursor.execute('''
                INSERT INTO ORDERED(customer_id,food_no,quantity,pay_id, pay_amount) VALUES
                (%s, %s, %s, %s, %s)
                ''', (customer_id, foodno, quantity, StorePay_id[0], pay_amount))
                connection.commit()
            return StoreAlready, StorePay_id
            connection.commit()
        except db.Error as e:
            print(e.with_traceback)
            connection.rollback()

    @ staticmethod
    def CreateTableReviews():
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE Reviews
    (
        review_id             INT AUTO_INCREMENT PRIMARY KEY,
        review_rate           DECIMAL (2,2) NOT NULL,
        review_description    VARCHAR (500) NOT NULL,
        Order_ID              int NOT NULL UNIQUE,
        FOREIGN KEY (Order_ID) REFERENCES ORDERED(Order_ID) ON DELETE CASCADE
    )
        ''')

        connection.commit()
        connection.close()
    @staticmethod
    def InsertIntoReviews(rate, revDesc, ord_id):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        cursor.execute("START TRANSACTION;")
        try:
            cursor.execute('''
            INSERT INTO Reviews(review_rate, review_description, Order_ID) VALUES
            (%s, %s, %s)
            ''', (rate, revDesc, ord_id))
            connection.commit()
        except db.IntegrityError as error:
            print("Can't insert more reviews for 1 customer", error)
            connection.close()
            return False
        except db.Error as error:
            print("There is a problem while insertion, rolling back.", error)
            connection.rollback()
        # connection.commit()
        # lastId = cursor.lastrowid
        connection.close()
        return True
        # return lastId

    @staticmethod
    def returnAllReviewsOfFood_noWithJoins(food_no):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute(f'''
            SELECT c.first_name, c.last_name, r.review_rate, r.review_description from Reviews r
            inner join Ordered o
            on o.Order_Id = r.Order_Id
            INNER join Customers c
            on o.customer_id = c.customer_id
            inner join Food f
            on o.food_no = f.food_no
            where f.food_no = '{food_no}'
        ''')
        reviews = cursor.fetchall()
        return reviews

    @staticmethod
    def returnAllReviewsRatesAndFood_nos():
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute(f'''
            SELECT f.food_no, avg(r.review_rate), count(*) from Reviews r
            inner join Ordered o
            on o.Order_Id = r.Order_Id
            INNER join Customers c
            on o.customer_id = c.customer_id
            inner join Food f
            on o.food_no = f.food_no
            GROUP by f.food_no
        ''')
        reviews = cursor.fetchall()
        return reviews

    @staticmethod
    def returnReviewsOfFood_noWithJoins(food_id):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute(f'''
            SELECT avg(r.review_rate), count(*) from Reviews r
            inner join Ordered o
            on o.Order_Id = r.Order_Id
            INNER join Customers c
            on o.customer_id = c.customer_id
            inner join Food f
            on o.food_no = f.food_no
            GROUP by f.food_no
            having f.food_no = '{food_id}'
        ''')
        reviews = cursor.fetchone()
        return reviews

    @staticmethod
    def FoodsFilterByOrderRatings():
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT f.food_no, f.food_image, f.food_price,f.food_title, f.food_description, f.admin_id
            from Food f left join Ordered o
            on f.food_no = o.food_no
            left join Reviews r
            on r.Order_Id = o.Order_Id
            group by f.food_no
            order by avg(review_rate) desc;
        ''')
        foods = cursor.fetchall()
        return foods

    @ staticmethod
    def returnTable(table):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * from {table}")
        tableTuples = cursor.fetchall()
        return tableTuples

    @staticmethod
    def testing(number,customer_id):
        db = Database()
        connection = db.create_connection()
        cursor = connection.cursor()
        cursor.execute('''
        INSERT INTO Payment(pay_number, customer_id) VALUES
        (?, ?)
        ''', (number, customer_id))
        connection.commit()
        pay_id = cursor.execute(f"SELECT pay_id from payment where pay_number = '{number}' and customer_id = '{customer_id}'")
        cursor2 = connection.cursor()
        count = cursor2.execute("select count(*) from payment")
        return pay_id, count







        
