from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from Project import db
from Project.models import User
from Project.users.forms import UpdateUserForm, ChangePassword
from Project.core.forms import ContactForm
import time

users=Blueprint('users',__name__)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))

@users.route("/account", methods=['GET','POST'])
@login_required
def account():
    form=UpdateUserForm()
    form4=ContactForm()
    form2=ChangePassword()
    if form.submit.data and form.validate():
        current_user.username=form.username.data
        current_user.email=form.email.data
        # current_user.password_hash=generate_password_hash(form.password.data)
        current_user.investment_pref1=form.invpref1.data
        current_user.investment_pref2=form.invpref2.data
        current_user.deposit_pref=form.depopref.data
        # current_user.donation_pref1=form.donpref1.data
        # current_user.donation_pref2=form.donpref2.data
        db.session.commit()
        flash('User account Updated')
        return redirect(url_for('users.account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    
    if form4.submit4.data and form4.validate():
        return redirect(url_for('users.account'))
    
    if form2.submit2.data and form2.validate():
        current_user.password_hash=generate_password_hash(form2.password.data)
        db.session.commit()
        return redirect(url_for('users.logout'))

    return render_template('account.html', form=form, form4=form4, form2=form2)