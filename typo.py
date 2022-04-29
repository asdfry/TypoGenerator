import re
import random
from typing import List, Tuple

import jamotools


class Typo:
    def __init__(self) -> None:

        self.list_key_ko = [
            ["ㅂ", "ㅈ", "ㄷ", "ㄱ", "ㅅ", "ㅛ", "ㅕ", "ㅑ", "ㅐ", "ㅔ"],
            ["ㅁ", "ㄴ", "ㅇ", "ㄹ", "ㅎ", "ㅗ", "ㅓ", "ㅏ", "ㅣ"],
            ["ㅋ", "ㅌ", "ㅊ", "ㅍ", "ㅠ", "ㅜ", "ㅡ"],
        ]
        self.list_key_en_upper = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["Z", "X", "C", "V", "B", "N", "M"],
        ]
        self.list_key_en_lower = [
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
            ["z", "x", "c", "v", "b", "n", "m"],
        ]
        self.dict_shift = {"ㅂ": "ㅃ", "ㅈ": "ㅉ", "ㄷ": "ㄸ", "ㄱ": "ㄲ", "ㅅ": "ㅆ", "ㅐ": "ㅒ", "ㅔ": "ㅖ"}
        self.list_ja = ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
        self.list_mo = ["ㅏ", "ㅑ", "ㅓ", "ㅕ", "ㅗ", "ㅓ", "ㅜ", "ㅠ", "ㅡ", "ㅣ"]
        self.dx = [0, 0, -1, 1]
        self.dy = [-1, 1, 0, 0]
        self.key_type = None
        self.list_key = None

    def convert(self, seq: str, k: int = 1):

        if len(seq) < 1:
            return seq

        jamo: List[str] = list(jamotools.split_syllables(seq))

        try:
            target_ids: List[int] = random.sample(range(len(jamo)), k)
        except:  # 바꾸고 싶은 자모 수가 원본의 자모 길이를 넘는 경우
            target_ids: List[int] = random.sample(range(len(jamo)), 1)

        for idx in target_ids:
            target_key = jamo[idx]
            idx_row, idx_col = self._get_key_index(target_key)

            if not self.key_type:
                continue

            # 타겟키 주변에 위치한 키들을 후보키 리스트에 추가
            candidate_keys: List[str] = self._get_near_keys(idx_row, idx_col)

            # [한글] 쉬프트 키와 같이 입력 시 쌍모음 또는 쌍자음이 되는 경우 후보키 리스트에 추가
            if self.key_type == "ko" and target_key in self.dict_shift:
                candidate_keys.append(self.dict_shift[target_key])
            # [영어] 대소문자 변환 후 후보키 리스트에 추가
            elif self.key_type == "en_up":
                candidate_keys.append(target_key.lower())

            near_key = random.sample(candidate_keys, 1)[0]  # 후보키 중 하나를 변경키로 설정

            # 타겟키 변경
            if self.key_type == "ko":  # [한글] 타겟키와 변경키가 둘 다 자음이거나 모음이면 변경)
                if target_key in self.list_ja and near_key in self.list_ja:
                    jamo[idx] = near_key
                elif target_key in self.list_mo and near_key in self.list_mo:
                    jamo[idx] = near_key
            else:
                jamo[idx] = near_key

        return jamotools.join_jamos(jamo)

    def _get_key_index(self, target_key: str) -> Tuple[int, int]:

        # 타겟키 한글, 영어 체크
        if re.match(r"[a-z]", target_key):
            self.key_type = "en_lo"
            self.list_key = self.list_key_en_lower
        elif re.match(r"[A-Z]", target_key):
            self.key_type = "en_up"
            self.list_key = self.list_key_en_upper
        elif re.match(r"[ㄱ-ㅎㅏ-ㅣ]", target_key):
            self.key_type = "ko"
            self.list_key = self.list_key_ko

        # 타겟키의 인덱스 (키보드 자판 위치) 검색
        for idx_row in range(len(self.list_key)):
            for idx_col, key in enumerate(self.list_key[idx_row]):
                if key == target_key:
                    return idx_row, idx_col

        return -1, -1

    def _get_near_keys(self, idx_row: int, idx_col: int) -> List[str]:

        list_result: List[str] = []

        # 타겟키 상하좌우 키 검색
        for i in range(4):
            x = idx_row + self.dx[i]
            y = idx_col + self.dy[i]
            if x < 0 or y < 0:
                continue
            else:
                try:
                    list_result.append(self.list_key[x][y])
                except IndexError:  # 타겟키가 키보드 자판에서 끝에 위치한 경우
                    continue

        return list_result
