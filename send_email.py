#!/usr/bin/env python
# coding: utf-8

import smtplib
import email.message


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
            <h1>IT'S TIME TO INVEST</h1>
            <p>Hey I noticed that are some stocks that are on your target prices, check it out !!!</p>
            <ul>
        """
    for stock in list_of_stocks:
        email_body += f"<li>Stock Name: <b>{stock.name}</b>  - Target Price: <b>R$ {stock.target_price}</b>  - Real Time Price: <b>R$ {stock.real_time_price}</b> </li>"

    email_body += """
        </ul>
    <p>Best regards,</p>
    
    <p>Pedro Nogueira</p>
    
        </body>
    </html>
    
    """

    # Create an Email Message object
    msg = email.message.Message()
    msg['Subject'] = f"🤑 IT'S TIME TO INVEST {recipient.upper()}"
    msg['From'] = 'XXXXXXXXXXXXXX'
    msg['To'] = 'XXXXXXXXXXXXXXX'
    password = 'XXXXXXXXXXXXXXX'

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
