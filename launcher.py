import os
import hashlib
import subprocess
import configparser
from urllib import request
import difflib

config = configparser.ConfigParser()
config.read('config.ini')

exe_file = config['DEFAULT']['exe_path']
md5_file = config['DEFAULT']['md5_path']
md5_updated_file = config['DEFAULT']['md5_updated_path']
app_folder = config['DEFAULT']['app_path']
url = config['WEB']['url']

df = difflib.Differ()

md5_file_text = open(md5_file, "r").read()
md5_updated_file_text = open(md5_updated_file, "r").read()

def hasher(rootdir):
   for dirpath,_,filenames in os.walk(rootdir):
      for f in filenames:
          hasher = hashlib.md5()
          full_path = os.path.join(dirpath, f)
          content = open(full_path, 'rb').read()
          hasher.update(content)
          md5.write(hasher.hexdigest() + full_path.replace('./app/', ' *') + '\n')

# running terminal 
process = subprocess.Popen(['wine ' + exe_file], shell=True)

# create md5 hash
md5 = open(md5_file, 'w')
hasher(app_folder)
md5.close()   

# upload update.md5
request.urlretrieve(url + "/update.md5", "update.md5")

# difference
txt1_list = sorted(md5_file_text.splitlines())
txt2_list = sorted(md5_updated_file_text.splitlines())
difference = list(df.compare(txt1_list, txt2_list))

for item in difference:
    if (item.find("+") == 0):
        file_path = item.split('*')[1]
        try: 
            request.urlretrieve(url + "/" + file_path, 'app/' + file_path)
        except:
            print('Error on file [create]' + file_path)
    if (item.find("-") == 0):
        file_path = item.split('*')[1]
        try: 
            os.remove('./app/' + file_path)
        except:
            print('Error on file [remove]' + file_path)

# md5 upload new settings
md5 = open(md5_file, 'w')
md5.write(md5_updated_file_text)
md5.close()

