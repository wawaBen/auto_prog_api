from fastapi import UploadFile
import zipfile
import binascii

def processing_DCU102(fileDCU102: UploadFile, output_file: str):
    buff = fileDCU102.file.read()
    size = len(buff)
    print(size)
    out_hex = ['{:02X}'.format(b) for b in buff]

    check_num=None
    count=0
    for index,f in enumerate(out_hex):
        if f=='A5':
            num="".join([out_hex[index-6],out_hex[index-5],out_hex[index-4],out_hex[index-3],out_hex[index-2],out_hex[index-1],out_hex[index]])
            if not check_num and (index==16860 or index==25052):
                check_num=num     
            if num==check_num:
                count+=1
                out_hex[index-6]='FF'
                out_hex[index-5]='FF'
                out_hex[index-4]='FF'
                out_hex[index-3]='FF'
                out_hex[index-2]='FF'
                out_hex[index-1]='FF'
                out_hex[index]='FF'

    with open(output_file, 'wb') as fout:
        for line in out_hex:
            fout.write(
                binascii.unhexlify(''.join(line.split()))
            )


def zipfileFunction(TMP_ZIP_FILE, output_file):

    zip_file = zipfile.ZipFile(TMP_ZIP_FILE,'w', compression = zipfile.ZIP_STORED) # Compression type     
    # zip the file
    zip_file.write(output_file)
    zip_file.close()