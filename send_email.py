

import smtplib
import email.message
import os

from pathlib import Path
from dotenv import load_dotenv


current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)


EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

#####


def send_email(recipient, list_of_stocks):
    # HTML content for the email body with Lorem Ipsum text
    email_body = """
    <html>
        <head>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    margin: 20px;
                }
                h1 {
                    color: #007BFF;
                }
                p {
                    line-height: 1.6;
                }
            </style>
        </head>
        <body>
             <h1>É HORA DE INVESTIR</h1>
            <p>Olá! Percebi que existem algumas ações que estão nos preços-alvo que você definiu. Confira!</p>
            <ul>
        """
    for stock in list_of_stocks:
        email_body += f"<li>Stock Name: <b>{stock.name}</b>  - Target Price: <b>R$ {stock.target_price}</b>  - Real Time Price: <b>R$ {stock.real_time_price}</b> </li>"

    email_body += """
        </ul>
    <p>Atenciosamente,</p>

    <p>Pedro Nogueira</p>
    
        </body>
    </html>
    
    """

    # Create an Email Message object
    msg = email.message.Message()
    msg['Subject'] = f"🤑 É HORA DE INVESTIR!!! {recipient.upper()}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECIPIENT

    password = EMAIL_PASSWORD

    # Set the content type to HTML
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(email_body)

    # Connect to Gmail's SMTP server
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    try:
        # Login and send the email
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Email sent successfully')
    except Exception as e:
        print(f'Error sending email: {e}')
    finally:
        # Close the connection
        s.quit()


if __name__ == '__main__':
    # Call the function to send the email
    # send_email()
    pass
