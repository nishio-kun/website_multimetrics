"""
単語を可視化するモジュール。
"""
import argparse

from gensim.models import word2vec
from matplotlib import pyplot as plt
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties
import numpy as np
from sklearn.manifold import TSNE


rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro']


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', required=True,
                        help='Input file.')
    parser.add_argument('-v', action='store_true', help='Verbose mode.')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    word2vec_model = word2vec.Word2Vec.load(args.input_file)

    # 単語の一覧を取得する
    vocab_thresh = 20
    vocabs = []
    for word, vocab_obj in word2vec_model.wv.vocab.items():
        if vocab_obj.count >= vocab_thresh:
            vocabs.append(word)

    if args.v:
        print(vocabs)
    print(f'N = {len(vocabs)}')

    # emb_tuple = tuple([word2vec_model[v] for v in vocabs])
    emb_tuple = tuple([word2vec_model.wv[v] for v in vocabs])
    X = np.vstack(emb_tuple)

    model = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    model.fit_transform(X)

    # matplotlibで t-SNEの図を描く
    skip = 0
    limit = len(vocabs)

    plt.figure(figsize=(40,40))
    plt.scatter(model.embedding_[skip:limit, 0], model.embedding_[skip:limit, 1])

    count = 0
    for label, x, y in zip(vocabs, model.embedding_[:, 0], model.embedding_[:, 1]):
        count +=1
        if(count < skip): continue
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
        if(count == limit): break

    plt.show()


if __name__ == '__main__':
    main()
