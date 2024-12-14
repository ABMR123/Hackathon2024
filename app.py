from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tickets = []

@app.route('/')
def index():
    return render_template('index.html', tickets=tickets)

@app.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        tickets.append({'title': title, 'description': description})
        return redirect(url_for('index'))
    return render_template('create_ticket.html')

if __name__ == '__main__':
    app.run(debug=True)
