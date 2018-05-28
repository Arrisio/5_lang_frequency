import argparse
import re
from collections import Counter
import chardet


def load_data(filepath):
    with open(filepath, 'r', encoding='UTF8') as file_handler:
        return file_handler.read()


def get_most_frequent_words(text, number_of_words):
    word_list = re.sub(r'([^\w\d]|_)+', ' ', text).split(' ')
    return Counter(word_list).most_common(number_of_words)


def decode_text(text_bytes):
    most_common_charsets = ['utf8', 'cp1251']
    for charset in most_common_charsets:
        try:
            return text_bytes.decode(charset)
        except ValueError:
            pass

    try:
        return text_bytes.decode(chardet.detect(text_bytes)['encoding'])
    except ValueError:
        raise ValueError('Не могу декодировать данные')


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-f', action='store',
        dest='filepath',
        help='Filepath with text, "book.txt" by default',
        default='book.txt'
    )

    parser.add_argument(
        '-n', action='store',
        type=int,
        dest='number_of_words',
        help='Number of most common words, by default',
        default=10
    )

    return parser.parse_args()


def print_list_of_tuples(list_of_tuples):
    for i_tuple in list_of_tuples:
        print('{:>6} : {} '.format(i_tuple[0], i_tuple[1]))


if __name__ == '__main__':
    params = parse_arguments()

    try:
        text_bytes = load_data(params.filepath)
    except ValueError:
        exit('Не могу прочитать данные из файла {}'.format(params.filepath))
    except OSError:
        exit('Файл {} не существует '.format(params.filepath))

    text = decode_text(text_bytes)

    print_list_of_tuples(get_most_frequent_words(text, params.number_of_words))
