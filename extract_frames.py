import cv2
import os

video_path = "Hamburgers_being_assembled_with_._202605152043.mp4"
output_dir = "frames"
target_frames_count = 150 # user asked for 150 to 200 frames
max_width = 1920

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

cap = cv2.VideoCapture(video_path)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"Total frames in video: {total_frames}")

step = max(1, total_frames // target_frames_count)
print(f"Extracting every {step} frame(s)")

frame_idx = 0
saved_idx = 1

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    if frame_idx % step == 0 and saved_idx <= target_frames_count:
        # Resize if width > 1920
        h, w = frame.shape[:2]
        if w > max_width:
            new_w = max_width
            new_h = int((new_w / w) * h)
            frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        output_path = os.path.join(output_dir, f"frame_{saved_idx:03d}.webp")
        cv2.imwrite(output_path, frame, [cv2.IMWRITE_WEBP_QUALITY, 80])
        saved_idx += 1
        
    frame_idx += 1

cap.release()
print(f"Saved {saved_idx - 1} frames to {output_dir}")
