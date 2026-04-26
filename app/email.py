from threading import Thread
from flask import current_app, render_template
from flask_mail import Message


def send_async_email(app, msg):
    """在背景執行寄信（正確傳入 app）"""
    with app.app_context():        # ← 使用傳入的 app
        try:
            mail = app.extensions.get('mail')
            if mail:
                mail.send(msg)
                print(f"✅ Email sent successfully to {msg.recipients[0]}")
            else:
                print("❌ Mail extension not found in app")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")


def send_email(subject, recipients, text_body, html_body):
    """發送郵件"""
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    # 正確傳入 current_app 到執行緒
    Thread(target=send_async_email, 
           args=(current_app._get_current_object(), msg)).start()


def send_password_reset_email(user):
    """寄送重設密碼郵件"""
    token = user.get_reset_password_token()
    send_email(
        subject='[ASP.NET Core Community] Reset Your Password',
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt.j2', 
                                  user=user, token=token),
        html_body=render_template('email/reset_password.html.j2', 
                                  user=user, token=token)
    )