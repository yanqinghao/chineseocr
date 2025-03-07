# coding=utf-8
from __future__ import absolute_import, print_function

import os
import json
from suanpan.app import app
from suanpan.app.arguments import Folder
from suanpan.log import logger
from suanpan.utils import image
from suanpan.storage import storage
from arguments import Images


@app.input(Images(key="inputImage"))
@app.input(Folder(key="inputData"))
@app.output(Images(key="outputImage"))
def SPViaSegment(context):
    args = context.args
    images = args.inputImage

    files = []

    try:
        jsonFile = os.path.join(args.inputData, "project.json")
        with open(jsonFile, "rb") as load_f:
            fileInfo = json.load(load_f)

        for i, j in fileInfo["metadata"].items():
            files.append(os.path.join(images.folder, j["vid"]))
            try:
                filename = os.path.splitext(j["vid"])[0] + "_" + j["av"]["1"] + ".png"
            except:
                filename = (
                    os.path.splitext(j["vid"])[0] + "_" + i.split("_")[-1] + ".png"
                )
            xy = j["xy"][1:]
            img = image.read(os.path.join(images.folder, j["vid"]))
            image.save(
                os.path.join(args.outputImage, filename),
                img[
                    int(xy[1]) : int(xy[1] + xy[3]), int(xy[0]) : int(xy[0] + xy[2]), :
                ],
            )
    except:
        logger.info("can not find project.json or json format error")

    for idx, img in enumerate(images):
        if images.images[idx] not in files:
            image.save(
                os.path.join(
                    args.outputImage,
                    storage.delimiter.join(
                        images.images[idx].split(storage.delimiter)[8:]
                    ),
                ),
                img,
            )

    return args.outputImage


if __name__ == "__main__":
    SPViaSegment()
