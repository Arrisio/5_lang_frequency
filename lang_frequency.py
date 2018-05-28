import argparse
import re
from collections import Counter
import chardet


def load_data(filepath):
    with open(filepath, 'rb') as file_handler:
        text_bytes = file_handler.read()

    try:
        return text_bytes.decode('utf8')
    except ValueError:
        pass

    return text_bytes.decode(chardet.detect(text_bytes)['encoding'])


def get_most_frequent_words(text, number_of_words):
    word_list = re.sub(r'([^\w]|_)+', ' ', text).split()
    return {k: v for (k, v) in Counter(word_list).most_common(number_of_words)}


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


def print_words_freq(list_of_words_freq):
    for word, freq in list_of_words_freq.items():
        print('{:>6} : {} '.format(word, freq))


if __name__ == '__main__':
    params = parse_arguments()

    try:
        text = load_data(params.filepath)
    except (ValueError, TypeError):
        exit('Не могу прочитать текст из файла {}'.format(params.filepath))
    except OSError:
        exit('Файл {} не существует '.format(params.filepath))

    print_words_freq(get_most_frequent_words(text, params.number_of_words))
