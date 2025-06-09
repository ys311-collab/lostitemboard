from PIL import Image, ImageTk

#이미지 경로와 프레임을 받았을 때 이미지를 표시해주는 함수
def load_image(img_path, frame):
    try:
        image = Image.open(img_path)
        image = image.resize((100, 100))  #이미지 크기 조정
        return ImageTk.PhotoImage(image, master=frame)
    except Exception as e:  #예외 처리
        print(e)
        return None

#이미지를 컴퓨터 파일에서 선택하게 하는 함수수
def select_image():
    from tkinter import filedialog
    img_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
    return img_path
