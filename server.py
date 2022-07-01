import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from datetime import datetime
from flask import Flask, request, render_template
from pathlib import Path

app = Flask(__name__)

# Read image features
fe = FeatureExtractor()
features = []
img_paths = []
for feature_path in Path("./static/feature").glob("*.npy"):
    features.append(np.load(feature_path))
    img_paths.append(Path("./static/img_deckel") / (feature_path.stem + ".jpg"))
features = np.array(features)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["query_img"]
        
        # Crop and Save image
        img = Image.open(file.stream)
        
        width, height = img.size
        img = img.crop((width/5, height/4, width*4/5, height*3/4)) # left top right bottom
        
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)
        
        # Run search
        query = fe.extract(img)
        dists = np.linalg.norm(features - query, axis=1)
        ids = np.argsort(dists)[:50]
        scores = [(dists[id], img_paths[id], id+1) for id in ids]
        
        print(scores)
        
        
        return render_template("puzzle.html", query_path=uploaded_img_path, scores=scores)
    else:
        return render_template("puzzle.html")
    
if __name__ == "__main__":
    app.run()#host='0.0.0.0', debug=True, port=5000)