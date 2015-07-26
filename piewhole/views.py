from piewhole import app

@app.route("/")
def say_hi():
    return 'Site is live'
