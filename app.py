from flask import Flask, request, render_template_string

app = Flask(__name__)

# Load the HTML from the same file above or as a template
with open("index.html", "r") as file:
    html_template = file.read()

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    date = request.form['date']
    time = request.form['time']
    service = request.form['service']

    # Here you could email this info to the owner or store in a DB
    print(f"New Booking:\nName: {name}\nEmail: {email}\nPhone: {phone}\nDate: {date}\nTime: {time}\nService: {service}")

    return f"""
        <h2>Thank you {name}, your appointment for {service} on {date} at {time} is confirmed!</h2>
        <p>We have sent the details to the parlour owner.</p>
        <a href='/'>Book another</a>
    """

if __name__ == '__main__':
    app.run(debug=True)
