import youtube_transcript_api
print("LIBRARY LOADED FROM:", youtube_transcript_api.__file__)

from youtube_transcript_api import YouTubeTranscriptApi
import re
import time
import random
import concurrent.futures
import os

def extract_video_id(url):
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r'v=([a-zA-Z0-9_-]{11})',
        r'youtu\.be/([a-zA-Z0-9_-]{11})',
        r'shorts/([a-zA-Z0-9_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

class YouTubeTranscriptProcessor:
    def __init__(self, input_filename, output_filename):
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.processed_video_ids = set()
        self.videos_processed = 0
        self.max_retries = 3
        # Create ThreadPoolExecutor once and reuse it to prevent overhead
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def fetch_transcript(self, video_id):
        """Fetch transcript with retries, timeout, and proper error logging."""
        for attempt in range(self.max_retries + 1):
            try:
                def _fetch_task():
                    api = YouTubeTranscriptApi()
                    transcript_data = api.fetch(video_id, languages=['en'])
                    return transcript_data

                future = self.executor.submit(_fetch_task)
                transcript_data = future.result(timeout=30)
                
                texts = [snippet.text for snippet in transcript_data.snippets]
                return " ".join(texts).replace('\n', ' ')
                
            except Exception as e:
                error_msg = str(e)
                # Check for rate limit specifically
                if "429" in error_msg or "Too Many Requests" in error_msg:
                    print(f"\n[CRITICAL RATE LIMIT] YouTube blocked the request for {video_id} (HTTP 429).")
                    if attempt < self.max_retries:
                        # Exponential backoff for rate limits (1-5+ minutes)
                        wait_time = (attempt + 1) * 120 + random.uniform(15, 45)
                        print(f"-> Cooling down for {wait_time:.0f} seconds before retrying...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print("\n[ERROR] Persistent rate limit. You may need to stop the script and wait a few hours, use a VPN, or use a cookies file.\n")
                        return None
                        
                print(f"[Warning] Error fetching {video_id}: {error_msg}")
                if attempt < self.max_retries:
                    retry_delay = random.uniform(10, 20)
                    print(f"-> Retrying in {retry_delay:.2f}s (Attempt {attempt + 1}/{self.max_retries})...")
                    time.sleep(retry_delay)
                else:
                    print(f"[Error] Skipping {video_id} after {self.max_retries} retries.")
                    return None

    def load_progress(self):
        """Scan existing output to automatically resume progress."""
        if os.path.exists(self.output_filename):
            try:
                with open(self.output_filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Safer regex to avoid greedy match bugs
                    found_urls = re.findall(r'Video URL:\s*(https?://\S+)', content)
                    for url in found_urls:
                        vid = extract_video_id(url)
                        if vid:
                            self.processed_video_ids.add(vid)
                            
                if self.processed_video_ids:
                    print(f"\nResuming progress: Found {len(self.processed_video_ids)} already processed videos in output file.\n")
            except Exception as e:
                print(f"Notice: Could not read previous output file for resume: {e}")

    def process_videos(self):
        """Main batch processing loop."""
        print(f"Reading links from {self.input_filename}...")
        try:
            with open(self.input_filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"Error: Could not find {self.input_filename}.")
            return

        self.load_progress()
        file_exists = os.path.exists(self.output_filename)

        with open(self.output_filename, 'a', encoding='utf-8') as out_file:
            if not file_exists:
                out_file.write("UX MASTER GUIDE: COMBINED VIDEO TRANSCRIPTS\n")
                out_file.write("=" * 60 + "\n\n")

            for line in lines:
                line = line.strip()
                if not line or line.startswith('-') or line.startswith('Extracted'):
                    continue

                if ' | ' in line:
                    parts = line.split(' | ', 1)
                    title = parts[0]
                    url = parts[1]
                else:
                    title = "Unknown Video Topic"
                    url = line

                video_id = extract_video_id(url)
                
                # Check memory before fetching
                if not video_id or video_id in self.processed_video_ids:
                    continue
                
                display_title = title if title != "Browse All Topics & Authors" else "Additional UX Video"
                print(f"Fetching transcript for: {display_title}...")
                
                transcript = self.fetch_transcript(video_id)
                
                # Update progress only if transcript was successfully retrieved
                if transcript:
                    self.processed_video_ids.add(video_id)
                    
                    out_file.write(f"### {display_title}\n")
                    out_file.write(f"Video URL: {url}\n\n")
                    out_file.write(transcript + "\n\n")
                    out_file.write("-" * 60 + "\n\n")
                    
                    self.videos_processed += 1
                    print(f"Completed {self.videos_processed} videos in this run.")
                    
                    # Flush changes immediately
                    out_file.flush()
                    os.fsync(out_file.fileno())
                    
                    # Rate limiting delays (only applied on success)
                    delay = random.uniform(10, 20)
                    print(f"Waiting {delay:.2f} seconds before next request...")
                    time.sleep(delay)
                    
                    if self.videos_processed % 10 == 0:
                        batch_pause = random.uniform(120, 180)
                        print(f"\n--- Processed {self.videos_processed} videos. Batch pause for {batch_pause:.2f}s... ---\n")
                        time.sleep(batch_pause)

        # Cleanly shutdown executor
        self.executor.shutdown(wait=False)
        print(f"\nSuccess! Filtered and combined transcripts saved to: {self.output_filename}")

if __name__ == "__main__":
    input_txt = "1.psychology-study-guide-YouTube_Video_Links.txt"
    output_txt = "1.psychology-study-guide-YouTube_Video_Transcripts.txt"
    
    processor = YouTubeTranscriptProcessor(input_txt, output_txt)
    processor.process_videos()