from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///mydb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

# databse schema
class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(200))
    product_type = db.Column(db.String(200))
    quantity = db.Column(db.String(200))
    warehouse = db.Column(db.String(200))

class Sale(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.String(200))
    locationid = db.Column(db.Integer, db.ForeignKey('location.id'))
    
class Location(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    location_name = db.Column(db.String(200))

class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(200))
    to_location = db.Column(db.String(200))
    from_location = db.Column(db.String(200))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)

# function to delete product
@app.route('/delete_product/<int:id>')
def delete(id):
    print(id)
    task_to_delete = Product.query.get_or_404(id)
    print(task_to_delete)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')

# function fro report
@app.route('/report/<int:id>',methods=["GET"])
def report(id):
    product_info= db.session.query(Product).filter(Product.id == id).all()
    locations = Location.query.all()
    location_info= db.session.query(Location).filter(Location.location_name != product_info[0].warehouse).all()
    movement_info= db.session.query(Product,Movement).filter(Movement.product_id == id, Product.id == id).all()
    warehouse_quant = int(product_info[0].quantity)
    final_repo=[]
    for i in locations:
        if i.location_name != product_info[0].warehouse:
            move_from= db.session.query(db.func.sum(Movement.quantity)).filter(Movement.from_location == i.location_name,  Movement.product_id == id).scalar()
            if move_from == None:
                move_from = 0
            move_to= db.session.query(db.func.sum(Movement.quantity)).filter(Movement.to_location == i.location_name,   Movement.product_id == id).scalar()
            if move_to == None:
                move_to = 0
            m = move_to - move_from
            warehouse_quant = warehouse_quant - m
            final_repo.append(m) 
    final_location=[]
    for i in location_info:
        final_location.append(i.location_name)
    res={}
    for key in final_location:
        for value in final_repo:
            res[key] = value
            final_repo.remove(value)
            break 
    return render_template('report.html',product_info=product_info,movement_info=movement_info,final_repo=final_repo,location_info=location_info,res=res,warehouse_quant=warehouse_quant)

# function to update product
@app.route('/update_product/<int:id>',methods=["GET","POST"])
def update_product(id):
    user = Product.query.get_or_404(id)
    if request.method == 'POST':
        user.id = request.form['id']
        user.product_name = request.form['product_name']
        user.product_type = request.form['product_type']
        user.quantity = request.form['quantity']
        user.warehouse = request.form['warehouse']
        db.session.commit()
        return redirect('/')
    else:
        user1s = Product.query.all()
        page ='updatehome'
        return render_template('home.html',page=page,user1s=user1s,user=user)

# function to get details
@app.route('/',methods=['GET','POST'])
def get():
    if request.method == "GET":
        user1s = Product.query.all()
        locations = Location.query.all()
        movements = db.session.query(Product, Movement).filter(Product.id == Movement.product_id ).all()
        page ='home'
        user = Product(id='',product_name='',product_type='',quantity='',warehouse='')
        return render_template('home.html',user1s=user1s,locations=locations,movements=movements,page=page,user=user)
    else:
        product_name = request.form['product_name']
        product_type = request.form['product_type']
        quantity = request.form['quantity']
        warehouse = request.form['warehouse']
        newUser1 = Product(product_name=product_name,product_type=product_type,quantity=quantity,warehouse=warehouse)
        db.session.add(newUser1)
        db.session.commit()
        return redirect('/')

# function to delete location
@app.route('/delete_location/<int:id>')
def delete_location(id):
    task_to_delete = Location.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')

# function to add location
@app.route('/add_location',methods=['POST'])
def add_location():
    location_name= request.form['location_name']
    newLocation = Location(location_name=location_name)
    db.session.add(newLocation)
    db.session.commit()
    return redirect('/')

# function to add movement
@app.route('/add_movement',methods=['POST'])
def add_movement():
    timestamp= request.form['timestamp']
    to_location= request.form['to_location']
    from_location= request.form['from_location']
    product_id= request.form['product_id']
    quantity= request.form['quantity']
    newMovement = Movement(timestamp=timestamp,to_location=to_location,from_location=from_location,product_id=product_id,quantity=quantity)
    db.session.add(newMovement)
    db.session.commit()
    return redirect('/')

# function to delete movement
@app.route('/delete_movement/<int:id>')
def delete_movement(id):
    task_to_delete = Movement.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')

@app.route('/sales', methods=['GET'])
def get_sales():
    products = Product.query.all()
    
    return render_template('sales.html',products=products)







# main
if __name__ == "__main__":
    app.run(debug=True)
