from flask import Flask, render_template

app = Flask(__name__, template_folder="front")


@app.route("/")
def handle_main_page():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
