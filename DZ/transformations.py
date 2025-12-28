import pixel_transformer
import pixelsort
import corruption2

# Global variables to store current image data
original_pixel_data = None
current_pixel_data = None
current_width = 0
current_height = 0
current_texture_id = "initial_texture"

def set_global_data(pixel_data, width, height, texture_id):
    global current_pixel_data, current_width, current_height, current_texture_id, original_pixel_data
    current_pixel_data = pixel_data
    current_width = width
    current_height = height
    current_texture_id = texture_id
    original_pixel_data = pixel_data

def get_global_pixel_data():
    return current_pixel_data

def apply_pixel_sort(threshold=0.5):
    global current_pixel_data
    if current_pixel_data and current_width > 0:
        try:
            import dearpygui.dearpygui as dpg
            
            sorted_data = pixelsort.sort_intervals_by_lightness(
                current_pixel_data, 
                current_width, 
                current_height,
                threshold=threshold
            )
            
            dpg.set_value(current_texture_id, sorted_data)
            current_pixel_data = sorted_data
            dpg.set_value("status", f"Pixelsorted (edge thresh: {threshold:.2f})")
            
        except Exception as e:
            print(f"Pixelsort error: {e}")

def apply_corruption2(tameness=0):
    global current_pixel_data
    if current_pixel_data and current_width > 0:
        try:
            import dearpygui.dearpygui as dpg
            import numpy as np
            import io
            from PIL import Image
            data_array = np.array(current_pixel_data, dtype=np.float32)
            data_array = data_array.reshape(current_height, current_width, 4)
            img_array = (data_array * 255).astype(np.uint8)

            img = Image.fromarray(img_array, 'RGBA')
            
            img_bytes = io.BytesIO()
            img.convert('RGB').save(img_bytes, format='JPEG', quality=100)
            image_bytes = img_bytes.getvalue()

            corrupted_bytes = corruption2.corrupt_image(image_bytes, tameness=tameness)

            corrupted_img = Image.open(io.BytesIO(corrupted_bytes))
            corrupted_img = corrupted_img.convert('RGBA')
            corrupted_array = np.array(corrupted_img).astype(np.float32) / 255.0

            dpg.set_value(current_texture_id, corrupted_array.flatten().tolist())
            current_pixel_data = corrupted_array.flatten().tolist()
            dpg.set_value("status", f"Destroyed image (tameness: {tameness})")
        
        except Exception as e:
            print(f"Corruption2 error: {e}")

def reset_to_original():
    global current_pixel_data, original_pixel_data, current_width
    if current_pixel_data and original_pixel_data and current_width > 0:
        try:
            import dearpygui.dearpygui as dpg
            dpg.set_value(current_texture_id, original_pixel_data)
            current_pixel_data = original_pixel_data
            dpg.set_value("status", "Reset to original")
            print("Reset to original image")
            
        except Exception as e:
            print(f"Reset error: {e}")
            import dearpygui.dearpygui as dpg
            dpg.set_value("status", f"Reset error: {str(e)}")
