import tkinter as tk
import lostInput as ml

losts=tk.Tk()
lost_list=[] #각 분실물의 이름을 저장하는 리스트

class lost:
    def __init__(self, name, mw):
        self.name=name
        ml.showState(mw)

ml.showTitle()
ml.lostInput()

# for lost_item in lost_list:
#     lost(lost_item, losts)

losts.mainloop()