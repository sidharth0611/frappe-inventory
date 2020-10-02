from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///mydb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
class User1(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(200))
    product_type = db.Column(db.String(200))
    quantity = db.Column(db.String(200))
    warehouse = db.Column(db.String(200))
    movements = db.relationship('Movement', backref="user2")
    
    
    

class Location(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    location_name = db.Column(db.String(200))


class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(200))
    to_location = db.Column(db.String(200))
    from_location = db.Column(db.String(200))
    product_id = db.Column(db.Integer, db.ForeignKey('user1.id'))
    quantity = db.Column(db.Integer)
    
@app.route('/delete_product/<int:id>')
def delete(id):
    print(id)
    task_to_delete = User1.query.get_or_404(id)
    print(task_to_delete)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')

@app.route('/report/<int:id>',methods=["GET"])
def report(id):
    abc= db.session.query(User1).filter(User1.id == id).all()
    xyz= db.session.query(User1,Movement).filter(Movement.product_id == id, User1.id == id).all()
    ghi= db.session.query(db.func.sum(Movement.quantity)/2).filter(Movement.from_location == User1.warehouse, Movement.product_id == id).scalar()
    print(ghi)
    return render_template('report.html',xyz=xyz,abc=abc)

@app.route('/update_product/<int:id>',methods=["GET","POST"])
def update_product(id):
    user = User1.query.get_or_404(id)
    if request.method == 'POST':
        user.id = request.form['id']
        user.product_name = request.form['product_name']
        user.product_type = request.form['product_type']
        user.quantity = request.form['quantity']
        user.warehouse = request.form['warehouse']
        db.session.commit()
        return redirect('/')
    else:
        user1s = User1.query.all()
        page ='updatehome'
        return render_template('home.html',page=page,user1s=user1s,user=user)
@app.route('/',methods=['GET','POST'])
def get():
    if request.method == "GET":
        user1s = User1.query.all()
        locations = Location.query.all()
        movements = db.session.query(User1, Movement).filter(User1.id == Movement.product_id ).all()
        page ='home'
        user = User1(id='',product_name='',product_type='',quantity='',warehouse='')
        return render_template('home.html',user1s=user1s,locations=locations,movements=movements,page=page,user=user)
    else:
        product_name = request.form['product_name']
        product_type = request.form['product_type']
        quantity = request.form['quantity']
        warehouse = request.form['warehouse']
        newUser1 = User1(product_name=product_name,product_type=product_type,quantity=quantity,warehouse=warehouse)
        db.session.add(newUser1)
        db.session.commit()
        return redirect('/')

@app.route('/delete_location/<int:id>')
def delete_location(id):
    task_to_delete = Location.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')


@app.route('/add_location',methods=['POST'])
def add_location():
    location_name= request.form['location_name']
    newLocation = Location(location_name=location_name)
    db.session.add(newLocation)
    db.session.commit()
    return redirect('/')

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

@app.route('/delete_movement/<int:id>')
def delete_movement(id):
    task_to_delete = Movement.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')




if __name__ == "__main__":
    app.run(debug=True)
