from flask import Flask, render_template, request, redirect, make_response, url_for

app = Flask(__name__)


@app.route('/')
def index():
    if request.cookies.get('name'):
        name = request.cookies.get('name')
        return render_template('hello.html', name=name)
    else:
        return render_template('index.html')


@app.post('/login/')
def login():
    name = request.form.get('name')
    email = request.form.get('email')
    response = make_response(redirect(url_for('hello', name=name)))
    response.set_cookie('name', name)
    print(name)
    return response


@app.post('/logout/')
def logout():
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('name')
    return response


@app.route('/hello/<name>')
def hello(name):
    if request.cookies.get('name'):
        if name != request.cookies.get('name'):
            return redirect((url_for('hello', name=request.cookies.get('name'))))
        return render_template('hello.html', name=name)
    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run()