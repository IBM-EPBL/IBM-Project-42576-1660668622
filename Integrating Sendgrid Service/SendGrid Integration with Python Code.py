# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# from_address we pass to our Mail object, edit with your name
FROM_EMAIL = 'Your_Name@SendGridTest.com'


def SendEmail(to_email_id):
    """ Send an email to the provided email addresses

    :param to_email_id = email to be sent to
    :returns API response code
    :raises Exception e: raises an exception """
    message = Mail(
        from_email_id=FROM_EMAIL,
        to_email_id=to_email_id,
        subject='A Test from SendGrid!',
        html_content='<strong>Hello there from SendGrid your URL is: ' +
        '<a href=''https://github.com/cyberjive''>right here!</a></strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print(f"Response Code: {code} ")
        print(f"Response Body: {body} ")
        print(f"Response Headers: {headers} ")
        print("Message Sent!")
    except Exception as exp:
        print("Error: {0}".format(exp))
    return str(response.status_code)


if __name__ == "__main__":
    SendEmail(to_email_id=input("Email address to send to? "))
