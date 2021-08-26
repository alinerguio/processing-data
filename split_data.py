import pandas as pd
import json 

def split_info_archives(len_buckets, archive_name):
    # in order to make the testing easier 
    file = open("../" + archive_name + ".txt", "r")
    dict_with_files = file.read()
    dict_with_files = json.loads(dict_with_files)

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


def split_into_gender_commonvoice():
	data = pd.read_csv('./data/validated.tsv', sep='\t', header=0)
	data['path'] = 'adapted_commonvoice_dataset/' + data['path']
	list_of_female = data[data['gender'] == 'female'].path.tolist()
	new_dict_female = {} 

	for element in list_of_female:
	    file_name = element.split('.')[0] + '.wav'
	    if file_name in dict_with_files.keys():
	        new_dict_female[file_name] = dict_with_files[file_name]

	file = open('../female_adapted_commonvoice.txt', 'w')
	file.write(str(new_dict_female).replace("'", '"'))
	file.close()

	list_of_others = data[data['gender'] != 'female'].path.tolist()

	new_dict_others = {} 

	for element in list_of_others:
	    file_name = element.split('.')[0] + '.wav'
	    new_dict_others[file_name] = dict_with_files[file_name]

	file = open('../others_adapted_commonvoice.txt', 'w')
	file.write(str(new_dict_others).replace("'", '"'))
	file.close()


if __name__ == '__main__':
	split_info_archives(500, 'others_adapted_cv')