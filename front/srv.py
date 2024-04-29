from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
def handle_main_page():
    bs_css = url_for('static', filename='bootstrap/bootstrap.min.css')
    bs_js = url_for('static', filename='bootstrap/bootstrap.bundle.min.js')
    script_js = url_for('static', filename='script.js')
    return render_template("index.html", bs_css=bs_css, bs_js=bs_js, script_js=script_js)


@app.route("/register")
def handle_register_page():
    bs_css = url_for('static', filename='bootstrap/bootstrap.min.css')
    bs_js = url_for('static', filename='bootstrap/bootstrap.bundle.min.js')
    script_js = url_for('static', filename='script.js')

    for_reg_js = url_for("static", filename="for_reg.js")
    return render_template("reg_page.html", bs_css=bs_css, bs_js=bs_js, script_js=script_js, for_reg_js=for_reg_js)


@app.route("/login")
def handle_login_page():
    bs_css = url_for('static', filename='bootstrap/bootstrap.min.css')
    bs_js = url_for('static', filename='bootstrap/bootstrap.bundle.min.js')
    script_js = url_for('static', filename='script.js')

    for_auth_js = url_for("static", filename="for_auth.js")
    return render_template("auth_page.html", bs_css=bs_css, bs_js=bs_js, script_js=script_js, for_auth_js=for_auth_js)


if __name__ == '__main__':
    app.run(debug=True, port=8000, host="0.0.0.0")
