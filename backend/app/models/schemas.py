from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class SearchRequest(BaseModel):
    query: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    sensor: Optional[str] = None
    top_k: int = 20

class Location(BaseModel):
    lat: float
    lon: float

class ChangeInfo(BaseModel):
    type: str
    confidence: float
    earliest_supported: str

class Observation(BaseModel):
    date: str
    image: str

class Candidate(BaseModel):
    id: str
    location: Location
    semantic_score: float
    change: Optional[ChangeInfo] = None
    observations: Optional[List[Observation]] = None

class CandidateReview(BaseModel):
    decision: str  # confirmed, rejected, uncertain

class CandidateDetail(BaseModel):
    id: str
    location: Location
    semantic_score: float
    quality: float
    change: ChangeInfo

class TimelineResponse(BaseModel):
    observations: List[Dict[str, Any]]

class ChangeResponse(BaseModel):
    type: str
    confidence: float
    earliest_supported: str
    geometry: Dict[str, Any]
