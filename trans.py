#! python3
# _*_ coding:utf-8 _*_

import os
import re
import textwrap
import requests
import argparse
from Color.color import Colored
from checkcoding import file_encoding

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0'
}

class TranslatorBing:
    def __init__(self, args):
        self.args = args
        self.url = 'https://cn.bing.com/ttranslatev3?isVertical=1&&IG=63E3E72E23044A0A9286E3C149F19F77&IID=translator.5028.2'
        self.color = Colored()
        self.flag = 0

    def create_data(self, language):
        self.data = {
            'fromLang': 'auto-detect',
            'text': self.args.text[0],
            'to': language
        }

    def is_Chinese(self):
        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
        mo = zh_pattern.search(self.args.text[0])
        if mo:
            return True
        else:
            return False

    def show_text(self, width1, width2):
        if self.args.dir[0]:
            origin = textwrap.fill('原文: ' + self.args.text[0], width=width1)
            target = textwrap.fill('译文: ' + self.trans_text, width=width2)
            lines = ['\n\n', origin, '\n', target]
            coding = file_encoding(self.args.file[0])
            with open(self.args.dir[0], 'a', encoding=coding) as f:
                f.writelines(lines)

        print('')
        print(textwrap.fill(self.origin, width=width1))
        print(textwrap.fill(self.target, width=width2))

    def translate(self):
        if self.is_Chinese():
            self.create_data('en')
            self.flag = 1
        else:
            self.create_data('zh-Hans')

        response = requests.post(self.url, data=self.data, headers=headers)
        result = response.json()
        self.trans_text = result[0].get('translations')[0].get('text')
        self.origin = '原文: ' + self.color.cyan(self.args.text[0])
        self.target = '译文: ' + self.color.green(self.trans_text)
        if self.flag == 1:
            self.show_text(55, 90)
        else:
            self.show_text(90, 55)


def run():
    parse = argparse.ArgumentParser(
        prog='trans',
        description='必应在线翻译命令行版'
    )
    parse.add_argument(
        '-t',
        '--text',
        nargs=1,
        default=[''],
        help='指定需要翻译的语句'
    )
    parse.add_argument(
        '-f',
        '--file',
        nargs=1,
        help='指定txt文件的路径, 按行翻译整个txt文件'
    )
    parse.add_argument(
        '-d',
        '--dir',
        nargs=1,
        default=[''],
        help='指定一个txt文件路径，将翻译结果保存到该txt文件'
    )

    args = parse.parse_args()
    # 从TXT文件获取要翻译的句子
    if args.file:
        path = args.file[0]
        if not (os.path.exists(path) and path.endswith('.txt')):
            print(f'ERROR: <{path}>不存在或不是TXT文件. 请使用trans -h 查看用法')
            return
        try:
            coding = file_encoding(path)    # 获取文件编码
            f = open(path, 'r', encoding=coding)
            for line in f.readlines():
                if len(line) == 0 or line == '\n':
                    continue
                args.text[0] = line
                t1 = TranslatorBing(args)
                t1.translate()
            return
        except:
            print(f'ERROR: 无法打开<{path}>, 请检查文件是否损坏或为空!')
            return

    if args.text[0] == '':
        print('INFO - 没有要翻译的句子, 请使用trans -h 查看用法')
        return
    t2 = TranslatorBing(args)
    t2.translate()

if __name__ == '__main__':
    run()
