# frappe-inventory

This project is done using Flask, Flask-sqlalchemy, SQLite
db.engine.execute('select user1.id, user1.firstname, user1.email, movement.timestamp, movement.to_location, movement.from_location, movement.product_id from user1 inner join movement on user1.id = movement.product_id')