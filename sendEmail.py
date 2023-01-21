import smtplib
import random
server = smtplib.SMTP('smtp.gmail.com', 587)
randomNumber = str(random.randint(1000, 9999))
print(randomNumber, type(randomNumber))
# randomnew = "OTP ", randomNumber

server.starttls()
server.login('pranavjore@gmail.com', 'bgxvrcjsvbiojylu')
server.sendmail('youcantrust@gmail.com', 'yashjosh7486@gmail.com',
                randomNumber)
print("Mail send")
