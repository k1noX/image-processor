from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
import os
import datetime
import re
from werkzeug.utils import secure_filename


from Files.Utils import is_allowed_name, transliterate, secure_file_path, secure_path
from Models.SessionMaker import get_db_session
from Models.File import File, engine
from Config.Config import AppConfig, FlaskConfig


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

flask_config = FlaskConfig()

app.secret_key = flask_config.secret
app.config["CORS_HEADERS"] = "Content-Type"
app.url_map.strict_slashes = False
app_config = AppConfig()


@app.route("/api/file-server/", methods=["POST"])
@cross_origin()
def upload_file():
    if not "file" in request.files:
        return jsonify({"message": "File Not Found!"}), 204

    f = request.files["file"]

    _, extension = os.path.splitext(f.filename)
    name = f.filename
    if "name" in request.form:
        name = request.form["name"] + extension

    try:
        if not is_allowed_name(name):
            return jsonify({"message": "File Name Not Allowed!"}), 400

        with get_db_session(engine) as session:
            name = re.sub(f"{extension}$", "", name)
            created_at = datetime.datetime.now()

            file = File(
                name=name,
                extension=extension,
                created_at=created_at,
            )

            if "comment" in request.form:
                file.comment = request.form["comment"]
                
            session.add(file)
            session.commit()
        
        with get_db_session(engine) as session:    
            file = session.query(File).filter(File.name == name)\
                .filter(File.extension == extension)\
                .filter(File.created_at == created_at).first()
                    
            f.save(os.path.join(app_config.path, str(file.id) + file.extension))

            file.size = os.stat(os.path.join(app_config.path, str(file.id) + file.extension)).st_size
            
            session.commit()
            
            return jsonify(file.dict), 200
    except FileNotFoundError:
        return jsonify({"message": "File Folder Not Found!"}), 500


@app.route("/api/file-server/", methods=["GET"])
@cross_origin()
def get_all_files():
    with get_db_session(engine) as session:
        files = session.query(File).all()
        result = []

        for file in files:
            result.append(file.dict)

        return jsonify(result)


@app.route("/api/file-server/<id>/", methods=["GET"])
@cross_origin()
def get_file_by_id(id):
    with get_db_session(engine) as session:
        print(id)
        file = session.query(File).filter(File.id == id).first()

        if not file:
            return jsonify({"message": "File Not Found!"}), 404

        if not file.exists:
            session.delete(file)
            session.commit()
            return jsonify({"message": "File Not Found!"}), 404

        return jsonify(file.dict)


@app.route("/api/file-server/<id>/", methods=["PATCH"])
@cross_origin()
def update_file_by_id(id):
    if not any((param in request.json for param in ["name", "comment"])):
        return jsonify({"message": "Method Requires Name, Comment or Path"}), 204

    with get_db_session(engine) as session:
        file = session.query(File).filter(File.id == id).first()

        if not file:
            return jsonify({"message": "File Not Found!"}), 404

        if not file.exists:
            session.delete(file)
            return jsonify({"message": "File Not Found!"}), 404

        try:
            if "name" in request.json:
                new_name = transliterate(request.json["name"])
                file.rename(new_name)

            if "comment" in request.json:
                file.set_comment(request.json["comment"])

        except File.FileError as e:
            return jsonify({"message": e.args}), 400

        session.commit()

        return jsonify(file.dict)


@app.route("/api/file-server/<id>/", methods=["DELETE"])
@cross_origin()
def delete_file_by_id(id):
    with get_db_session(engine) as session:
        file = session.query(File).filter(File.id == id).first()

        if not file:
            return jsonify({"message": "File Not Found!"}), 404

        if file.exists:
            os.remove(file.full_path)

        session.delete(file)
        session.commit()
        return jsonify({"message": "File Has Been Removed!"})


@app.route("/api/file-server/<id>/download", methods=["GET"])
def download_file(id):
    with get_db_session(engine) as session:
        file = session.query(File).filter(File.id == id).first()

        if not file:
            return jsonify({"message": "File Not Found!"}), 404

        if not file.exists:
            session.delete(file)
            session.commit()
            return jsonify({"message": "File Not Found!"}), 404

        return send_from_directory(
            os.path.join(app_config.path),
            path=str(file.id) + file.extension,
            as_attachment=False,
        )