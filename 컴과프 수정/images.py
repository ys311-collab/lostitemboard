from PIL import Image, ImageTk

def load_image(img_path, frame):
    try:
        image = Image.open(img_path)
        # image = image.resize((100, 100))
        return ImageTk.PhotoImage(image, master=frame)
    except Exception as e:
        print(e)
        return None
    
def save_image(image,save_path):
    image.save(save_path)
