from flask import Flask, request, jsonify, redirect
from flask_cors import CORS, cross_origin
import os


from utils.file_utils import transliterate
from models.file import File
from services.files import create_file
from injectors.flask import FlaskContainer
from injectors.app import AppContainer
from injectors.db import DbContainer

app = FlaskContainer.app

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
        file = create_file(f, name, extension, request.form['comment'])
            
        return jsonify(file.dict), 200
    except FileNotFoundError:
        return jsonify({"message": "File Folder Not Found!"}), 500


@app.route("/api/file-server/", methods=["GET"])
@cross_origin()
def get_all_files():
    with DbContainer.get_db_session(DbContainer.engine) as session:
        files = session.query(File).all()
        result = []

        for file in files:
            result.append(file.dict)

        return jsonify(result)


@app.route("/api/file-server/<id>/", methods=["GET"])
@cross_origin()
def get_file_by_id(id):
    with DbContainer.get_db_session(DbContainer.engine)  as session:
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
        return jsonify({"message": "Method Requires Name or Comment"}), 204

    with DbContainer.get_db_session(DbContainer.engine)  as session:
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
    with DbContainer.get_db_session(DbContainer.engine)  as session:
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
    with DbContainer.get_db_session(DbContainer.engine)  as session:
        file: File = session.query(File).filter(File.id == id).first()

        if not file:
            return jsonify({"message": "File Not Found!"}), 404

        if not file.exists:
            session.delete(file)
            session.commit()
            return jsonify({"message": "File Not Found!"}), 404
        print(f"REDIRECT_URL={AppContainer.config.static_redirect_url}")
        print(AppContainer.config.static_redirect_url + str(file.id) + str(file.extension))
        return redirect(AppContainer.config.static_redirect_url + str(file.id) + str(file.extension), 301)

@app.route("/api/file-server/status", methods=["GET"])
def check_status():
    return ({"status": "healthy"})