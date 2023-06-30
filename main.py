from flask import Flask, render_template, request, send_file, redirect, jsonify
import os
import platform, socket, psutil
import datetime
import json

init_time = datetime.datetime.now()

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/queryAllFiles", methods=["GET"])
def queryAll():
    with open("data/index.json", "r") as file:
        return jsonify(json.loads(file.read()))


@app.route("/image", methods=["GET"])
def serveImage():
    args = request.args
    img_name = args.get("image", default="", type=str)
    folder_name = args.get("folder", default="", type=str)
    action = args.get("action", default="", type=str)

    if img_name != "" and folder_name != "":
        # TODO: add delete
        if action == "delete":
            try:
                os.remove(f"{folder_name}/{img_name}")
                # remove the file in the index
                index = json.loads(open('data/index.json', 'r').read())
                for i in range(len(index)):
                    if (index[i][0] == img_name):
                        del index[i]
                        break
                open('data/index.json', 'w').write(json.dumps(index))
                return True
            except Exception as e:
                return {"status": "failed", "error": str(e)}

        elif action == "":
            try:
                path = f"{folder_name}/{img_name}"
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
                # get path
                path = "assets"
                # get filetype
                video_extensions = ["mp4", "avi", "mkv", "mov", "wmv"]
                extension = file.filename.split(".")[1]
                print(extension)
                if extension != "json":
                    if extension in video_extensions:
                        filetype = "video"
                    else:
                        filetype = "image"
                # save file at the defined path
                file.save(os.path.join(path, file.filename))
                # add the file to the index
                index = json.loads(open('data/index.json', 'r').read())
                index.append([file.filename, path, filetype])
                open('data/index.json', 'w').write(json.dumps(index))

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
# TODO: finish upload page
