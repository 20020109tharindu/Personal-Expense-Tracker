from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for expenses
expenses = []


@app.route('/')
def index():
    return render_template('index.html', expenses=expenses)


@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = float(request.form['amount'])
        description = request.form['description']
        expenses.append({
            'date': date,
            'category': category,
            'amount': amount,
            'description': description
        })
        return redirect(url_for('index'))
    return render_template('add_expense.html')


if __name__ == '__main__':
    app.run(debug=True)
