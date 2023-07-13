from flask import Blueprint, jsonify, request
from sqlalchemy.orm.exc import NoResultFound
import services.tasks as task_service
from flask_cors import cross_origin


image_processing_bp = Blueprint(
    "image_processing_bp", __name__, url_prefix="/api/image-processing"
)


@image_processing_bp.route("/", methods=["GET"])
def get_all_tasks():
    return jsonify(task_service.get_all_tasks())


@image_processing_bp.route("/", methods=["POST"])
def create_task():
    content = request.json

    if not all(k in content for k in ["file_ids", "algorithm"]):
        return jsonify({"message": "Required fields are 'file_ids', 'algorithm'"}), 204

    try:
        return jsonify(
            {
                "task-ids": task_service.create_task(
                    content["file_ids"], content["algorithm"], content["params"]
                )
            }
        )
    except task_service.FileNotFoundException as e:
        return jsonify({"message": "File can't be found!"}), 400
    except task_service.FileNotImageException as e:
        return jsonify({"message": "File is not an image!"}), 400
    except task_service.FileException as e:
        return jsonify({"message": "Failed to process the query!"}), 500
    except Exception:
        return jsonify({"message": "Server Error"}), 500


@image_processing_bp.route("/<id>/", methods=["GET"])
def get_task_by_id(id):
    try:
        return jsonify(task_service.get_task_by_id(id).dict)
    except NoResultFound:
        return jsonify({"message": "Task Not Found"}), 404
    except AttributeError:
        return jsonify({"message": "Task Not Found"}), 404
    except Exception:
        return jsonify({"message": "Server Error"}), 500


@image_processing_bp.route("/<id>/restart/", methods=["POST"])
def restart_task(id):
    try:
        return jsonify(task_service.restart_task(id).dict)
    except task_service.TaskRestartException as e:
        return jsonify({"message": "".join(e.args)}), 500
    except Exception:
        return jsonify({"message": "Server Error"}), 500


@image_processing_bp.route("/status", methods=["GET"])
def check_status():
    return ({"status": "healthy"})