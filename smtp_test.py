import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('nikhilrpatil03@gmail.com', 'kukndcmjpbdmqtsg')
print("Login successful!")
