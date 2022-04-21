import os
import sys
from pydub import AudioSegment


def process_files(directory_files):
  files_list = os.listdir(directory_files) 
  list_extension = ['ogg', 'mp3', 'wma', 'flv', 'mp4'] 
  
  new_path = directory_files.split('/')
  new_path = [element for element in new_path if element != '']
  new_path[-1] = new_path[-1] + '_wav/' 
  new_path = '/'.join(new_path) 

  for file in files_list:
    file_extension = file.split('.')[-1]
    if file_extension in list_extension:
      path = directory_files + '/' + file
      new_file = file.split('.')[0]
      data = AudioSegment.from_file(path, file_extension)

      if not os.path.isdir(new_path):
        os.makedirs(new_path)

      new_file = new_path + new_file

      data.export(new_file + '.wav', format="wav")
  
  
if __name__ == '__main__':
  process_files(sys.argv[1])