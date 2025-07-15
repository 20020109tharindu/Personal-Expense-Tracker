from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    # <-- Add this line    @app.route('/api/expenses', methods=['POST'])
    category = db.Column(db.String(50), nullable=False)

    def add_expense():
        data = request.get_json()
        new_expense = Expense(
            description=data['description'],
            category=data['category'],  # <-- Add this line
            amount=float(data['amount'])
        )
        db.session.add(new_expense)
        db.session.commit()
        return jsonify({
            'id': new_expense.id,
            'description': new_expense.description,
            'category': new_expense.category,  # <-- Add this line
            'amount': new_expense.amount,
            'date': new_expense.date.strftime('%Y-%m-%d')
        }), 201
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return jsonify([{
        'id': expense.id,
        'description': expense.description,
        'category': expense.category,
        'amount': expense.amount,
        'date': expense.date.strftime('%Y-%m-%d')
    } for expense in expenses])    


@app.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    new_expense = Expense(
        description=data['description'],
        category=data['category'],
        amount=float(data['amount'])
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({
        'id': new_expense.id,
        'description': new_expense.description,
        'amount': new_expense.amount,
        'category': new_expense.category,
        'date': new_expense.date.strftime('%Y-%m-%d')
    }), 201


@app.route('/api/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
