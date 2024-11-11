import os
import cv2
import logging
from pathlib import Path
import sys

def setup_logging():
    """Configure logging to both file and console"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('video_processing.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def extract_frame(video_path, output_path, timestamp):
    """Extract a frame from the video at given timestamp"""
    try:
        # Open the video file
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            logging.error(f"Error: Could not open video {video_path}")
            return False
        
        # Get the FPS of the video
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            logging.error(f"Error: Invalid FPS for video {video_path}")
            return False
            
        # Calculate frame number from timestamp
        frame_number = int(timestamp * fps)
        
        # Set the frame position
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        # Read the frame
        ret, frame = cap.read()
        
        if not ret:
            logging.error(f"Error: Could not read frame from {video_path} at {timestamp}s")
            cap.release()
            return False
            
        # Save the frame
        cv2.imwrite(str(output_path), frame)
        
        # Release the video capture object
        cap.release()
        
        return True
        
    except Exception as e:
        logging.error(f"Error extracting frame from {video_path} at {timestamp}s: {str(e)}")
        return False

def process_video(video_path, output_folder):
    """Process a single video file"""
    try:
        # Create output folder for this video
        video_name = Path(video_path).stem
        video_output_folder = Path(output_folder) / video_name
        video_output_folder.mkdir(parents=True, exist_ok=True)

        # Extract frames
        frames = {
            'image_pair_half_second.jpg': 0.5,  # First frame
            'image_pair_five_second.jpg': 5  # Frame at 5 seconds
        }

        success = True
        for frame_name, timestamp in frames.items():
            frame_path = video_output_folder / frame_name
            if not extract_frame(str(video_path), str(frame_path), timestamp):
                success = False

        if success:
            logging.info(f"Successfully processed {video_path}")
        return success

    except Exception as e:
        logging.error(f"Error processing {video_path}: {str(e)}")
        return False

def main():
    # Setup paths
    input_folder = Path('data/raw_data/ride_17822_20240203052746/recordings')
    output_folder = Path('data/preprocessed_data/ride_17822_20240203052746/image_pairs')

    # Setup logging
    setup_logging()

    # Create output folder
    output_folder.mkdir(parents=True, exist_ok=True)

    # Process videos
    total_videos = 0
    successful_videos = 0

    for video_file in input_folder.glob('*.ts'):
        total_videos += 1
        if process_video(video_file, output_folder):
            successful_videos += 1

    # Log summary
    logging.info(f"Processing complete: {successful_videos}/{total_videos} videos processed successfully")

if __name__ == "__main__":
    main()