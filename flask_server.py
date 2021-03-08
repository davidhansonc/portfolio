from flask import Flask, render_template, request, redirect
import requests
import os
# from email.message import EmailMessage

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("index.html")


# @app.route("/<string:page_name>")
# def show_page(page_name=None):
#     return render_template(page_name)


@app.route("/", methods=["POST", "GET"])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            # write_to_csv(data)
            print("about to send email..")
            send_email(data)
            print("sending...")
            return render_template("index.html")  # redirect("/index.html")
        except:
            return "something IS wrong."
    else:
        return "must have been a GET request"


def send_email(new_data):
    name = new_data["name"]
    inquiree_address = new_data["email"]
    subject = new_data["subject"]
    message = new_data["message"]

    api_key = os.environ["MAILGUN_API_KEY"]
    domain_name = os.environ["MAILGUN_DOMAIN"]

    return requests.post(
            f"https://api.mailgun.net/v3/{domain_name}/messages",
            auth=("api", api_key),
            data={"from": f"{name} <{inquiree_address}>",
                "to": "davidhanson.c@gmail.com",
                "subject": subject,
                "text": message
                })


if __name__ == "__main__":
    app.run()
    # app.run(debug=True)
