from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from Project import db, mail
from Project.models import User
from Project.users.forms import UpdateUserForm, ChangePassword
from Project.core.forms import ContactForm
import time
from flask_mail import Mail, Message

users=Blueprint('users',__name__)



def contact_mail(name,email, message):
    global mail
    msg=Message('Thank you for contacting us!',recipients=[email])
    msg.html='''<div class="body_changes" style="color: white; background-color: #000000; background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover; width:750px; margin-right: auto; margin-left: auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;" >

        <div style="margin-right: 20px;margin-left: 20px;">
            <br>
            <img src="https://i.ibb.co/2qG2YCw/fin-Nourish.png%22" style="width:400px;display: block; margin-left: auto; margin-right: auto;" align="center;" alt="finNourish-Logo" border="0">
            
            <p style="font-size: 130%;color: #14bf98;">
                <b>Dear {},</b>
            </p>
            <p style="font-size: 130%;text-align: justify;color: white;">
                Thank you for reaching out to <span style="color: #14bf98"><b>finNourish!</b></span> Somebody from our team will contact you soon to better serve you and address your query.
                
            </p>
            <p style="font-size: 130%;color: #14bf98;">
                <b>
                    Regards,<br>
                    Team finNourish
                </b>

            </p>
            
            <p>
                <a href="https://fin-nourish.herokuapp.com/" target="_blank"><button type="button" style="  border: none;
                    color: white;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 15px;
                   
                    cursor: pointer;
                    background-color: #14bf98;"><b>Visit Website</b></button></a>
    
            </p>

            
            <br>

            
        

        </div>

    </div>'''.format(name)
    
    mail.send(msg)
    msg2=Message('New Contact Enquiry',recipients=['finnourish@gmail.com'])
    msg2.body='Name of Applicant: {}\n\nEmail ID: {}\n\nMessage: {}'.format(name,email,message)
    mail.send(msg2)

# def admin_mail(name, email, message):
#     global mail
    
#     msg2=Message('New Contact Enquiry',recipients=['finnourish@gmail.com'])
#     msg2.body='Name of Applicant: {}\n\nEmail ID: {}\n\nMessage: {}'.format(name,email,message)
#     mail.send(msg2)

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
        contact_mail(form4.name.data, form4.email.data, form4.message.data)
        # admin_mail(form4.name.data, form4.email.data, form4.message.data)
        return redirect(url_for('users.account'))
    
    if form2.submit2.data and form2.validate():
        current_user.password_hash=generate_password_hash(form2.password.data)
        db.session.commit()
        return redirect(url_for('users.logout'))

    return render_template('account.html', form=form, form4=form4, form2=form2)