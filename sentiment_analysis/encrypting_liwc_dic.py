from itertools import cycle
import base64
import zipfile
import re
import sys

"""
Example command:
python script.py "./original/LIWC2015_English.dic" "./e2015.dic" "/home/user/.wine/drive_c/Program Files (x86)/LIWC2015/app/lib/LIWC2015-app-1.5.0.jar"
"""

input_dic = 'D:\\Desktop\\Social_Sharing\\raw_data\\LIWC2015_English_Flat.dic'
output_dic = 'D:\\Desktop\\Social_Sharing\\raw_data\\e2015.dic'

jar_location = 'D:\\Software\\LIWC2015\\app\\lib\\LIWC2015-app-1.6.0.jar'
class_name = 'com/liwc/LIWC2015/model/Dictionary.class'
expr = re.compile(b'\x0e([\x20-\x7f]+)\x07')
key = None

with zipfile.ZipFile(jar_location, 'r') as zf:
    with zf.open(class_name, 'r') as byte_stream:
        byte_code = byte_stream.read()
        all_matches = re.findall(expr, byte_code)
        if len(all_matches) >= 1:
            key = str.encode(all_matches[0].decode())

if key is None:
    print("Key not found. Can't proceed.")
else:
    with open(input_dic, 'rb') as f:
        message = f.read()

    decrypted_msg = ''.join([chr(i^j) for i, j in zip(base64.decodebytes(message), cycle(key))])
    with open(output_dic, 'wb') as f:
        f.write(str.encode(decrypted_msg))
