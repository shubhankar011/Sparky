from flask import Flask, render_template, Response

from livestreaming import run_vision_web

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        run_vision_web(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    print("Sparky camera server running...")
    print("Local:   http://127.0.0.1:5000")
    print("Network: http://<YOUR-LAPTOP-IP>:5000")

    app.run(
        host="0.0.0.0",
        port=5000,
        threaded=True
    )
