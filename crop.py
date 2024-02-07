from PIL import Image
import os

destination_path = "C:\\Users\\Administrator\\Desktop\\1.mjpeg"
def crop_to_phone_resolution(image):
    target_ratio = 9 / 16
    width, height = image.size
    current_ratio = width / height

    if current_ratio > target_ratio:
        # Если изображение шире, обрезаем по горизонтали
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        right = left + new_width
        top, bottom = 0, height
    else:
        # Если изображение выше, обрезаем по вертикали
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        bottom = top + new_height
        left, right = 0, width

    return image.crop((left, top, right, bottom))

def changephoto_to_camera(image_path):
    # Открываем изображение
    # image_path = "C:\\Users\\Administrator\\Desktop\\photo\\1.jpg"
    img = Image.open(image_path)

    # Обрезаем изображение
    cropped_img = crop_to_phone_resolution(img)

    # Сохраняем обрезанное изображение с новым именем
    cropped_img.save("C:\\Users\\Administrator\\Desktop\\1_cropped.jpg")

    if os.path.exists(destination_path):
        os.remove(destination_path)
    # Опционально, оставляем исходный файл без изменений
    os.rename("C:\\Users\\Administrator\\Desktop\\1_cropped.jpg", destination_path)
# changephoto_to_camera("C:\\Users\\Administrator\\Desktop\\photo\\2024-02-05 21.23.21.jpg")