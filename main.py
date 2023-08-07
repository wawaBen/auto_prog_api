
from distutils.log import debug
from fileinput import filename
import pandas as pd
from flask import *
from flask_restful import Resource, Api, reqparse
import os
from werkzeug.utils import secure_filename
import zipfile
from os.path import exists
import werkzeug

UPLOAD_DIRECTORY_ONE = "./data/one/"
UPLOAD_DIRECTORY_TWO = "./data/two/"
TMP_ZIP_FILE = "/tmp/files_off.zip"

app = Flask(__name__)
api = Api(app)


class Upload(Resource):

    def get(self):
        return "GET OK. YOU SHOULD USE POST METHOD FOR THIS API", 200  # return data and 200 OK


    def post(self):


        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('fileEEPROM', required=True, type=werkzeug.datastructures.FileStorage, location='files') # add filelocation
        args = parser.parse_args()  # parse arguments to dictionary

        fileEEPROM = args['fileEEPROM']
        uploadType = 'SID208'

        if (uploadType=='DCU102'):
            UPLOAD_DIRECTORY = UPLOAD_DIRECTORY_ONE
        elif (uploadType=='SID208'):
            UPLOAD_DIRECTORY = UPLOAD_DIRECTORY_TWO
        else:
            return "incorrect type", 200
        
        if (exists(TMP_ZIP_FILE)):
            os.remove(TMP_ZIP_FILE)


        zipfolder = zipfile.ZipFile(TMP_ZIP_FILE,'w', compression = zipfile.ZIP_STORED) # Compression type 

            
        # zip all the files which are inside in the folder
        for root,dirs, files in os.walk(UPLOAD_DIRECTORY):
            for file in files:
                zipfolder.write(UPLOAD_DIRECTORY+file)
        zipfolder.close()

        response = make_response(send_file(TMP_ZIP_FILE, mimetype = 'zip', download_name= 'files_off.zip', as_attachment = True), 200)

        response.headers.set('Access-Control-Allow-Origin', '*')
        response.headers.set('Access-Control-Allow-Methods', 'POST')

        return response
 
api.add_resource(Upload, '/upload')  # add endpoints

if __name__ == '__main__':
    app.run(debug=True)