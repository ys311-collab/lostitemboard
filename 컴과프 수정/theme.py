from tkinter import ttk
from ttkthemes import ThemedTk
import lostandfound
import pygame

pygame.mixer.init()

colors = ['#555B6E', '#89B0AE', '#BEE3DB','#FAF9F9','#FFD6BA']

theme_bgm = {
    "basic": "bgm_basic.mp3",
    "aqua": "bgm_aqua.mp3",
    "cozy": "bgm_cozy.mp3",
    "sunny": "bgm_sunny.mp3"
}

# 배경음악 재생 함수
def play_music(file_path):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)  # 반복 재생

def basic_theme():
    global colors
    colors = ['#555B6E', '#89B0AE', '#BEE3DB','#FAF9F9','#FFD6BA']
    lostandfound.apply_style()
    lostandfound.refresh_ui()
    play_music(theme_bgm["basic"])
    

def aqua_theme():
    global colors
    colors = ['#023436','#037971','#049A8F','#00BFB3',"#B3EDE9"]
    lostandfound.apply_style()
    lostandfound.refresh_ui()
    play_music(theme_bgm["aqua"])

def cozy_theme():
    global colors
    colors = ['#FFC4EB','#FFE4FA','#F1DEDC','#E1DABD','#ABC798']
    lostandfound.apply_style()
    lostandfound.refresh_ui()
    play_music(theme_bgm["cozy"])
def sunny_theme():
    global colors
    colors = ["#5A4DEE", "#E9D349","#35FC66","#FA3DE1","#82B4F6"]
    lostandfound.apply_style()
    lostandfound.refresh_ui()
    play_music(theme_bgm["sunny"])

#print(ThemedTk().get_themes())
