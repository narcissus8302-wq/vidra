export const API_BASE_URL = "http://localhost:8000/api";

export interface Location {
    lat: number;
    lon: number;
}

export interface ChangeInfo {
    type: string;
    confidence: number;
    earliest_supported: string;
}

export interface Observation {
    date: string;
    image: string;
}

export interface Candidate {
    id: string;
    location: Location;
    semantic_score: number;
    change?: ChangeInfo;
    observations?: Observation[];
}

export interface CandidateDetail extends Candidate {
    quality: number;
    review?: { decision: string, timestamp: string, analyst: string };
}

export async function searchCandidates(query: string): Promise<Candidate[]> {
    const res = await fetch(`${API_BASE_URL}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, top_k: 20 })
    });
    return res.json();
}

export async function getCandidate(id: string): Promise<CandidateDetail> {
    const res = await fetch(`${API_BASE_URL}/candidates/${id}`);
    return res.json();
}

export async function getTimeline(id: string): Promise<{ observations: Record<string, unknown>[] }> {
    const res = await fetch(`${API_BASE_URL}/candidates/${id}/timeline`);
    return res.json();
}

export async function getChange(id: string): Promise<Record<string, unknown>> {
    const res = await fetch(`${API_BASE_URL}/candidates/${id}/change`);
    return res.json();
}

export async function reviewCandidate(id: string, decision: string): Promise<Record<string, unknown>> {
    const res = await fetch(`${API_BASE_URL}/candidates/${id}/review`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ decision })
    });
    return res.json();
}