from datetime import datetime
import os
import re
import threading
import cv2
from cv2 import dnn_superres
import requests
from vmagnify import VMagnify


class VMagnifyPicture(VMagnify):
    DOWNLOAD_FOLDER = "static/img/downloads/"
    GENERATED_FOLDER = "static/img/generated/"

    def __init__(self) -> None:
        """ class constructor """
        self.original_picture = None

    def __download_url_content(self, r, file_extension):
        """ download the content of the URL"""
        current_datetime = datetime.now()
        # As original file name can be unreliable, file name is built with the current datetime
        file_path = self.DOWNLOAD_FOLDER + \
            current_datetime.strftime("%Y_%m_%d_%H_%M_%S") + file_extension
        open(file_path, 'xb').write(r.content)
        return file_path

    def __get_url(self, url: str):
        """ do a GET request on the URL """
        r = requests.get(url, allow_redirects=True)
        _, file_extension = os.path.splitext(url)
        return r, file_extension

    def __generate_pictures(self):
        """ generate the pictures of the 3 models """
        process_x2_picture = threading.Thread(target=self.__process_thread_picture, args=(
            self.original_picture, self.EDSR_MODEL_X2_PATH))
        process_x3_picture = threading.Thread(target=self.__process_thread_picture, args=(
            self.original_picture, self.EDSR_MODEL_X3_PATH))
        process_x4_picture = threading.Thread(target=self.__process_thread_picture, args=(
            self.original_picture, self.EDSR_MODEL_X4_PATH))
        process_x2_picture.start()
        process_x3_picture.start()
        process_x4_picture.start()
        process_x2_picture.join()
        process_x3_picture.join()
        process_x4_picture.join()

    def __process_thread_picture(self, original_picture, model_path: str):
        """ thread which generates a picture by calling the model """
        # Create an SR object
        sr = dnn_superres.DnnSuperResImpl_create()
        # Get the model name
        model_type = model_path.split("/")[2].lower()
        base_name = os.path.basename(model_path)
        model_name, _ = os.path.splitext(base_name)
        # Get the model scale
        model_scale = int(model_name.split("x")[1])
        file_name = os.path.basename(self.__file_path)
        # Read the desired model
        sr.readModel(model_path)
        # Configure the model
        sr.setModel(model_type, model_scale)
        # Process the picture
        generated_picture = sr.upsample(original_picture)
        # Save the picture
        new_file_path = self.GENERATED_FOLDER + \
            file_name+"_x"+str(model_scale)+".jpg"
        cv2.imwrite(new_file_path, generated_picture)

    def __remove_file(self, path: str):
        """ remove the file when it is invalid """
        os.remove(path)

#    def __upload_picture(self):

    def __validate_file(self, path: str):
        """ validate if the file in input is a picture """
        FILE_EXTENSIONS_LIST = [".png", ".jpg", ".jpeg"]
        _, file_extension = os.path.splitext(path)
        try:
            FILE_EXTENSIONS_LIST.index(file_extension)
        except ValueError:
            # ValueError means that the file extension found isn't in our list
            return False
        mat = cv2.imread(path)
        h, w, c = mat.shape
        if h > 0 and w > 0 and c == 3:
            # picture is valid if we have an height and width greater than 0 and 3 color channels
            self.__file_path = path
            self.original_picture = mat
            return True
        else:
            return False

#    def __cleanup_pictures(self):

#    def process_uploaded_picture(self, file: str):

    def process_url(self, url: str):
        """ process the URL """
        self.url = url
        r, file_extension = self.__get_url(url)
        if r.status_code == 200:
            # status code 200 is OK
            file_path = self.__download_url_content(r, file_extension)
            res = self.__validate_file(file_path)
            if res:
                self.__generate_pictures()
            else:
                self.__remove_file(file_path)
