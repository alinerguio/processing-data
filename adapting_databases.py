import os 
import shutil
import pandas as pd


def remove_punc(sentence):
    # subfunction used in functions in order to remove punctuation from original transcripts
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    
    for char in sentence:
        if char in punc:
            sentence = sentence.replace(char, '')
            
    return sentence


def adapt_laps_database(base_dir, list_dir):
    # function to adapt the organization folder schema of both laps database 
    # this was applied in order to facilitate the implementation of the transcriptions algorithms 
    # the result is all files in only one folder - without subfolders
    new_dir = './data/adapted_laps_dataset/'

    if list_dir == []:
        base_dir = './download_databases/data/'
        list_dir = os.listdir(base_dir)
        list_dir = [element for element in list_dir if '.' not in element and 'laps' in element]
        if not os.path.isdir(new_dir):
            os.makedirs(new_dir)

    for element in list_dir:
        if '.wav' in element or '.txt' in element: 
            shutil.move(base_dir + element, new_dir + element)
            # shutil.move(base_dir + element, new_dir + 'laps_' + element)
        elif '.' not in element:
            dir_to_explore = base_dir + element + '/'
            adapt_laps_database(dir_to_explore, os.listdir(dir_to_explore))


def adapt_voxforge_database():
    # function to adapt the organization folder schema of voxforge database
    # this was applied in order to facilitate the implementation of the transcriptions algorithms
    # the result is all files in only one folder - without subfolders
    new_dir = './data/adapted_voxforge_dataset/'
    base_dir = './download_databases/data/'

    list_dir = os.listdir(base_dir)
    list_dir = [element for element in list_dir if 'adapted' not in element and '.' not in element and 'voxforge' in element]
    
    if not os.path.isdir(new_dir):
        os.makedirs(new_dir)

    base_dir = base_dir + list_dir[0]
    list_dir = os.listdir(base_dir)
    list_dir = [element for element in list_dir if '.' not in element]

    for folder in list_dir:
        sub_dir = base_dir + '/' + folder + '/'

        if not os.path.isdir(sub_dir + 'wav/'):
            sub_list_dir = os.listdir(sub_dir)
            sub_list_dir = [element for element in sub_list_dir if '.wav' in element]
            transcriptions_dir = sub_dir + 'prompts-original'
            # new_transcriptions_dir = sub_dir + folder + '_prompts-original'
        else:
            sub_list_dir = os.listdir(sub_dir + 'wav/')
            transcriptions_dir = sub_dir + 'etc/prompts-original'
            # new_transcriptions_dir = sub_dir + 'etc/' + folder + '_prompts-original'
            sub_dir = sub_dir + 'wav/' 

        for element in sub_list_dir:
            shutil.move(sub_dir + element, new_dir + 'voxforge_' + folder + '_' + element)

        transcriptions_file = open(transcriptions_dir, "r")
        transcriptions = transcriptions_file.readlines()
        
        for transcription in transcriptions:
            transcription = transcription.split()
            file_name = 'voxforge_' + folder + '_' + transcription[0] + '.txt'
            transcription = ' '.join(transcription[1:])
            
            file = open(new_dir + file_name, "w")
            file.write(transcription)
            file.close()

        # shutil.move(transcriptions_dir, new_transcriptions_dir)


def adapt_common_voice(base_dir, list_dir):
    # gets the slice of the data that was validated (and move folders)
    # get the slice of the data that was validated in the dataset (metadata and original transcription)
    # creates the non-punctuated original transcript column in the dataset

    # working only with validated data
    new_dir = './data/adapted_commonvoice_dataset/'

    if base_dir == '':
        base_dir = './download_databases/data/'
        list_dir = os.listdir(base_dir)
        list_dir = [element for element in list_dir if ('common-voice' in element or 'cv-corpus' in element) and ('.tar.gz' not in element and '.zip' not in element)]
        
        base_dir = base_dir + list_dir[0] + '/pt/'

        if not os.path.isdir(new_dir):
            os.makedirs(new_dir)

    validated_dataset = 'validated.tsv'

    if validated_dataset in list_dir and 'clips' in list_dir:
        data = pd.read_csv(base_dir + '/' + validated_dataset, sep='\t', header=0)
        base_file_dir = base_dir + 'clips/'

        original_data = data[['path', 'sentence']]
        original_data['sentence'] = original_data['sentence'].apply(remove_punc)

        files_list = data[['path']].stack().tolist()

        for file in files_list: 
            shutil.move(base_file_dir + file, new_dir + file)

        shutil.move(base_dir + validated_dataset, './data/common-voice-'  + validated_dataset)
        original_data.to_csv('./data/common-voice-validated-without-punct.csv', index=False)

    else: 
        list_dir = [element for element in list_dir if os.path.isdir(base_dir + element)]
        for element in list_dir:
            dir_to_explore = base_dir + element + '/'
            adapt_common_voice(dir_to_explore, os.listdir(dir_to_explore))


def create_datasets(databases):
    # transforms the metadata into datasets - in order to analyse it 
    # originaly applied to voxforge and laps 
    # also creates the non-punctuated original transcript column 

    data = pd.DataFrame(columns=['file','transcriptions'])
    data_without_punct = pd.DataFrame(columns=['file','transcriptions'])
    base_dir = './data/'

    if not os.path.isdir(base_dir):
        os.makedirs(base_dir)

    for database in databases:
        list_dir = os.listdir(base_dir + database)
        list_dir = [element for element in list_dir if '.txt' in element]
        for file in list_dir:
            txt_dir = base_dir + database + '/' + file
            transcription = open(txt_dir, "r").read()
            data_file = pd.DataFrame(data={'file':[file.split('.')[0] + '.wav'], 'transcriptions':[transcription]})
            os.remove(txt_dir)

            data_file_wp = pd.DataFrame(data={'file':[file.split('.')[0] + '.wav'], 'transcriptions':[remove_punc(transcription)]})

            data = data.append(data_file, ignore_index=True)
            data_without_punct = data_without_punct.append(data_file_wp, ignore_index=True)

        data.to_csv(base_dir + database + '.csv', index=False)
        data_without_punct.to_csv(base_dir + database + '_without_punct.csv', index=False)


if __name__ == '__main__':
    adapt_voxforge_database()
    adapt_laps_database('', [])
    adapt_common_voice('', [])

    databases = ['adapted_voxforge_dataset', 'adapted_laps_dataset']
    create_datasets(databases)
