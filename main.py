from flask import Flask, render_template, request, send_file, redirect
import os
import platform, socket, psutil
import datetime

init_time = datetime.datetime.now()

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/queryAllFiles", methods=["GET"])
def queryAll():
    folder_name = request.args.get("folderName", default="assets", type=str)
    dir = os.listdir(folder_name)
    res = []
    for i in dir:
        # image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        video_extensions = [".mp4", ".avi", ".mkv", ".mov", ".wmv"]
        extension = i[-4:]
        if extension in video_extensions:
            res.append((i, "video"))
        else:
            res.append((i, "image"))
    return {"dir": res}


@app.route("/image", methods=["GET"])
def serveImage():
    args = request.args
    img_name = args.get("image", default="", type=str)
    folder_name = args.get("folder", default="", type=str)
    action = args.get("action", default="", type=str)

    print(img_name)
    print(folder_name)

    if img_name != "" and folder_name != "":
        # TODO: add delete
        if action == "delete":
            try:
                os.remove(f"{folder_name}/{img_name}")
                print(f"deleted: {folder_name}/{img_name}")
                return True
            except Exception as e:
                return {"status": "failed", "error": str(e)}

        elif action == "":
            try:
                path = f"{folder_name}/{img_name}"
                print(path)
                return send_file(path)
            except Exception as e:
                return str(e)


@app.route("/icon/<name>", methods=["GET"])
def favicon(name):
    return send_file(f"icon/{name}")


# TODO: add a upload gate
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        print("get")
        return render_template("upload.html")
    elif request.method == "POST":
        try:
            files = request.files.getlist("file[]")
            for file in files:
                file.save(f"assets/{file.filename}")
            return redirect("/", code=302)
        except Exception as e:
            return {"status": "failed", "error": str(e)}

# host info
@app.route("/hostinfo")
def hostInfo():
    try:
        info = {}
        info["hostname"] = socket.gethostname()
        info["uptime"] = init_time
        info["platform"] = f"{platform.system()} {platform.release()} ({platform.version()})"
        info["processor"] = platform.processor()
        info["architecture"] = platform.machine()
        info["ram"] = str(round(psutil.virtual_memory().total / (1024.0**3))) + " GB"
        return info
    except Exception as e:
        return {"status": "failed", "error": str(e)}


# TODO: add albums
# TODO: write a GUI script which allow the server to run with windows and be able to change database location
# TODO: finish upload page

app.run(host="0.0.0.0", debug=True)
