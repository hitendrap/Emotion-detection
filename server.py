from flask import Flask, render_template, send_from_directory, Response
from camera import Camera
import argparse

camera = Camera()
camera.run()

app = Flask(__name__)
@app.after_request
def add_header(r):
	r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	r.headers["Pragma"] = "no-cache"
	r.headers["Expires"] = "0"
	r.headers["Cache-Control"] = "public, max-age=0"
	return r

@app.route("/")
def entrypoint():
	return render_template("index.html")

@app.route("/images/last")
def last_image():
		r = "main.png"
		return send_from_directory("images",r)

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
			   b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')

@app.route("/stream")
def stream_page():
	return render_template("stream.html")

@app.route("/video_feed")
def video_feed():
	return Response(gen(camera),
		mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-p','--port',type=int,default=5000)
	parser.add_argument("-H","--host",type=str,default='0.0.0.0')
	args = parser.parse_args()
	app.run(host=args.host,port=args.port)