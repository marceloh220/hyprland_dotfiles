#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from typing import List, Tuple

from whatthedouchesay_ascii_art import BOLSONARO_ASCII, TRUMP_ASCII
from whatthedouchesay_generator import douche_generator

def show_douche_trump() -> str:
    return TRUMP_ASCII


def show_douche_bolsonaro() -> str:
    return BOLSONARO_ASCII

def split_msg(msg: str) -> Tuple[List[str], int]:
    words = msg.split()
    total_words = len(words)
    sections = [
        " ".join(words[: total_words // 3]),
        " ".join(words[total_words // 3 : 2 * total_words // 3]),
        " ".join(words[2 * total_words // 3 :]),
    ]
    msg_size = len(max(sections, key=len)) if sections else 0
    return sections, msg_size

def _render_message_border(prefix: str, msg_len: int) -> None:
    print(f"{prefix}    {'-' * (msg_len + 4)}")


def _render_message_line(prefix: str, text: str, msg_len: int) -> None:
    padding = " " * (msg_len + 1 - len(text))
    print(f"{prefix}   |  {text} {padding}|")


def douche_says(douche: str, phrase: str) -> None:
    msg_list, msg_len = split_msg(phrase)
    bubble_lines = {5: 0, 6: 1, 7: 2}

    for line_number, line in enumerate(douche.splitlines(), start=1):
        if line_number in (4, 8):
            _render_message_border(line, msg_len)
            continue

        if line_number in bubble_lines:
            msg_index = bubble_lines[line_number]
            _render_message_line(line, msg_list[msg_index], msg_len)
            continue

        print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador de frases aleatórias de douches famosos.")
    parser.add_argument("-m", "--mode", choices=["desmotivational", "dicks", "todes"], default="todes", help="Modo de geração de frases.")
    parser.add_argument("-d", "--douche", choices=["trump", "bolsonaro"], default="trump", help="Douche para usar na arte ASCII.")
    args = parser.parse_args()
    
    douche = ""
    quote = ""
    if args.douche == "trump":
        douche = show_douche_trump()
        quote = douche_generator(args.mode, "en")
    elif args.douche == "bolsonaro":
        douche = show_douche_bolsonaro()
        quote = douche_generator(args.mode, "pt-br")
    
    douche_says(douche, quote)
