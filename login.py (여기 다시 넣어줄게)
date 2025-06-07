import tkinter as tk
from tkinter import messagebox

# 사용자 정보 파일 경로
USER_FILE = "users.txt"

# 사용자 정보 로드 함수
def load_user_data():
    users = {}
    try:
        with open(USER_FILE, "r") as f:
            for line in f:
                id_, pw = line.strip().split(":")
                users[id_] = pw
    except FileNotFoundError:
        pass  # 파일 없으면 빈 딕셔너리 유지
    return users

# 사용자 정보 저장 함수 (추가)
def save_user_data(users):
    with open(USER_FILE, "w") as f:
        for id_, pw in users.items():
            f.write(f"{id_}:{pw}\n")



