import argparse
import re
from collections import Counter
import chardet


def load_data(filepath):
    return open(filepath, 'rb').read()


def get_most_frequent_words(text):
    return Counter(text.split(' ')).most_common((10))


def decode_text(text_bytes):
    most_common_charsets = ['utf8', 'cp1251']
    for charset in most_common_charsets:
        try:
            return text_bytes.decode(charset)
        except ValueError:
            pass

    try:
        result = chardet.detect(text_bytes)
        return text_bytes.decode(result['encoding'])
    except ValueError:
        return


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-f', action='store',
        dest='filepath',
        help='Filepath with text, "book.txt" by default',
        default='book.txt'
    )

    return parser.parse_args()


def print_list_of_tuples(list_of_tuples):
    for i_tuple in list_of_tuples:
        print('{:>6} : {} '.format(i_tuple[0], i_tuple[1]))


if __name__ == '__main__':
    params = parse_arguments()

    try:
        text_bytes = load_data(params.filepath)
    except ValueError as e:
        print('Не могу прочитать данные из файла {}'.format(params.filepath))
        exit()
    except OSError as e:
        print('Файл {} не существует '.format(params.filepath))
        exit()

    text = decode_text(text_bytes)
    if text is None:
        raise ValueError('Не могу декодировать данные')

    text = re.sub(r'([^\w\d]|_)+', ' ', text)
    try:
        most_common_word_list = (get_most_frequent_words(text))
    except ValueError:
        print('Не могу посчитать')

    print_list_of_tuples(most_common_word_list)
