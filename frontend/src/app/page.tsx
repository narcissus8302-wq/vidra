"use client";

import { useState } from "react";
import { SearchBar } from "@/components/search/SearchBar";
import { SearchResults } from "@/components/search/SearchResults";
import { MapView } from "@/components/map/MapView";
import { CandidatePanel } from "@/components/analysis/CandidatePanel";
import { Candidate, searchCandidates } from "@/lib/api";
import { Layers } from "lucide-react";

export default function Dashboard() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [isSearching, setIsSearching] = useState(false);

  const handleSearch = async (query: string) => {
    setIsSearching(true);
    try {
      const res = await searchCandidates(query);
      setCandidates(res);
      setSelectedId(null);
    } catch (e) {
      console.error(e);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="flex h-screen w-full overflow-hidden bg-background">
      {/* LEFT PANEL: Search & Results */}
      <div className="w-96 flex flex-col border-r shadow-sm z-10 bg-background relative">
        <div className="p-4 border-b">
          <div className="flex items-center gap-2 mb-4 font-semibold text-lg text-primary tracking-tight">
            <Layers className="h-5 w-5" />
            <span>SATELLITE ANALYST</span>
          </div>
          <SearchBar onSearch={handleSearch} isLoading={isSearching} />
        </div>
        <div className="flex-1 overflow-y-auto">
          <SearchResults
            candidates={candidates}
            selectedId={selectedId}
            onSelect={setSelectedId}
          />
        </div>
      </div>

      {/* CENTER: Map */}
      <div className="flex-1 relative bg-muted/20">
        <MapView
          candidates={candidates}
          selectedCandidateId={selectedId}
          onSelectCandidate={setSelectedId}
        />
      </div>

      {/* RIGHT PANEL: Analysis */}
      {selectedId && (
        <div className="w-[450px] border-l shadow-xl z-10 bg-background transition-all">
          <CandidatePanel
            key={selectedId}
            candidateId={selectedId}
            onClose={() => setSelectedId(null)}
          />
        </div>
      )}
    </div>
  );
}