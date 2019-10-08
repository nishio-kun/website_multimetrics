"""
A3RT を扱うモジュール。
"""
import sys

import requests

sys.path.append('../')
import settings


TEXT_SUMMARIZATION_API = settings.TEXT_SUMMARIZATION_API
TEXT_SUMMARIZATION_API_KEY = settings.TEXT_SUMMARIZATION_API_KEY


def text_summarize(sentences, linenumber=1, separation='。'):
    """
    文章を要約します。
    """

    data = {'apikey': TEXT_SUMMARIZATION_API_KEY,
            'sentences':sentences,
            'linenumber': linenumber,
            'separation': separation}
    response = requests.post(TEXT_SUMMARIZATION_API, data=data)

    result = response.json()
    if result['status'] == 0:
        return result['summary']
    else:
        print('error: ', result['message'])
        return


if __name__ == '__main__':
    def output(title, sentences, result):
        import pprint

        print('** ' + title + ' **')
        print(sentences)
        print()
        pprint.pprint(result)
        print()

    print('A3RT TEST\n')

    sentences = '昨日は六甲全山縦走に行く予定で、しかし全く起きられず断念してグランフロントでお茶しながら仕事をしたりこれを読んだりしていた。今日こそは行くぞと思っていたのだが、タイマーをかけていなかったせいで気がついたら8時であった。というわけですごく今日の午前はふてくされていたんだけど、お風呂に入って読書をするのってやってみたいなあ、でも本が濡れるのはいやだなぁ…とか逡巡していたのを思い切って実行することにしてみた。なるほどこれは楽しいかもしれない。ハイアットの大きなバスタブ万歳である。バスケア商品に凝りたくなってくる。1時間半ぐらいで残り半分を読み終えて、いろいろさっぱりした。できなかったことを悔やんでもしょうがない。やろうとしていたことができなくても、他のことをしてみればよい。他のことは、もともとやろうとしていたことよりも達成感は低いのだけれど、それでもやらないよりはずっと良い。'

    output('文章要約', sentences, text_summarize(sentences))
