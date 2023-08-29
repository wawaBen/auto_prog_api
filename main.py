from fastapi import FastAPI, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import os
from os.path import exists
from fastapi.responses import FileResponse
from fastapi_versioning import VersionedFastAPI, version
from Utils import dcu102, sid208


# -----------------
# Description
# ----------------- 

description = """
AutoProgAPI helps to manipulate hex files for auto programming. 🚀

## DCU102

One file to transform for IMMOFF

## SID208

2 files to provide (flash & EEPROM) to transform for IMMOFF

"""

app = FastAPI(
    title='auto-prog-app',
    description=description,
    summary="API for autoprogramming app",
    version="1.0",
)



# -----------------
# Set CORS Policy
# TODO : restriction to specific location   
# ----------------- 

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------
# Params
# ----------------- 

TMP_OUTPUT_DIR = "/tmp/files/"
TMP_ZIP_FILE = "/tmp/files_off.zip"

# -----------------
# Pour le DCU102   
# ----------------- 

@app.post("/uploadDCU102/{type}",
        status_code=status.HTTP_200_OK,
        summary="DCU 102 calculator",
        description="blablabla")
@version(1, 0)
def post_fileDCU102(type: str, fileDCU102: UploadFile):

    #Check that we are doing IMMOOFF
    if (type=="IMMOOFF"):

        #Creating the output file name
        output_file=TMP_OUTPUT_DIR+fileDCU102.filename.replace(".bin","")+"_off"

        #We remove all previous files
        if (exists(TMP_ZIP_FILE)):
            os.remove(TMP_ZIP_FILE)
            
        if (exists(output_file)):
            os.remove(output_file)

        #Creating folder if it doesn't exists
        if (not exists(TMP_OUTPUT_DIR)):
            os.mkdir(TMP_OUTPUT_DIR)

        #We call the associated function
        dcu102.processing_DCU102(fileDCU102, output_file)

        #Creating zip file
        dcu102.zipfileFunction(TMP_ZIP_FILE, output_file)

        #Deleting output file
        if (exists(output_file)):
            os.remove(output_file)

        response = FileResponse(path=TMP_ZIP_FILE, filename="files_off.zip")

    else:
        response = {"message": "Type Unknown"}
        raise HTTPException(status_code=404, detail="Type not found")

    return response

# -----------------
# Pour le SID208   
# ----------------- 

@app.post("/uploadSID208")
@version(1, 0)
def post_fileSID208(type: str, fileSID208_flash: UploadFile, fileSID208_EEPROM: UploadFile):

    #Check that we are doing IMMOOFF
    if (type=="IMMOOFF"):
        
        #Creating the output file name
        output_file_flash=TMP_OUTPUT_DIR+fileSID208_flash.filename.replace(".bin","")+"_off"
        output_file_EEPROM=TMP_OUTPUT_DIR+fileSID208_EEPROM.filename.replace(".bin","")+"_off"

        #We remove all previous files
        if (exists(TMP_ZIP_FILE)):
            os.remove(TMP_ZIP_FILE)
            
        if (exists(output_file_flash)):
            os.remove(output_file_flash)
        
        if (exists(output_file_EEPROM)):
            os.remove(output_file_EEPROM)

        #Creating folder if it doesn't exists
        if (not exists(TMP_OUTPUT_DIR)):
            os.mkdir(TMP_OUTPUT_DIR)

        #We call the associated function
        sid208.processing_SID208(fileSID208_flash, fileSID208_EEPROM, output_file_flash, output_file_EEPROM)

        # Creating zip file
        sid208.zipfileFunction(TMP_ZIP_FILE, output_file_flash, output_file_EEPROM)

        #Deleting output file
        if (exists(output_file_flash)):
            os.remove(output_file_flash)
        if (exists(output_file_EEPROM)):
            os.remove(output_file_EEPROM)

        response = FileResponse(path=TMP_ZIP_FILE, filename="files_off.zip")

    else:
        response = {"message": "Type Unknown"}
        raise HTTPException(status_code=404, detail="Type not found")

    return response


# ----------------------
# Pour le versionning   
# ----------------------

app = VersionedFastAPI(app)