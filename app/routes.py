from flask import Blueprint, request, send_file
from io import BytesIO
from PIL import Image
from .segmenter import segment_image

segment_blueprint = Blueprint("segment", __name__)


@segment_blueprint.route("/segment", methods=["POST"])
def segment():
    if "image" not in request.files or "model_size" not in request.form:
        return "No image file or model size provided", 400

    file = request.files["image"]
    model_size = request.form["model_size"]
    image = Image.open(file)

    # Perform segmentation
    segmented_image = segment_image(image, model_size=model_size)

    # Save segmented image to a bytes buffer
    img_io = BytesIO()
    segmented_image.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")
