import os
import json

from pydub import AudioSegment

# this processing is spetially made for google 

def process_files(directory_files):
  files_list = os.listdir(directory_files) 
  list_extension = ['ogg', 'wav', 'mp3', 'wma', 'flv', 'mp4'] 
  info = {}
  
  time = 0
  qnt_files = 0
  for file in files_list:
    file_extension = file.split('.')[-1]
    if file_extension in list_extension:
      path = directory_files + file
      new_file = file.split('.')[0] 
      data = AudioSegment.from_file(path, file_extension)
      new_path = './processed_files/'


      if not os.path.isdir(new_path):
        os.makedirs(new_path)

      folder = [element for element in directory_files.split('/') if 'adapted' in element][0]
      new_path = new_path + folder + '/'

      if not os.path.isdir(new_path):
        os.makedirs(new_path)

      new_path = new_path + new_file

      data = data.set_sample_width(2)
      data = data.set_channels(1)
      

      if len(data) > 59999:
        len_audio = len(data)
        slice_audio_1 = 0
        slice_audio_2 = 59999 
        naming = 1

        while len_audio != slice_audio_1:
          info[folder + '/' + new_file + '_slice_' + str(naming) + '.wav'] = data.frame_rate

          data[slice_audio_1:slice_audio_2].export(new_path + '_slice_' + str(naming) + '.wav', format="wav")

          naming += 1
          slice_audio_1 = slice_audio_2
          slice_audio_2 = slice_audio_2 + 59999 if len_audio > slice_audio_2 + 59999 else len_audio
      else: 
        info[folder + '/' + new_file + '.wav'] = data.frame_rate
        data.export(new_path + '.wav', format="wav")
      os.remove(path) # comment this line if you don't want the adapted database folder to be erased
 
      time = time + data.duration_seconds
      qnt_files = qnt_files + 1

  file = open(folder + '_info.txt', 'w')
  file.write(str(info).replace("'", '"'))
  print('\nNew files on processed_files/' + folder + ' folder and its informations on ' + folder + '_info.txt file\n\n')
  file.close()

  return time, qnt_files


def split_info_archives(len_buckets, archive_name):
    # in order to make the testing easier 
    file = open("../" + archive_name + ".txt", "r")
    dict_with_files = file.read()
    dict_with_files = json.loads(dict_with_files)

    len_buckets = 500

    count_buckets = 0
    count_files = 0
    temp_dict = {}

    for key in dict_with_files:
        if count_buckets < len_buckets:
            temp_dict[key] = dict_with_files[key]
            count_buckets += 1
        else: 
            file = open('../info/' + archive_name + '_' + str(count_files) + '.txt', 'w')
            file.write(str(temp_dict).replace("'", '"'))
            file.close()
            count_files += 1
            temp_dict = {}
            count_buckets = 0
    
    if count_buckets < len_buckets:
        file = open('../info/' + archive_name + '_' + str(count_files) + '.txt', 'w')
        file.write(str(temp_dict).replace("'", '"'))
        file.close()




if __name__ == '__main__':
  # to generate the report 
  # data_report: some metrics about the database being processed 
  list_dir = os.listdir('./data/')
  list_dir = [element for element in list_dir if '.' not in element]
  all_time = 0
  all_qnt_files = 0

  if os.path.isfile('info.txt'):
    os.remove('info.txt')

  data_report = open('data_report.txt', 'w')

  for folder in list_dir: 
    print(folder)
    time, qnt_files = process_files('./data/' + folder + '/')
    all_time += time
    all_qnt_files += qnt_files
    
    report = 'Database: ' + folder + '\nQuantity of files: ' + str(qnt_files) + '\nTotal time (in seconds): ' + str(time) + '\n\n'

    print(report)

    data_report.write(report)

  report = 'Final report: \nQuantity of files: ' + str(all_qnt_files) + '\nTotal time (in seconds): ' + str(all_time) + '\n\n'
  print(report)

  data_report.write(report)
  data_report.close()

