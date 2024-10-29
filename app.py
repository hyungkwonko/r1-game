from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling image segmentation
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the image segmentation here
        segmented_image_path = filepath  # Placeholder
        
        return jsonify({"segmented_image": segmented_image_path})
    return jsonify({"error": "Failed to process image"})

if __name__ == '__main__':
    app.run(debug=True)
