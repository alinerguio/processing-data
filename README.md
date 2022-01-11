# Processing Audio Files

## Goal

The goal is to download and organize the audios in order to facilitate the transcription and analysis. This repository was developed to be used in a research that resulted in other repositories, such as:

- [Google Cloud Speech to Text API use](https://github.com/alinerguio/google-transcript-tool)

- [Vosk API](https://github.com/alinerguio/vosk-transcript-tool)

## Requirements

To use this code, you'll need this requirements.   

[![Python Version](https://img.shields.io/badge/python-3.8.2-green)](https://www.python.org/downloads/release/python-382/)

When the repository is first cloned, use this commands:
```
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

Also, you will have to install [FFmpeg](https://www.ffmpeg.org/) to be able to process the files. 


### Hachoir 

The [library hachoir](https://hachoir.readthedocs.io/en/latest/metadata.html) wasn't used on any of the scripts, but it was used for the debugging of the audios. It might come in handy when having trouble assessing some characteristics of the data. The command line is: 
```
hachoir-metadata name_of_the_file
```

And the metadata is presented as the following example. 
```
Common:
- Duration: 7 sec 900 ms
- Channel: mono
- Sample rate: 48.0 kHz
- Bits/sample: 16 bits
- Compression rate: 1.0x
- Compression: Microsoft Pulse Code Modulation (PCM)
- Bit rate: 768.0 Kbit/sec
- MIME type: audio/x-wav
- Endianness: Little endian

```

## Execution
Then, every time you want to access, don't forget to activate you enviroment:
```
$ source env/bin/activate
```

## Pipeline

### Downloading

First of all, it is needed to acquire the data. For this test, some free Brazilian Portuguese databases were used. Those are downloaded using the *download_databases/download_files.py* is runned. The databases are the following: 

 - [Laps BM](https://gitlab.com/fb-audio-corpora/lapsbm16k/-/archive/master/lapsbm16k-master.zip) 
    
 - [Laps Mail](https://gitlab.com/fb-audio-corpora/lapsmail16k/-/archive/master/lapsmail16k-master.zip')

 - [VoxForge](http://www02.smt.ufrj.br/~igor.quintanilha/voxforge-ptbr.tar.gz)

There is also a database that needs to be downloaded manually, and it has many different languages in it. 

 - [Common Voice Portuguese](https://commonvoice.mozilla.org/pt/datasets)

### Processing 

The *adapting_databases.py* script assumes that the data is in the **dowload_databases/data** folder. The main goal of this script is to organize the dowloaded data to make the processing easier. Because of that, this processing is very specific for the databases already mentioned in the last session. It basically rearranges the audio files into a single folder with the name of the database. Also, it gets the respective transcriptions (in some cases they were in the txt format) and creates a dataframe with two columns: the original transcription and the file name. Also, it is created a dataframe with the original transcription without punctuation. 



