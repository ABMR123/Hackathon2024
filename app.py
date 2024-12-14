from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'i4jg4wujgerhjgreuwjgur'

tickets = []
users = {
    'user': {'password': generate_password_hash('e'), 'role': 'user'},
    'responder': {'password': generate_password_hash('e'), 'role': 'responder'},
    '2': {'password': generate_password_hash('e'), 'role': 'responder'},
    'jerry': {'password': generate_password_hash('e'), 'role': 'user'}
}

@app.route('/')
def index():
    if 'username' in session:
        if session['role'] == 'responder':
            return redirect(url_for('responder_view'))
        else:
            return redirect(url_for('user_view'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username]['password'], password):
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if username not in users:
            users[username] = {'password': generate_password_hash(password), 'role': role}
            session['username'] = username
            session['role'] = role
            return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/user_view')
def user_view():
    if 'username' not in session or session['role'] != 'user':
        return redirect(url_for('login'))
    user_tickets = [ticket for ticket in tickets if ticket['creator'] == session['username']]
    return render_template('user_view.html', tickets=user_tickets)

@app.route('/responder_view')
def responder_view():
    if 'username' not in session or session['role'] != 'responder':
        return redirect(url_for('login'))
    return render_template('responder_view.html', tickets=tickets)

@app.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    if 'username' not in session or session['role'] != 'user':
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        tickets.append({'title': title, 'description': description, 'creator': session['username'], 'response': None})
        return redirect(url_for('user_view'))
    return render_template('create_ticket.html')

@app.route('/respond_ticket/<int:ticket_id>', methods=['GET', 'POST'])
def respond_ticket(ticket_id):
    if 'username' not in session or session['role'] != 'responder':
        return redirect(url_for('login'))
    ticket = tickets[ticket_id]
    if request.method == 'POST':
        response = request.form['response']
        tickets[ticket_id]['response'] = response
        return redirect(url_for('responder_view'))
    return render_template('respond_ticket.html', ticket=ticket, ticket_id=ticket_id)

@app.route('/ticket/<int:ticket_id>')
def ticket_view(ticket_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    ticket = tickets[ticket_id]
    if session['role'] == 'user' and ticket['creator'] != session['username']:
        return redirect(url_for('user_view'))
    return render_template('ticket_view.html', ticket=ticket, ticket_id=ticket_id)

@app.route('/ticket_response/<int:ticket_id>')
def ticket_response_view(ticket_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['role'] != 'responder':
        return redirect(url_for('login'))
    ticket = tickets[ticket_id]
    return render_template('ticket_response_view.html', ticket=ticket, ticket_id=ticket_id)

if __name__ == '__main__':
    app.run(debug=True)
