from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metadata.db'
db = SQLAlchemy(app)


class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50))
    department = db.Column(db.String(50))
    category = db.Column(db.String(50))
    subcategory = db.Column(db.String(50))


class SKUData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.Integer)
    name = db.Column(db.String(50))
    location = db.Column(db.String(50))
    department = db.Column(db.String(50))
    category = db.Column(db.String(50))
    subcategory = db.Column(db.String(50))

# Create the database tables before running the app
with app.app_context():
    db.create_all()


# Route to update metadata
@app.route('/api/v1/update_metadata', methods=['POST'])
def update_metadata():
    with app.app_context():
        data = request.get_json()
        print("data",data)

        # Assuming the metadata is provided in the request body as a list of dictionaries
        metadata_list = data.get('metadata', [])

        # Clear existing metadata
        Metadata.query.delete()
        db.session.commit()

        # Insert new metadata
        for item in metadata_list:
            new_metadata = Metadata(
                location=item['Location'],
                department=item['Department'],
                category=item['Category'],
                subcategory=item['SubCategory']
            )
            db.session.add(new_metadata)

        db.session.commit()

        return jsonify({'message': 'Metadata updated successfully'}), 200

# Route to update SKU data
@app.route('/api/v1/update_sku_data', methods=['POST'])
def update_sku_data():
    with app.app_context():
        data = request.get_json()

        # Assuming the SKU data is provided in the request body as a list of dictionaries
        sku_data_list = data.get('sku_data', [])

        # Clear existing SKU data
        SKUData.query.delete()
        db.session.commit()

        # Insert new SKU data
        for item in sku_data_list:
            new_sku_data = SKUData(
                sku=item['SKU'],
                name=item['NAME'],
                location=item['LOCATION'],
                department=item['DEPARTMENT'],
                category=item['CATEGORY'],
                subcategory=item['SUBCATEGORY']
            )
            db.session.add(new_sku_data)

        db.session.commit()

        return jsonify({'message': 'SKU data updated successfully'}), 200

@app.route('/api/v1/location', methods=['GET', 'POST'])
def location():
    with app.app_context():
        if request.method == 'GET':
            locations = Metadata.query.distinct(Metadata.location).all()
            return jsonify([location.location for location in locations])

        if request.method == 'POST':
            data = request.get_json()
            new_location = Metadata(location=data['location'])
            db.session.add(new_location)
            db.session.commit()
            return jsonify({'message': 'Location added'}), 201


@app.route('/api/v1/location/<location_id>/department', methods=['GET', 'POST'])
def department(location_id):
    with app.app_context():
        if request.method == 'GET':
            departments = Metadata.query.filter_by(location=location_id).distinct(Metadata.department).all()
            return jsonify([department.department for department in departments])
    
        if request.method == 'POST':
                data = request.get_json()
                new_department = Metadata(location=data['location'], department=data['department'])
                db.session.add(new_department)
                db.session.commit()
                return jsonify({'message': 'Department added'}), 201
            
        if request.method == 'PUT':
            data = request.get_json()
            department_to_update = Metadata.query.filter_by(location=data['location'], department=data['department']).first()
            if department_to_update:
                department_to_update.category = data.get('category', department_to_update.category)
                department_to_update.subcategory = data.get('subcategory', department_to_update.subcategory)
                db.session.commit()
                return jsonify({'message': 'Department updated'}), 200
            else:
                return jsonify({'message': 'Department not found'}), 404

        if request.method == 'DELETE':
            data = request.get_json()
            department_to_delete = Metadata.query.filter_by(location=data['location'], department=data['department']).first()
            if department_to_delete:
                db.session.delete(department_to_delete)
                db.session.commit()
                return jsonify({'message': 'Department deleted'}), 200
            else:
                return jsonify({'message': 'Department not found'}), 404
            
# Routes for Category
@app.route('/api/v1/category', methods=['GET', 'POST'])
def category():
    if request.method == 'GET':
        categories = Metadata.query.distinct(Metadata.category).all()
        return jsonify([category.category for category in categories])

    if request.method == 'POST':
        data = request.get_json()
        new_category = Metadata(location=data['location'], department=data['department'], category=data['category'])
        db.session.add(new_category)
        db.session.commit()
        return jsonify({'message': 'Category added'}), 201


# Routes for Subcategory
@app.route('/api/v1/subcategory', methods=['GET', 'POST'])
def subcategory():
    if request.method == 'GET':
        subcategories = Metadata.query.distinct(Metadata.subcategory).all()
        return jsonify([subcategory.subcategory for subcategory in subcategories])

    if request.method == 'POST':
        data = request.get_json()
        new_subcategory = Metadata(
            location=data['location'],
            department=data['department'],
            category=data['category'],
            subcategory=data['subcategory']
        )
        db.session.add(new_subcategory)
        db.session.commit()
        return jsonify({'message': 'Subcategory added'}), 201


# Similar routes can be added for category and subcategory

@app.route('/api/v1/sku', methods=['POST'])
def get_sku():
    with app.app_context():
        input_data = request.get_json()
        skus = SKUData.query.filter_by(
            location=input_data['Location'],
            department=input_data['Department'],
            category=input_data['Category'],
            subcategory=input_data['SubCategory']
        ).all()
        return jsonify([sku.sku for sku in skus])


if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)
