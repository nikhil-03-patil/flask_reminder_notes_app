import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your_mail_id', 'your_mail_id_app_password')
print("Login successful!")
