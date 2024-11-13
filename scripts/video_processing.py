import cv2

def extract_frames(video_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)
    success, frame = video.read()
    count = 0
    
    while success:
        # Save the frame as an image (optional)
        cv2.imwrite(f'frame_{count}.jpg', frame)

        # Display the frame (optional)
        cv2.imshow(f'Frame {count}', frame)

        # Move to the next frame
        success, frame = video.read()
        count += 1

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = "path_to_video.mp4"  # Add path to your sample video
    extract_frames(video_path)
