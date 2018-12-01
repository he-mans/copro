from io import BytesIO
from PIL import Image as PilImage

def convert_image(images):
    image_bytes = BytesIO()
    images_byte_array_dict = {}   
    images_byte_array = []
    
    if type(images) != list:
        images.save(image_bytes,"JPEG")
        image_bytes = image_bytes.getvalue()
        return image_bytes
    else:
        for i,image in enumerate(images):
            images_byte_array_dict.update({f'array{i}':BytesIO()})
            image.save(images_byte_array_dict[f'array{i}'],"JPEG")
            images_byte_array.append(images_byte_array_dict[f'array{i}'].getvalue() )
        return images_byte_array