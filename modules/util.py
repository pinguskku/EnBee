import pandas as pd
import random
import csv
import os

# put your github tokens
# tokens = ['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', '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', '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', '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', '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']
tokens = ['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', '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', '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']

def select_token():
    value = random.randrange(1,10)

    if value % 2 == 0:
        return tokens[0]
    else:
        return tokens[1]


def save_to_csv(data, cols, path):
    df = pd.DataFrame(data, columns = cols)
    df.to_csv(path, index = False)


def save_to_csv_dict(data, path):
    with open(path,'w') as f:
        w = csv.writer(f)
        w.writerow(data.keys())
        w.writerow(data.values())

def get_empty_df():
    df = pd.DataFrame()
    return df

def read_from_csv(path):
    df = pd.read_csv(path, encoding='CP949')
    return df


def remove_blank(elements):
    result = [e for e in elements if e]
    return result


def divide_message_file(elements):
    result = [e for e in elements if e.endswith(".go")]
    return result


def remove_above_path(elements):
    result = []

    for element in elements:
        with_path_elements = element.split("/")
        file_name = with_path_elements[len(with_path_elements)-1]

        result.append(file_name)

    return result

# if you know some solutions to verify whether testfile or production file
# you can change this code by using your solution
# Basic rule is that filename includes "test" keyword
def test_file_verify(filename):
    if "_test.go" in filename:
        return True
    else:
        return False

def remove_duplicate(arr):
    result1 = set(arr)
    result2 = list(result1)

    return result2

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)