from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/clothes/')
def clothes():
    _clothes = [
        {
            "name": "Платье",
            "price": "1500"
        },
        {
            "name": "Джинсы",
            "price": "2000"
        },
        {
            "name": "Пальто",
            "price": "15000"
        },
    ]
    context = {'clothes': _clothes}
    return render_template('clothes.html', **context)


@app.route('/contacts/')
def contacts():
    return render_template('contacts.html')


@app.route('/shoes/')
def shoes():
    return render_template('shoes.html')


if __name__ == '__main__':
    app.run()
