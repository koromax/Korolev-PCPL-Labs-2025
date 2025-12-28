import numpy as np

def sort_intervals_by_lightness(pixel_data, width, height, threshold=0.9):
    img_array = np.array(pixel_data, dtype=np.float32).reshape(height, width, 4)
    
    rgb = img_array[:, :, :3]
    gray = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]
    
    for y in range(height):
        row = img_array[y, :, :]
        row_gray = gray[y, :]
        
        diffs = np.abs(np.diff(row_gray, append=row_gray[-1]))
        
        if diffs.max() > 0:
            diffs = diffs / diffs.max()
        
        is_edge = diffs > threshold
        
        intervals = []
        start_idx = 0
        
        for x in range(width):
            if is_edge[x] or x == width - 1:
                end_idx = x
                if end_idx > start_idx:
                    intervals.append((start_idx, end_idx))
                start_idx = x
        
        for start, end in intervals:
            interval_pixels = row[start:end, :]
            interval_gray = row_gray[start:end]
            
            sorted_indices = np.argsort(interval_gray)
            row[start:end, :] = interval_pixels[sorted_indices]
    
    return img_array.flatten().tolist()
