import tkinter as tk
from PIL import Image, ImageTk
import requests
import image_processing
import os

API_KEY = "kDG4C5n27HLzZvvvVTzrmwffBQ0yR4FMAvVgSqI-qfY"
root = tk.Tk()
root.title("Recipe Picker:")
root.eval("tk::PlaceWindow . center")
def delete_files_with_extension(extension):
    current_directory = os.getcwd()

    for filename in os.listdir(current_directory):
        if filename.endswith(extension):
            os.remove(os.path.join(current_directory, filename))
            print(f"Deleted: {filename}")


def delete_files():

    delete_files_with_extension(".jpg")

def setup_image(count):

    image_path = f"Image{count}.jpg"
    original_image = Image.open(image_path)
    resized_image = original_image.resize((120, 120), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(resized_image)
    return image

def setup_frame3():

    frame3 = tk.Frame(root, width=500, height=600, bg="#3d6466")
    frame3.grid(row=0, column=0)
    frame3.pack_propagate(False)

    tk.Label(frame3, text="Thanks for playing! Click PLAY AGAIN to play again", bg="#3d6466", fg="white", font=("TkMenuFont", 11)).pack(pady=50)

    coordinates = [(70, 100), (210, 100), (350, 100), (70, 300), (210, 300)]

    for i, (x, y) in enumerate(coordinates):

        image = setup_image(i + 5)
        label = tk.Label(frame3, image=image, bg="#3d6466")
        label.image = image
        label.place(x=x, y=y)

    
    button = tk.Button(frame3, text="PLAY AGAIN", font=("tKHeadingFont", 20), bg="#3d6466", fg="white", cursor="hand2", activebackground="#badee2",
              activeforeground="black", command=setup_frame1)

    button.place(x=150, y=500)

def setup_frame2():


    frame2 = tk.Frame(root, width=500, height=600, bg="#3d6466")
    frame2.grid(row=0, column=0)
    frame2.pack_propagate(False)

    tk.Label(frame2, text="Click the GO button below to see the cartoon effect!", bg="#3d6466", fg="white", font=("TkMenuFont", 11)).pack(pady=50)

    coordinates = [(70, 100), (210, 100), (350, 100), (70, 300), (210, 300)]

    for i, (x, y) in enumerate(coordinates):

        image = setup_image(i)
        label = tk.Label(frame2, image=image, bg="#3d6466")
        label.image = image
        label.place(x=x, y=y)

    
    button = tk.Button(frame2, text="GO", font=("tKHeadingFont", 20), bg="#3d6466", fg="white", cursor="hand2", activebackground="#badee2",
              activeforeground="black", command=setup_frame3)

    button.place(x=200, y=450)
def setup_frame1():


    frame1 = tk.Frame(root, width=500, height=600, bg="#3d6466")
    frame1.grid(row=0, column=0)
    frame1.pack_propagate(False)

    delete_files()

    image_path = "assets/food.webp"
    original_image = Image.open(image_path)
    resized_image = original_image.resize((200, 200), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(resized_image)

    label = tk.Label(frame1, image=image, bg="#3d6466")
    label.image = image
    label.pack(pady=10)

    tk.Label(frame1, text="Turn Your Food Pics Into AI Generated Images!", bg="#3d6466", fg="white", font=("TkMenuFont", 14)).pack(pady=50)

    user_input = tk.Text(frame1, height=1, width=20)
    user_input.pack(pady=50)

    def get_input():
        user_input2 = user_input.get("1.0", "end-1c")
        search_query = user_input2.replace(' ', '+')  

        url = f'https://api.unsplash.com/search/photos?query={search_query}&client_id={API_KEY}'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
        else:
            print(f'Error: {response.status_code}')

        urls = []
        for photo in data['results']:
            image_url = photo['urls']['regular']
            urls.append(image_url)

        count = 0
        print(len(urls))

        for url in urls:
            if count < 5:
                image_data = requests.get(url).content
                with open(f"Image{count}.jpg", 'wb') as file:
                    file.write(image_data)
                count += 1

        for i in range(5):
            image_processing.process_image(f"Image{count - 5}.jpg", count)
            count += 1
        
        setup_frame2()
    tk.Button(frame1, text="ENTER", font=("tKHeadingFont", 20), bg="#3d6466", fg="white", cursor="hand2", activebackground="#badee2",
              activeforeground="black", command=get_input).pack()

    return root

if __name__ == "__main__":
    root = setup_frame1()
    root.mainloop()
