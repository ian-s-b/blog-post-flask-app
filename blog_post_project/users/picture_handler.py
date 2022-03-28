from pathlib import Path
from PIL import Image

from flask import current_app

def add_profile_pic(pic_upload, username):
    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    storage_filename = str(username) + '.' + ext_type

    filepath = str(Path(current_app.root_path,'static','profile_pics',storage_filename))

    output_size = (400,400)

    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename
