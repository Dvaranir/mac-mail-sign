import base64
import os
import glob
import uuid
from pathlib import Path

id_for_sign = str(uuid.uuid1())[0:7]
sign_name = f"Itsupport_Sign_{id_for_sign}"
all_signatures_file_name = "AllSignatures.plist"
new_sign_template = f"""
    <dict>
        <key>SignatureIsRich</key>
        <true/>
        <key>SignatureName</key>
        <string>{sign_name}</string>
        <key>SignatureUniqueId</key>
        <string>{sign_name}</string>
    </dict>
"""

path_to_mail = os.path.expanduser("~/Library/Mail/")

os.chdir(path_to_mail)
folder_name = glob.glob("V**")[0]

synced_file_name = "SyncedFilesInfo.plist"

os.chdir(os.path.expanduser("~/Downloads/sign-script"))

path_to_mail_data = os.path.expanduser(f"~/Library/Mail/{folder_name}/MailData")
path_to_library = os.path.expanduser(f"{path_to_mail_data}/Signatures/")
path_to_all_signatures_file = path_to_library + all_signatures_file_name
path_to_synced_file = f"{path_to_mail_data}/{synced_file_name}"

if os.path.exists(path_to_synced_file):
    os.remove(f"{path_to_mail_data}/{synced_file_name}")
else:
    print("SyncedFilesInfo.plist not exist, continue")

data_array = []

with open ("data.txt", "r", encoding="utf-8") as data:
    for line in data:
        data_array.append(line.split(":")[1].strip())

name = data_array[0]
position = data_array[1]
number = data_array[2]
email = data_array[3]
address = data_array[4]
residence = data_array[5]
photo_name = data_array[6]
first_sign_paragraph = data_array[7].split("!!НОВАЯСТРОКА!!")[0]
second_sign_paragraph = data_array[7].split("!!НОВАЯСТРОКА!!")[1]

with open(photo_name, "rb") as image_file:
     encoded_image_bytes = base64.b64encode(image_file.read())
encoded_image_string = str(encoded_image_bytes)[2:-1]

with open ("sign.mailsignature", "r", encoding="utf-8") as sign_template:
    sign_template_string = sign_template.read()

output_sign_string = sign_template_string.replace("!!NAME!!", name).replace("!!POSITION!!", position).replace("!!NUMBER!!", number).replace("!!EMAIL!!", email).replace("!!ADDRESS!!", address).replace("!!RESIDENCE!!", residence).replace("!!IMAGE!!", encoded_image_string).replace("!!SIGNPARTONE!!", first_sign_paragraph).replace("!!SIGNPARTTWO!!", second_sign_paragraph)

with open (f"{path_to_library}{sign_name}.mailsignature", "w", encoding="utf-8") as output_file:
    output_file.write(output_sign_string)

signatures_file = Path(path_to_all_signatures_file)

def createSignatureFile():
    with open (all_signatures_file_name, "r", encoding="utf-8") as signature_list:
        signature_list_string = signature_list.read()

    
    output_signature_list = signature_list_string.replace("!!SIGN!!", new_sign_template)

    with open (path_to_all_signatures_file, "w", encoding="utf-8") as all_signnatures:
        all_signnatures.write(output_signature_list)

def addSignature():
    with open (path_to_all_signatures_file, "r", encoding="utf-8") as all_signnatures:
        all_signnatures_string = all_signnatures.read()

    anchor = all_signnatures_string.rfind("</dict>")
    anchor_length = len("</dict>")

    signatures_first_part = all_signnatures_string[0:anchor + anchor_length]
    signatures_second_part = all_signnatures_string[anchor + anchor_length:]
    
    with open (path_to_all_signatures_file, "w", encoding="utf-8") as all_signnatures_file:
        all_signnatures_file.write(signatures_first_part + new_sign_template + signatures_second_part)

if signatures_file.exists():
    addSignature()
else:
    createSignatureFile()

