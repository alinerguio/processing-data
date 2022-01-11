import shutil
import requests 
import os 

# the common voice database can be found on this link: https://commonvoice.mozilla.org/pt/datasets
# it can't be downloaded automatically 

def download_multiple_datasets():
    files = ['voxforge-ptbr.tar.gz']
    # files = ['lapsbm-val.tar.gz', 'voxforge-ptbr.tar.gz', 'lapsbm-test.tar.gz', 'alcaim.tar.gz']
    for file in files:
        path = './data/' + file
        if not os.path.exists(path):
            print('starting download of ' + file)
            r = requests.get('http://www02.smt.ufrj.br/~igor.quintanilha/' + file)
            open(path, 'wb').write(r.content)
            print('downloaded ' + file)


def download_laps_datasets():
    urls = ['https://gitlab.com/fb-audio-corpora/lapsbm16k/-/archive/master/lapsbm16k-master.zip', 'https://gitlab.com/fb-audio-corpora/lapsmail16k/-/archive/master/lapsmail16k-master.zip']
    
    for url in urls:
        print('starting download of ' + url.split('/')[-1])
        r = requests.get(url)
        file = url.split('/')[-1]
        open('./data/' + file, 'wb').write(r.content)
        print('downloaded ' + file)


def unzip_all_data(directory):
    list_dir = os.listdir(directory)
    list_dir = [element for element in list_dir if '.DS_Store' not in element and '.' in element and not os.path.isdir(directory + element)]

    for element in list_dir:
        print('unziping ' + element)
        element_dir = directory + element
        element_new_dir = directory + element.split('.')[0]

        if not os.path.isdir(element_new_dir):
            os.makedirs(element_new_dir)

        shutil.unpack_archive(element_dir, element_new_dir)
        os.remove(element_dir)
        print('folder ' + element.split('.')[0] + ' created and zip erased')


def create_dir():
    if not(os.path.isdir('./data/')):
        os.makedirs('./data/')


if __name__ == '__main__':
    create_dir()
    download_laps_datasets()
    download_multiple_datasets()
    unzip_all_data('./data/')