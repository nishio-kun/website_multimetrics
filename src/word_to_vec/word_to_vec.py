"""
テキスト中の文章を形態素解析するモジュール。
"""
import argparse
import os
import pathlib
import sys

from elasticsearch import Elasticsearch
from gensim.models import word2vec
from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter
from janome.tokenfilter import (CompoundNounFilter, LowerCaseFilter,
                                POSStopFilter)
from janome.tokenizer import Tokenizer


current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + '/../')


import settings
from utils.es_util import download_all


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', help='Elasticsearch index.')
    parser.add_argument('-i', '--input-file', help='Input file.')
    parser.add_argument('-o', '--output-file', required=True,
                        help='Output file.')
    parser.add_argument('-v', action='store_true', help='Verbose mode.')
    args = parser.parse_args()
    return args


def tokenize(text):
    """
    文章を分かち書きします。
    """
    exclusion = ['助詞', '助動詞', '記号']
    char_filters = [UnicodeNormalizeCharFilter()]
    tokenizer = Tokenizer()
    token_filters = [CompoundNounFilter(), POSStopFilter(exclusion),
                     LowerCaseFilter()]
    analyzer = Analyzer(char_filters, tokenizer, token_filters)

    ret = []
    for sentense in text.split('。')[:-1]:
        ret.append([])
        for token in analyzer.analyze(sentense.rstrip()):
            ret[-1].append(token.base_form)
    return ret


def main():
    args = parse_args()
    if not args.output_file.endswith('.model'):
        print('error: the extension of the output file is ".model"')
        return

    if args.index:
        client = Elasticsearch(settings.HOST)
        articles = download_all(client, args.index, 'body')
        tokens = []
        for text in articles:
            if text:
                tokens.extend(tokenize(text))
    elif args.input_file:
        text = ''
        with open(args.input_file) as f:
            for line in f:
                text += line.rstrip()
        tokens = tokenize(text)
    else:
        print('error: require index or input file.')
        return

    if args.v:
        print(tokens)

    model = word2vec.Word2Vec(tokens, sg=1, size=100, min_count=1, window=10,
                              hs=1, negative=0)

    model.save(args.output_file)
    print('success')


if __name__ == '__main__':
    main()
