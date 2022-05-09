import os
import re
import random
from typing import List, Tuple

import jamotools
import yaml


class Typo:

    def __init__(self) -> None:

        with open("/".join(os.path.abspath(__file__).split("/")[:-1]) + "/config.yaml", "r") as f:
            self.cfg = yaml.load(f, Loader=yaml.FullLoader)

        self.dx = [0, 0, -1, 1]
        self.dy = [-1, 1, 0, 0]
        self.key_type = None  # [ko, en_up, en_lo, symbol]
        self.list_key = []

    def convert(self, seq: str, k: int = 1) -> str:

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
            candidate_keys = []  # 후보키 리스트 (타겟키가 변경 될 수 있는 후보키 리스트)

            if not self.key_type:  # 타겟키가 공백이거나 명시특수문자인 경우
                continue

            if self.key_type == "symbol":
                candidate_keys.append(self.cfg["dict_symbol"][target_key])
            else:
                # 타겟키 주변에 위치한 키들을 후보키 리스트에 추가
                candidate_keys: List[str] = self._get_near_keys(idx_row, idx_col)
                # [한글] 쉬프트 키와 같이 입력 시 쌍모음 또는 쌍자음이 되는 경우 후보키 리스트에 추가
                if self.key_type == "ko":
                    if target_key in self.cfg["dict_shift_on"]:
                        candidate_keys.append(self.cfg["dict_shift_on"][target_key])
                    # 후보키 중 위와 같은 경우 후보키 리스트에 추가
                    # list_temp = []
                    # for candidate_key in candidate_keys:
                    #     if candidate_key in self.cfg["dict_shift_on"]:
                    #         list_temp.append(self.cfg["dict_shift_on"][candidate_key])
                    # candidate_keys += list_temp
                # [한글] 이중모음인 경우
                if target_key in self.cfg["dict_diphthong"]:
                    candidate_keys += self.cfg["dict_diphthong"][target_key]
                # [영어] 대소문자 변환 후 후보키 리스트에 추가
                elif self.key_type == "en_up":
                    candidate_keys.append(target_key.lower())
                elif self.key_type == "en_lo":
                    candidate_keys.append(target_key.upper())
            
            conversion_key = random.sample(candidate_keys, 1)[0]  # 후보키 중 하나를 변경키로 설정
            jamo[idx] = conversion_key  # 타겟키 변경

        return jamotools.join_jamos(jamo)

    def _get_key_index(self, target_key: str) -> Tuple[int, int]:

        # 타겟키 한글, 영어 체크
        if re.match(r"[a-z]", target_key):
            self.key_type = "en_lo"
            self.list_key = self.cfg["list_key_en_lower"]
        elif re.match(r"[A-Z]", target_key):
            self.key_type = "en_up"
            self.list_key = self.cfg["list_key_en_upper"]
        elif re.match(r"[ㄱ-ㅎㅏ-ㅣ]", target_key):
            self.key_type = "ko"
            self.list_key = self.cfg["list_key_ko"]
            if target_key in self.cfg["dict_shift_off"]:  # 쌍모음 또는 쌍자음인 경우
                target_key = self.cfg["dict_shift_off"][target_key]
        elif target_key in self.cfg["dict_symbol"]:
            self.key_type = "symbol"

        # 타겟키의 인덱스 (키보드 자판 위치) 검색
        for idx_row in range(len(self.list_key)):
            for idx_col, key in enumerate(self.list_key[idx_row]):
                if key == target_key:
                    return idx_row, idx_col

        return -1, -1

    def _get_near_keys(self, idx_row: int, idx_col: int) -> List[str]:

        list_result: List[str] = []
        target_key = self.list_key[idx_row][idx_col]

        if idx_row == -1 and idx_col == -1:
            return list_result

        # 타겟키 상하좌우 키 검색
        for i in range(4):
            x = idx_row + self.dx[i]
            y = idx_col + self.dy[i]
            if x < 0 or y < 0:
                continue
            try:
                temp_key = self.list_key[x][y]
                # [한글] 타겟키와 변경키가 둘 다 자음이거나 모음인 경우
                if self.key_type == "ko":
                    if target_key in self.cfg["list_ja"] and temp_key in self.cfg["list_ja"]:
                        list_result.append(temp_key)
                    elif target_key in self.cfg["list_mo"] and temp_key in self.cfg["list_mo"]:
                        list_result.append(temp_key)
                else:
                    list_result.append(temp_key)
            except IndexError:  # 타겟키가 키보드 자판에서 끝에 위치한 경우
                continue

        return list_result
