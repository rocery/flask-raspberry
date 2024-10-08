from PIL import Image, ExifTags
import os

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

def format_name(name):
    return ' '.join([word.capitalize() for word in name.split()])

def save_image(images, folder_path, quality=30, compress_level=3):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    for image in images:
        img = Image.open(image)
        # Handle image rotation based on EXIF orientation
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = img._getexif()
            if exif is not None:
                orientation = exif.get(orientation, 1)
                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(270, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # Cases: image don't have getexif
            pass
        
        # Save original image with reduced quality
        original_path = os.path.join(folder_path, f"original_{image.filename}")
        if image.filename.lower().endswith(('.jpg', '.jpeg')):
            img.save(original_path, quality=quality, optimize=True)
        elif image.filename.lower().endswith('.png'):
            img.save(original_path, compress_level=compress_level, optimize=True)
        
        # Create and save mirrored image with reduced quality
        mirrored_img = img.transpose(Image.FLIP_LEFT_RIGHT)
        mirrored_path = os.path.join(folder_path, f"mirrored_{image.filename}")
        if image.filename.lower().endswith(('.jpg', '.jpeg')):
            mirrored_img.save(mirrored_path, quality=quality, optimize=True)
        elif image.filename.lower().endswith('.png'):
            mirrored_img.save(mirrored_path, compress_level=compress_level, optimize=True)

def get_folders_info(upload_folder):
    folders_info = []
    for folder_name in os.listdir(upload_folder):
        folder_path = os.path.join(upload_folder, folder_name)
        if os.path.isdir(folder_path):
            image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            folders_info.append((folder_name, len(image_files)))
    return folders_info
