import pathlib

import os
from fastapi import APIRouter
from starlette.staticfiles import StaticFiles

IMAGEDIR = "images/"
uploads_dir = pathlib.Path(os.getcwd(), IMAGEDIR)


router = APIRouter()
router.mount("/images", StaticFiles(directory="images"), name="images")


def save_image(contents, file_path):
    with open(file_path, "wb") as f:
        f.write(contents)
