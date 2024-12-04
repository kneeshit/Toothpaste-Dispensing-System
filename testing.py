import cv2

def find_camera_indexes(max_to_test=10):
    # This function will test the first 'max_to_test' indexes.
    # It tries to open each index and capture a frame.
    # If it is successful, it prints the index.
    for i in range(max_to_test):
        cap = cv2.VideoCapture(i)
        if cap is None or not cap.isOpened():
            print(f"No camera found at index {i}")
        else:
            ret, frame = cap.read()
            if ret:
                print(f"Camera found at index {i}")
            else:
                print(f"Camera at index {i} is not available to capture")
        cap.release()

# Test the first 10 indexes
find_camera_indexes(10)
