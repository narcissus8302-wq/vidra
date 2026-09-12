from fastapi import APIRouter
from typing import List, Dict, Any
from app.models.schemas import SearchRequest, Candidate, CandidateDetail, TimelineResponse, ChangeResponse, CandidateReview
from app.services.mock_services import MockSearchService, MockChangeService, MockReviewService

api_router = APIRouter()

@api_router.get("/health")
def health_check():
    return {"status": "ok"}

@api_router.post("/search", response_model=List[Candidate])
def search(request: SearchRequest):
    return MockSearchService.search(request)

@api_router.get("/candidates/{candidate_id}", response_model=CandidateDetail)
def get_candidate(candidate_id: str):
    data = MockChangeService.get_candidate(candidate_id)
    # Inject mock review state if exists
    review = MockReviewService.get_review(candidate_id)
    if review:
        data["review"] = review
    return data

@api_router.get("/candidates/{candidate_id}/timeline", response_model=TimelineResponse)
def get_timeline(candidate_id: str):
    return MockChangeService.get_timeline(candidate_id)

@api_router.get("/candidates/{candidate_id}/change", response_model=ChangeResponse)
def get_change(candidate_id: str):
    data = MockChangeService.get_change(candidate_id)
    return data

@api_router.post("/candidates/{candidate_id}/review")
def review_candidate(candidate_id: str, review: CandidateReview):
    return MockReviewService.submit_review(candidate_id, review)

@api_router.get("/candidates/{candidate_id}/review")
def get_review(candidate_id: str):
    review = MockReviewService.get_review(candidate_id)
    if review:
        return review
    return {"decision": "unreviewed"}
