from werkzeug.utils import secure_filename

def upload_process(filename):
    filename = secure_filename(filename)
    fileFullPath = os.path.join(application.config['UPLOAD_FOLDER'], filename)
    with open(fileFullPath, "wb") as f:
        chunk_size = 4096
        while True:
            chunk = flask.request.stream.read(chunk_size)
            if len(chunk) == 0:
                return

            f.write(chunk)
    return jsonify({'filename': filename})