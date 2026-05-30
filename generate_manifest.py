#!/usr/bin/env python3
"""
generate_manifest.py
────────────────────
リポジトリ内の画像・テキストファイルを走査して manifest.json を生成します。
index.html と同じディレクトリで実行してください。

使い方:
    python generate_manifest.py
    python generate_manifest.py --dir data          # data/ サブフォルダを対象にする場合
    python generate_manifest.py --dir data --out manifest.json
"""

import json
import os
import re
import argparse

# ファイル名として有効なパターン
# 画像: 数字 + p1 / p2  例) 1p1.png, 12p2.jpg
# テキスト: 数字 + v / a / n  例) 1v.txt, 3a.txt, 5n.txt
IMG_PATTERN = re.compile(r'^\d+p[12]\.(png|jpg|jpeg|gif|webp|svg)$', re.IGNORECASE)
TXT_PATTERN = re.compile(r'^\d+[van]\.(txt|text)$', re.IGNORECASE)


def collect_files(base_dir: str) -> list[str]:
    result = []
    for fname in sorted(os.listdir(base_dir)):
        if IMG_PATTERN.match(fname) or TXT_PATTERN.match(fname):
            # index.html からの相対パスで記録
            rel = fname if base_dir == '.' else os.path.join(base_dir, fname).replace('\\', '/')
            result.append(rel)
    return result


def main():
    parser = argparse.ArgumentParser(description='emoji dictionary 用 manifest.json を生成します')
    parser.add_argument('--dir', default='.', help='データファイルが置かれているディレクトリ（デフォルト: カレント）')
    parser.add_argument('--out', default='manifest.json', help='出力先 JSON ファイル名（デフォルト: manifest.json）')
    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(f'エラー: ディレクトリ "{args.dir}" が見つかりません')
        return

    files = collect_files(args.dir)

    if not files:
        print(f'警告: "{args.dir}" に対象ファイルが見つかりませんでした')
        print('  画像: [番号]p1.png / [番号]p2.png')
        print('  テキスト: [番号]v.txt / [番号]a.txt / [番号]n.txt')
        return

    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(files, f, ensure_ascii=False, indent=2)

    print(f'✓ {len(files)} 件のファイルを {args.out} に書き出しました')
    for fp in files:
        print(f'  {fp}')


if __name__ == '__main__':
    main()
