import os
import tempfile
import base64
import logging
from typing import Dict, Any, Optional
import requests
from src.services.ai_provider_service import AIProviderService
from src.models import db, VideoAnalysis

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoAnalyzer:
    """Service for analyzing video content including transcription and visual analysis."""
    
    def __init__(self):
        self.ai_service = AIProviderService()
    
    def analyze_video(self, user_id: int, video_data: bytes, video_url: str = None, post_id: int = None) -> Dict[str, Any]:
        """Analyze a video including transcription and visual description."""
        try:
            # Save video data to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_video:
                temp_video.write(video_data)
                temp_video_path = temp_video.name
            
            try:
                # Extract audio for transcription
                audio_path = self._extract_audio(temp_video_path)
                if audio_path:
                    transcription_result = self._transcribe_audio(user_id, audio_path)
                    os.unlink(audio_path)  # Clean up audio file
                else:
                    transcription_result = {
                        "transcription": "Audio extraction failed or no audio found.",
                        "success": False
                    }
                
                # Extract frame for visual analysis
                frame_path = self._extract_frame(temp_video_path)
                if frame_path:
                    visual_result = self._analyze_frame(user_id, frame_path)
                    os.unlink(frame_path)  # Clean up frame file
                else:
                    visual_result = {
                        "description": "Frame extraction failed.",
                        "success": False
                    }
                
                # Get AI config used
                config = self.ai_service._get_config_for_user(user_id)
                
                # Save analysis results
                analysis = VideoAnalysis(
                    post_id=post_id or 0,
                    video_url=video_url or "",
                    transcription_text=transcription_result.get("transcription", ""),
                    visual_description=visual_result.get("description", ""),
                    user_id=user_id,
                    provider_config_id=config.id if config else None
                )
                
                db.session.add(analysis)
                db.session.commit()
                
                return {
                    "success": True,
                    "analysis_id": analysis.id,
                    "transcription": transcription_result.get("transcription", ""),
                    "visual_description": visual_result.get("description", ""),
                    "transcription_success": transcription_result.get("success", False),
                    "visual_success": visual_result.get("success", False)
                }
                
            finally:
                # Clean up temporary video file
                os.unlink(temp_video_path)
                
        except Exception as e:
            logger.error(f"Video analysis failed: {str(e)}")
            return {"error": f"Video analysis failed: {str(e)}"}
    
    def analyze_video_url(self, user_id: int, video_url: str, post_id: int = None) -> Dict[str, Any]:
        """Analyze a video from URL including transcription and visual description."""
        try:
            # Download video content
            logger.info(f"Downloading video from {video_url}")
            response = requests.get(video_url, timeout=30)
            if response.status_code != 200:
                return {"error": f"Failed to download video: {response.status_code}"}
            
            video_data = response.content
            return self.analyze_video(user_id, video_data, video_url, post_id)
            
        except Exception as e:
            logger.error(f"Video URL analysis failed: {str(e)}")
            return {"error": f"Video URL analysis failed: {str(e)}"}
    
    def _extract_audio(self, video_path: str) -> Optional[str]:
        """Extract audio from video file."""
        try:
            import ffmpeg
            # Extract audio using ffmpeg
            audio_path = video_path + ".wav"
            (
                ffmpeg
                .input(video_path)
                .output(audio_path, acodec='pcm_s16le', ac=1, ar='16000')
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            return audio_path
        except Exception as e:
            logger.warning(f"Audio extraction failed: {str(e)}")
            return None
    
    def _transcribe_audio(self, user_id: int, audio_path: str) -> Dict[str, Any]:
        """Transcribe audio using Whisper."""
        try:
            import whisper
            # Load the Whisper model
            model = whisper.load_model("base")
            
            # Transcribe the audio
            result = model.transcribe(audio_path)
            
            return {
                "success": True,
                "transcription": result["text"],
                "language": result["language"]
            }
        except Exception as e:
            logger.error(f"Audio transcription failed: {str(e)}")
            # Fallback to AI service
            try:
                with open(audio_path, 'rb') as audio_file:
                    audio_data = audio_file.read()
                return self.ai_service.call_speech_to_text(user_id, audio_data)
            except Exception as fallback_e:
                logger.error(f"Fallback transcription failed: {str(fallback_e)}")
                return {
                    "transcription": f"Transcription failed: {str(e)}",
                    "success": False
                }
    
    def _extract_frame(self, video_path: str) -> Optional[str]:
        """Extract a frame from video file."""
        try:
            import cv2
            # Open video file
            cap = cv2.VideoCapture(video_path)
            
            # Get frame at 1 second
            cap.set(cv2.CAP_PROP_POS_MSEC, 1000)
            ret, frame = cap.read()
            
            if ret:
                # Save frame to temporary file
                frame_path = video_path + ".jpg"
                cv2.imwrite(frame_path, frame)
                cap.release()
                return frame_path
            else:
                cap.release()
                return None
                
        except Exception as e:
            logger.warning(f"Frame extraction failed: {str(e)}")
            return None
    
    def _analyze_frame(self, user_id: int, frame_path: str) -> Dict[str, Any]:
        """Analyze frame using AI vision service."""
        try:
            # Read frame as bytes
            with open(frame_path, 'rb') as frame_file:
                frame_data = frame_file.read()
            
            # Use AI service for vision analysis
            result = self.ai_service.call_vision_to_text(
                user_id,
                {
                    "image": frame_data, 
                    "prompt": "Describe this video frame in detail, including objects, people, actions, setting, mood, and visual style."
                }
            )
            
            return result
        except Exception as e:
            logger.error(f"Frame analysis failed: {str(e)}")
            return {
                "description": f"Frame analysis failed: {str(e)}",
                "success": False
            }