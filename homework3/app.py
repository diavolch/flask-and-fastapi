from flask import Flask, render_template, request
from models import db, Users
from forms import RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = b'0be635e2c84d438ff67e2e9a093805d1bdb097fd468aa5e3d5f0cfb35aeffe0b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    firstname = form.firstname.data
    lastname = form.lastname.data
    email = form.email.data
    password_hash = generate_password_hash(str(form.password.data))

    if request.method == 'POST' and form.validate():
        if Users.query.filter(Users.email == email).all():
            context = {'alert_message': "Пользователь существует!"}
            return render_template('registration.html', form=form, **context)

        else:
            context = {'alert_message': "Регистрация успешна!"}
            new_user = Users(firstname=firstname, lastname=lastname, email=email, password=password_hash)
            db.session.add(new_user)
            db.session.commit()
            return render_template('registration.html', form=form, **context)
    return render_template('registration.html', form=form)




if __name__ == '__main__':
    app.run()
