import math
# from sklearn.mixture import GMM
# from sklearn import datasets
import utils

# iris = datasets.load_iris()
# print iris.data
# print iris.target

TAGS = [
    "weekly_report",
    "sound",
    "fab",
    "ir",
    "hci",
    "study",
    "app",
    "hardware",
    "business",
    "system"
]
TRAIN_DATA_TAG_FILE_PATH = 'public/data/train_data_tag.csv'

def train_tags():
    tags = []
    tags_n_array = []
    f = open(TRAIN_DATA_TAG_FILE_PATH, 'r')
    for line in f:
        # tags_tmp = []
        # tags_tmp = line.split(',')
        # for tag in TAGS:
        for i, tag in enumerate(TAGS):
            if tag in line.lower():
                # tags_tmp.append(tag)
                tags.append([tag])
                tags_n_array.append(i)
                break
        else:
    	    tags.append(['others'])
    	    tags_n_array.append(len(TAGS))
        # if len(tags_tmp) >= 2 and not 'system' in str(tags_tmp) :
        # if 'sound' in str(tags_tmp):
            # tags.append(tags_tmp)
    utils.write2csv('script/check_tags.csv', tags)
    return tags_n_array

def value(i):
	if 0 <= i and i < len(TAGS):
	    return TAGS[i]
	else:
		return "others"
