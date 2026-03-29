from deepface import DeepFace
import os
import cv2
import numpy as np
import logging
import time

logger = logging.getLogger(__name__)

class FaceAnalyzer:
    def __init__(self, detector_backend='retinaface'):
        """
        Face recognition and analysis engine using DeepFace.
        'opencv' is used for lightweight deployment (avoids OOM on HF Spaces).
        """
        self.detector_backend = detector_backend
        logger.info(f"Initialized FaceAnalyzer with {detector_backend} backend.")

    @staticmethod
    def _sanitize_results(obj):
        """
        Recursively converts NumPy types to standard Python types for JSON serialization.
        Handles float32, int64, ndarray, etc.
        """
        if isinstance(obj, dict):
            return {k: FaceAnalyzer._sanitize_results(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [FaceAnalyzer._sanitize_results(i) for i in obj]
        
        # Check for NumPy types (even if not imported as np)
        type_name = type(obj).__name__
        if 'float' in type_name:
            return float(obj)
        elif 'int' in type_name:
            return int(obj)
        elif 'ndarray' in type_name:
            return FaceAnalyzer._sanitize_results(obj.tolist())
        elif hasattr(obj, 'item') and callable(getattr(obj, 'item')):
            return obj.item()
            
        return obj

    def analyze(self, img_path):
        """
        Analyzes an image for age, gender, emotion, and race.
        Returns the findings as a dict.
        """
        try:
            start_time = time.time()
            # Try to run all actions first.
            results = DeepFace.analyze(
                img_path=img_path,
                actions=['age', 'gender', 'emotion', 'race'],
                detector_backend=self.detector_backend,
                enforce_detection=False,
                silent=True
            )
            process_time = time.time() - start_time
            logger.info(f"Analysis completed in {process_time:.2f}s")
            
            if isinstance(results, list):
                final_results = {"faces": results, "count": len(results), "process_time": process_time}
            else:
                final_results = {"faces": [results], "count": 1, "process_time": process_time}
            
            return FaceAnalyzer._sanitize_results(final_results)
            
        except Exception as e:
            logger.warning(f"Full analysis failed ({str(e)}), trying detection only...")
            try:
                # Fallback to basic detection if models are missing
                detection_results = DeepFace.extract_faces(
                    img_path=img_path,
                    detector_backend=self.detector_backend,
                    enforce_detection=False
                )
                faces = []
                for face in detection_results:
                    faces.append({
                        "face_confidence": face.get('confidence', 0),
                        "dominant_gender": "Unknown",
                        "gender": {"Unknown": 100.0},
                        "age": 0,
                        "dominant_emotion": "unknown",
                        "emotion": {"unknown": 100.0},
                        "dominant_race": "unknown",
                        "race": {"unknown": 100.0},
                        "warning": "AI model weights are missing. Face detected but analysis unavailable."
                    })
                fallback_results = {"faces": faces, "count": len(faces), "process_time": 0.5, "partial": True}
                return FaceAnalyzer._sanitize_results(fallback_results)
            except Exception as e2:
                logger.error(f"Detection fallback failed: {str(e2)}")
                return {"error": f"ML Engine error: {str(e)}"}

    def verify(self, img1_path, img2_path, model_name='VGG-Face'):
        """
        Verifies if two images contain the same person.
        Models: 'VGG-Face', 'Facenet', 'OpenFace', 'DeepFace', 'DeepID', 'ArcFace', 'Dlib', 'SFace', 'GhostFaceNet'
        """
        try:
            start_time = time.time()
            result = DeepFace.verify(
                img1_path=img1_path,
                img2_path=img2_path,
                model_name=model_name,
                detector_backend=self.detector_backend,
                enforce_detection=False,
                silent=True
            )
            process_time = time.time() - start_time
            result['process_time'] = process_time
            return FaceAnalyzer._sanitize_results(result)
        except Exception as e:
            logger.error(f"Verification failed: {str(e)}")
            return {"error": str(e)}

    def find_in_db(self, img_path, db_path, model_name='VGG-Face'):
        """
        Finds the closest matches in a database folder.
        """
        try:
            start_time = time.time()
            results = DeepFace.find(
                img_path=img_path,
                db_path=db_path,
                model_name=model_name,
                detector_backend=self.detector_backend,
                enforce_detection=False,
                silent=True
            )
            process_time = time.time() - start_time
            logger.info(f"Search in DB completed in {process_time:.2f}s")
            # results is a list of dataframes
            matches = []
            if isinstance(results, list):
                for df in results:
                    if not df.empty:
                        matches.append(df.to_dict('records'))
            final_matches = {"matches": matches, "process_time": process_time}
            return FaceAnalyzer._sanitize_results(final_matches)
        except Exception as e:
            logger.error(f"Database search failed: {str(e)}")
            return {"error": str(e)}

analyzer = FaceAnalyzer()
