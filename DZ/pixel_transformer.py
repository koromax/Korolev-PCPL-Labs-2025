import pixel_transformer
import numpy as np

def hue_shift(pixel_data, width, height, shift_amount=0.5):
    """
    Apply hue shift to pixel data.
    
    Args:
        pixel_data: List of floats (0-1) in RGBA format, length = width * height * 4
        width: Image width
        height: Image height
        shift_amount: Hue shift amount (0.0 to 1.0)
    
    Returns:
        List of transformed pixel data
    """
    # Convert to numpy array for easier manipulation
    data_array = np.array(pixel_data, dtype=np.float32).reshape(height, width, 4)
    
    # Only process RGB channels, leave alpha alone
    rgb = data_array[:, :, :3]
    alpha = data_array[:, :, 3:]
    
    # Simple hue shift: rotate RGB channels
    # This is a basic hue rotation - in real HSV it would be different
    if shift_amount < 0.33:
        # Shift red -> green -> blue -> red
        shifted = np.roll(rgb, shift=1, axis=2)
    elif shift_amount < 0.66:
        # Shift blue -> green -> red -> blue  
        shifted = np.roll(rgb, shift=2, axis=2)
    else:
        # Strong shift
        shifted = rgb[:, :, ::-1]  # Reverse RGB order
    
    # Blend with original based on shift_amount
    blend_factor = abs(shift_amount * 2 - 1)  # 0 at 0.5, 1 at 0 or 1
    shifted = rgb * (1 - blend_factor) + shifted * blend_factor
    
    # Recombine with alpha
    result = np.concatenate([shifted, alpha], axis=2)
    
    return result.flatten().tolist()

def simple_hue_shift(pixel_data, width, height):
    """
    Simple hue shift - swaps color channels in a predictable way.
    Easy to see the effect.
    """
    data_array = np.array(pixel_data, dtype=np.float32).reshape(height, width, 4)
    
    # Swap red and blue channels (simple hue shift)
    rgb = data_array[:, :, :3]
    alpha = data_array[:, :, 3:]
    
    # Create shifted version: BGR instead of RGB
    shifted = rgb[:, :, [2, 1, 0]]  # Swap red and blue
    
    # Combine back
    result = np.concatenate([shifted, alpha], axis=2)
    
    return result.flatten().tolist()

def invert_colors(pixel_data, width, height):
    """Invert RGB colors (negative image effect)"""
    data_array = np.array(pixel_data, dtype=np.float32).reshape(height, width, 4)
    
    # Invert RGB channels only
    data_array[:, :, :3] = 1.0 - data_array[:, :, :3]
    
    return data_array.flatten().tolist()

def grayscale(pixel_data, width, height):
    """Convert to grayscale"""
    data_array = np.array(pixel_data, dtype=np.float32).reshape(height, width, 4)
    
    # Calculate luminance
    rgb = data_array[:, :, :3]
    luminance = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]
    
    # Apply to all RGB channels
    data_array[:, :, 0] = luminance  # Red
    data_array[:, :, 1] = luminance  # Green
    data_array[:, :, 2] = luminance  # Blue
    
    return data_array.flatten().tolist()