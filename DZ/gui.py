import dearpygui.dearpygui as dpg
from PIL import Image
import numpy as np
import transformations

zoom_scale = 1.0
pan_x = 0
pan_y = 0
is_dragging = False
last_mouse_pos = (0, 0)

""" --- PIXEL SORT ----"""

def apply_pixel_sort():
    threshold = dpg.get_value("sort_threshold")
    transformations.apply_pixel_sort(threshold)

def destroy_image():
    tameness = (dpg.get_value("sort_threshold")) * 10000 // 100
    transformations.apply_corruption2(tameness)
    

""" --- IMAGE CALLBACK --- """

def load_image_callback(sender, app_data):
    global current_pixel_data, current_width, current_height, current_texture_id

    if 'file_path_name' in app_data:
        file_path = app_data['file_path_name']
        
        try:
            # Open and convert image
            img = Image.open(file_path)
            img = img.convert('RGBA')
            current_width, current_height = img.size
            
            print(f"Loading image: {current_width}x{current_height}")
            
            # Convert to DearPyGui format and store globally
            img_array = np.array(img).astype(np.float32) / 255.0
            current_pixel_data = img_array.flatten().tolist()
            
            print(f"Data length: {len(current_pixel_data)}, expected: {current_width * current_height * 4}")
            
            # Create a NEW texture for this image
            texture_reg_id = f"tex_reg_{current_width}_{current_height}_{hash(file_path)}"
            current_texture_id = f"texture_{current_width}_{current_height}_{hash(file_path)}"
            
            transformations.set_global_data(current_pixel_data, current_width, current_height, current_texture_id)
            # Create new texture registry
            dpg.add_texture_registry(show=False, tag=texture_reg_id)
            
            # Create texture with original image data
            dpg.add_dynamic_texture(
                parent=texture_reg_id,
                width=current_width,
                height=current_height,
                default_value=current_pixel_data,
                tag=current_texture_id
            )
            
            # Point image widget to the new texture
            dpg.configure_item("image_widget", texture_tag=current_texture_id)
            
            # Update image display size to fit canvas
            update_display_size()
            
            # Enable transformation buttons
            dpg.configure_item("reset_btn", enabled=True)
            dpg.configure_item("sort_threshold", enabled=True)
            dpg.configure_item("apply_sort_btn", enabled=True)
            dpg.configure_item("destroy_img_btn", enabled=True)
            # Update status
            dpg.set_value("status", f"Loaded: {file_path}")
            
            fit_to_canvas()
            print("Image loaded successfully")
            dpg.configure_item("save_btn", enabled=True)
            
        except Exception as e:
            print(f"Error: {e}")
            dpg.set_value("status", f"Error: {str(e)}")

def update_display_size():
    if current_width > 0 and current_height > 0:
        canvas_width = dpg.get_item_width("canvas")
        canvas_height = dpg.get_item_height("canvas")
        
        display_width = int(current_width * zoom_scale)
        display_height = int(current_height * zoom_scale)
        
        x_pos = pan_x + (canvas_width - display_width) // 2
        y_pos = pan_y + (canvas_height - display_height) // 2
        
        dpg.configure_item("image_widget", width=display_width, height=display_height)
        dpg.configure_item("image_widget", pos=[x_pos, y_pos])

def save_image():
    pixel_data = transformations.get_global_pixel_data()
    if pixel_data:
        try:
            data_array = np.array(pixel_data, dtype=np.float32)
            data_array = data_array.reshape(current_height, current_width, 4)
            
            img_array = (data_array * 255).astype(np.uint8)
            
            img = Image.fromarray(img_array, 'RGBA')
            
            def save_callback(sender, app_data):
                if 'file_path_name' in app_data:
                    save_path = app_data['file_path_name']
                    img.save(save_path)
                    dpg.set_value("status", f"Saved: {save_path}")
                    print(f"Image saved to: {save_path}")
            
            with dpg.file_dialog(
                directory_selector=False,
                show=True,
                callback=save_callback,
                tag="save_dialog",
                width=600,
                height=400
            ):
                dpg.add_file_extension("PNG Image{.png}")
                dpg.add_file_extension("All files{.*}")
            
        except Exception as e:
            print(f"Save error: {e}")
            dpg.set_value("status", f"Save error: {str(e)}")
    else:
        dpg.set_value("status", "No image to save")

""" --- ZOOM AND DRAG --- """
def fit_to_canvas():
    global zoom_scale, pan_x, pan_y
    
    if current_width > 0 and current_height > 0:
        canvas_width = dpg.get_item_width("canvas")
        canvas_height = dpg.get_item_height("canvas")
        
        scale_x = canvas_width / current_width
        scale_y = canvas_height / current_height
        zoom_scale = min(scale_x, scale_y)
        
        pan_x = 0
        pan_y = 0
        
        update_display_size()
        dpg.set_value("status", "Fitted to canvas")

def on_mouse_wheel(sender, app_data):
    global zoom_scale, pan_x, pan_y, display_width, display_height
    
    if dpg.is_item_hovered("canvas") and current_width > 0:
        old_zoom = zoom_scale
        
        if app_data > 0:
            zoom_scale *= 1.1
        else:
            zoom_scale *= 0.9
        
        # zoom_scale = max(0.1, min(10.0, zoom_scale))
        # canvas_width = dpg.get_item_width("canvas")
        # canvas_height = dpg.get_item_height("canvas")
        # display_width = int(current_width * zoom_scale)
        # display_height = int(current_height * zoom_scale)
        # center_x = pan_x + (canvas_width - display_width) // 2          # (a - b) / 2 + b / 2 
        # center_y = pan_y + (canvas_height - display_height) // 2
        # mouse_x, mouse_y = dpg.get_mouse_pos()
        # dx, dy = mouse_x - center_x, mouse_y - center_y
        # pan_x += dx * (zoom_scale / old_zoom - 1)
        # pan_y += dy * (zoom_scale / old_zoom - 1)

        # print(f"CD: ({canvas_width}, {canvas_height}), DD: ({display_width}, {display_height}), IC: ({center_x}, {center_y}), MP: ({mouse_x}, {mouse_y}), d: ({dx}, {dy}), pan: ({pan_x}, {pan_y})")
        update_display_size()
        dpg.set_value("status", f"Zoom: {zoom_scale:.2f}x")

def on_mouse_down(sender, app_data):
    global is_dragging, last_mouse_pos
    
    if dpg.is_item_hovered("canvas") and app_data == 0:
        is_dragging = True
        last_mouse_pos = dpg.get_mouse_pos()

def on_mouse_drag(sender, app_data):
    global pan_x, pan_y, last_mouse_pos, is_dragging
    
    if is_dragging and dpg.is_item_hovered("canvas"):
        current_mouse_pos = dpg.get_mouse_pos()
        
        if last_mouse_pos:
            delta_x = current_mouse_pos[0] - last_mouse_pos[0]
            delta_y = current_mouse_pos[1] - last_mouse_pos[1]
            
            pan_x += delta_x
            pan_y += delta_y
            
            last_mouse_pos = current_mouse_pos
            update_display_size()

def on_mouse_up(sender, app_data):
    global is_dragging, last_mouse_pos
    is_dragging = False
    last_mouse_pos = None


# Initialize DearPyGui
dpg.create_context()
dpg.create_viewport(title='Image Viewer', width=1200, height=800)

# Create a theme for transparent control panel
with dpg.theme() as transparent_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0, 200))
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0, 200))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (50, 50, 50, 200))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (70, 70, 70, 200))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (90, 90, 90, 200))
        dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))

# Create a theme for black canvas
with dpg.theme() as canvas_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0, 255))
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0, 0))

""" --- canvas window --- """
with dpg.window(
    label="",
    tag="canvas",
    no_title_bar=True,
    no_move=True,
    no_resize=True,
    no_scrollbar=True,
    no_scroll_with_mouse=True,
    no_collapse=True,
    no_background=True,
    no_close=True,
    no_bring_to_front_on_focus=True,
    menubar=False,
    width=1200,
    height=800,
    pos=[0, 0]
):
    dpg.bind_item_theme("canvas", canvas_theme)
    
    with dpg.handler_registry():
        dpg.add_mouse_wheel_handler(callback=on_mouse_wheel)
        dpg.add_mouse_click_handler(button=0, callback=on_mouse_down)
        dpg.add_mouse_drag_handler(button=0, callback=on_mouse_drag)
        dpg.add_mouse_release_handler(button=0, callback=on_mouse_up)

    # Create initial texture registry for canvas
    with dpg.texture_registry(show=False):
        dpg.add_dynamic_texture(
            width=1,
            height=1,
            default_value=[0.0, 0.0, 0.0, 0.0],  # Transparent
            tag="initial_texture"
        )
    
    # Image widget inside canvas - will be positioned and sized dynamically
    dpg.add_image("initial_texture", tag="image_widget", width=100, height=100, pos=[0, 0])

""" --- control panel --- """
with dpg.window(
    label="Controls",
    tag="control_panel",
    width=300,
    height=400,
    pos=[20, 20],
    no_resize=False,
    no_collapse=False,
    no_close=True,
    no_title_bar=False,
    no_scrollbar=True,
    no_move=False,
    no_background=False
):
    dpg.bind_item_theme("control_panel", transparent_theme)
    
    dpg.add_button(label="Open Image", callback=lambda: dpg.show_item("file_dialog"), width=280, height=40)
    dpg.add_button(label="Save Image", tag="save_btn", callback=save_image, width=280, height=40, enabled=False)
    dpg.add_spacer(height=10)
    
    dpg.add_button(label="Reset", tag="reset_btn", callback=transformations.reset_to_original, width=280, height=40, enabled=True)
    dpg.add_button(label="Fit to Canvas", callback=fit_to_canvas, width=280, height=40)
    dpg.add_text("Mouse: Wheel=Zoom, Left Drag=Pan", color=(150, 150, 150))

    dpg.add_spacer(height=20)
    dpg.add_text("No image loaded", tag="status")

    dpg.add_spacer(height=10)
    dpg.add_text("Pixel Sort:", color=(200, 200, 255))

    dpg.add_slider_float(
        label="Lightness Threshold",
        tag="sort_threshold",
        default_value=0.5,
        min_value=0.0,
        max_value=1.0,
        width=280,
        enabled=False,
        no_input=True
    )

    dpg.add_button(
        label="Apply Pixel Sort",
        tag="apply_sort_btn",
        callback=apply_pixel_sort,
        width=280,
        enabled=False
    )

    dpg.add_button(
        label="Destroy Image",
        tag="destroy_img_btn",
        callback=destroy_image,
        width=280,
        enabled=False
    )

with dpg.file_dialog(
    directory_selector=False,
    show=False,
    height=400,
    tag="file_dialog"
):
    dpg.add_file_extension("Images{.jpg,.jpeg,.png}")
    dpg.add_file_extension("All files{.*}")

# Resize handler to make canvas fill viewport
def on_viewport_resize(sender, app_data):
    """When viewport resizes, resize canvas to fill it"""
    width = dpg.get_viewport_width()
    height = dpg.get_viewport_height()
    
    # Resize canvas to fill viewport
    dpg.configure_item("canvas", width=width, height=height)
    
    # Update image display size if an image is loaded
    update_display_size()

# Set the callbacks
dpg.set_item_callback("file_dialog", load_image_callback)
dpg.set_viewport_resize_callback(on_viewport_resize)


dpg.setup_dearpygui()
dpg.show_viewport()
# dpg.maximize_viewport()  # Start maximized
dpg.start_dearpygui()
dpg.destroy_context()