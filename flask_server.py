from flask import Flask, render_template, request, redirect
import smtplib
import csv
from email.message import EmailMessage

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/<string:page_name>")
def show_page(page_name=None):
    return render_template(page_name)


@app.route("/submit_form", methods=["POST", "GET"])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            print("written to database")
            send_email(data)
            print("email sent")
            return render_template("index.html")  # redirect("/index.html")
        except:
            return "something went wrong while processing."
    else:
        return "must have been a GET request"


def send_email(new_data):
    email = EmailMessage()
    name = new_data["name"]
    sender_address = new_data["email"]
    subject = new_data["subject"]
    message = new_data["message"]
    email["from"] = name
    email["to"] = "davidhanson.c@gmail.com"
    email["subject"] = f"website contact form: {subject}"
    email.set_content(f"""Name: {name}\n\nEmail: {sender_address}\n\nSubject: {subject}\n\nMessage: \n{message}""")
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login("python.testing.djhd@gmail.com", "david#hanson")
        smtp.send_message(email)
    return "email sending..."


def write_to_csv(new_data):
    with open("./database.csv", "a", newline="") as database:
        name = new_data["name"]
        email = new_data["email"]
        subject = new_data["subject"]
        message = new_data["message"]
        csv_writer = csv.writer(database, delimiter=",", quotechar='"', \
                quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name, email, subject, message])
    return csv_writer


if __name__ == "__main__":
    app.run()
    # app.run(debug=True)
