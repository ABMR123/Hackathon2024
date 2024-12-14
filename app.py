from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

tickets = []
users = {
    'user': {'password': 'password', 'role': 'user'},
    'responder': {'password': 'password', 'role': 'responder'}
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
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('index'))

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
        tickets.append({'title': title, 'description': description, 'creator': session['username']})
        return redirect(url_for('user_view'))
    return render_template('create_ticket.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'username' not in session or session['role'] != 'responder':
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        new_role = request.form['new_role']
        if new_username not in users:
            users[new_username] = {'password': new_password, 'role': new_role}
            return redirect(url_for('responder_view'))
    return render_template('add_user.html')

if __name__ == '__main__':
    app.run(debug=True)
