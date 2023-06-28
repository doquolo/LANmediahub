from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/queryAllFiles", methods=['GET'])
def queryAll():
    folder_name = request.args.get("folderName", default="assets", type=str)
    dir = os.listdir(folder_name)
    res = []
    for i in dir:
        # image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv']
        extension = i[-4:]
        if extension in video_extensions:
            res.append((i, "video"))
        else:
            res.append((i, "image"))
    return {'dir': res}

@app.route("/image", methods=['GET'])
def serveImage():
    args = request.args
    img_name = args.get("image", default="", type=str)
    folder_name = args.get("folder", default="", type=str)
    print(img_name)
    print(folder_name)
    if (img_name != "" and folder_name != ""):
        try:
            path = f"{folder_name}/{img_name}"
            print(path)
            return send_file(path)
        except Exception as e:
            return str(e)
        
@app.route("/favicon", methods=['GET'])
def favicon():
    return send_file("favicon/favicon.png", mimetype='image/png')
        
# TODO: add a upload gate
# TODO: add albums / adaptive zoom

app.run(host="0.0.0.0")