from fastapi import UploadFile
import zipfile
import binascii

def processing_SID208(fileSID208_flash: UploadFile, fileSID208_EEPROM: UploadFile, output_file_flash: str, output_file_EEPROM: str):
    
    buff1 = fileSID208_flash.file.read()
    out_hex1 = ['{:02X}'.format(b) for b in buff1]

    check_num=None
    check_byte=None
    count=0
    for index,f in enumerate(out_hex1):
        if index==4102 or check_byte==f:
            num="".join([out_hex1[index-6],out_hex1[index-5],out_hex1[index-4],out_hex1[index-3],out_hex1[index-2],out_hex1[index-1],out_hex1[index]])
            if not check_num:
                check_num=num
                check_byte=out_hex1[index]    
            if num==check_num:
                count+=1
                out_hex1[index-6]='00'
                out_hex1[index-5]='00'
                out_hex1[index-4]='00'
                out_hex1[index-3]='00'
                out_hex1[index-2]='00'
                out_hex1[index-1]='00'
                out_hex1[index]='00'


    with open(output_file_flash, 'wb') as fout:
        for line in out_hex1:
            fout.write(
                binascii.unhexlify(''.join(line.split()))
            )


    buff2 = fileSID208_EEPROM.file.read()
    out_hex2 = ['{:02X}'.format(b) for b in buff2]

    for index,f in enumerate(out_hex2):
        if check_byte==f:
            num="".join([out_hex2[index-6],out_hex2[index-5],out_hex2[index-4],out_hex2[index-3],out_hex2[index-2],out_hex2[index-1],out_hex2[index]])
            if num==check_num:
                count+=1
                out_hex2[index-6]='00'
                out_hex2[index-5]='00'
                out_hex2[index-4]='00'
                out_hex2[index-3]='00'
                out_hex2[index-2]='00'
                out_hex2[index-1]='00'
                out_hex2[index]='00'
                out_hex2[index+1]='00'  

    with open(output_file_EEPROM, 'wb') as fout:
        for line in out_hex2:
            fout.write(
                binascii.unhexlify(''.join(line.split()))
            )



def zipfileFunction(TMP_ZIP_FILE, output_file_flash, output_file_EEPROM):

    zip_file = zipfile.ZipFile(TMP_ZIP_FILE,'w', compression = zipfile.ZIP_STORED) # Compression type     
    # zip the file
    zip_file.write(output_file_flash)
    zip_file.write(output_file_EEPROM)
    zip_file.close()