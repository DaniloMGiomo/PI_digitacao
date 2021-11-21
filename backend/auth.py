from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logado com sucesso!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta, tente novamente!.', category='error')
        else:
            flash('O email não existe.', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        print(data)
        email = data['email']
        password1 = data['password1']
        password2 = data['password2']
        user = User.query.filter_by(email=email).first()
        if user:
            return ('Email ja utilizado.')
        elif len(email) < 4:
            return ('Email incorreto.')
        elif password1 != password2:
            return ('Senhas não são iguais.')
        elif len(str(password1)) < 5:
            return ('Senha precisa de pelo menos 5 caracteres.')
        else:
            new_user = User(email=email, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return('Conta criada!')
            # return redirect(url_for('views.home'))
    # return render_template("sign_up.html", user=current_user)
