from typing import List, Dict, Any, Optional
from app.models.schemas import SearchRequest, Candidate, CandidateReview

# Mock In-Memory State
_MOCK_REVIEWS: Dict[str, Dict[str, Any]] = {}

class MockSearchService:
    @staticmethod
    def search(request: SearchRequest) -> List[Candidate]:
        # Return mock candidates
        return [
            Candidate(
                id="candidate-001",
                location={"lat": 18.5204, "lon": 73.8567},
                semantic_score=0.94,
                change={"type": "construction", "confidence": 0.91, "earliest_supported": "2025-07-14"},
                observations=[
                    {"date": "2024-01-12", "image": "/api/static/demo/candidate-001/2024-01.jpg"},
                    {"date": "2025-07-14", "image": "/api/static/demo/candidate-001/2025-07.jpg"}
                ]
            ),
            Candidate(
                id="candidate-002",
                location={"lat": 18.5254, "lon": 73.8617},
                semantic_score=0.89,
                change={"type": "clearance", "confidence": 0.84, "earliest_supported": "2025-06-10"},
                observations=[]
            )
        ]

class MockChangeService:
    @staticmethod
    def get_candidate(candidate_id: str) -> Dict[str, Any]:
        return {
            "id": candidate_id,
            "location": {"lat": 18.5204, "lon": 73.8567},
            "semantic_score": 0.94,
            "quality": 0.91,
            "change": {
                "type": "construction",
                "confidence": 0.91,
                "earliest_supported": "2025-07-14"
            }
        }

    @staticmethod
    def get_timeline(candidate_id: str) -> Dict[str, Any]:
        return {
            "observations": [
                {
                    "date": "2024-01-12",
                    "scene_id": "S2A_20240112",
                    "quality": 0.95,
                    "image": f"/api/static/demo/{candidate_id}/2024-01.jpg"
                },
                {
                    "date": "2025-07-14",
                    "scene_id": "S2A_20250714",
                    "quality": 0.92,
                    "image": f"/api/static/demo/{candidate_id}/2025-07.jpg"
                }
            ]
        }

    @staticmethod
    def get_change(candidate_id: str) -> Dict[str, Any]:
        return {
            "type": "construction",
            "confidence": 0.91,
            "earliest_supported": "2025-07-14",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[73.8567, 18.5204], [73.8577, 18.5204], [73.8577, 18.5214], [73.8567, 18.5214], [73.8567, 18.5204]]]
            },
            "change_mask_url": f"/api/static/demo/{candidate_id}/change-mask.png"
        }

class MockReviewService:
    @staticmethod
    def submit_review(candidate_id: str, review: CandidateReview) -> Dict[str, Any]:
        import datetime
        _MOCK_REVIEWS[candidate_id] = {
            "decision": review.decision,
            "timestamp": datetime.datetime.now().isoformat(),
            "analyst": "demo-user"
        }
        return {"status": "success", "review": _MOCK_REVIEWS[candidate_id]}

    @staticmethod
    def get_review(candidate_id: str) -> Optional[Dict[str, Any]]:
        return _MOCK_REVIEWS.get(candidate_id)
