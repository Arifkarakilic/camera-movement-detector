from datasets import load_dataset
import cv2
import os

def download_camerabench(output_dir="camerabench_frames", sample_video_index=0):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Video {sample_video_index} indiriliyor...")
    dataset = load_dataset("syCen/CameraBench", split="test")
    video_data = dataset[sample_video_index]

    # Hugging Face cache içindeki video yolu alınır
    video_path = video_data["Video"]
    print(f"Video yolu: {video_path}")

    # OpenCV ile karelere böl
    cap = cv2.VideoCapture(video_path)
    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(output_dir, f"frame_{i:03d}.jpg")
        cv2.imwrite(frame_path, frame)
        i += 1

    cap.release()
    print(f"{i} kare kaydedildi: {output_dir}")

if __name__ == "__main__":
    for i in range(3):  # İlk 3 videoyu indir ve ayrıştır
        folder_name = f"frames_video_{i}"
        download_camerabench(output_dir=folder_name, sample_video_index=i)
