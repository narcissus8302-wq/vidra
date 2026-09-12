import { Candidate } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Activity } from "lucide-react";

interface SearchResultsProps {
  candidates: Candidate[];
  selectedId: string | null;
  onSelect: (id: string) => void;
}

export function SearchResults({ candidates, selectedId, onSelect }: SearchResultsProps) {
  if (candidates.length === 0) {
    return <div className="p-4 text-center text-muted-foreground text-sm">No results found.</div>;
  }

  return (
    <div className="space-y-3 p-4">
      <div className="text-sm font-medium text-muted-foreground mb-4">
        RESULTS — {candidates.length} CANDIDATES
      </div>
      {candidates.map((c) => (
        <Card
          key={c.id}
          className={`cursor-pointer transition-colors hover:bg-accent/50 ${selectedId === c.id ? 'border-primary ring-1 ring-primary' : ''}`}
          onClick={() => onSelect(c.id)}
        >
          <CardContent className="p-4 flex flex-col gap-2">
            <div className="flex justify-between items-start">
              <span className="font-semibold text-sm">Candidate {c.id.split('-')[1]}</span>
              {c.change && <Badge variant="secondary">{c.change.type}</Badge>}
            </div>
            <div className="grid grid-cols-2 gap-2 text-xs text-muted-foreground mt-2">
              <div className="flex items-center gap-1">
                <Activity className="h-3 w-3" /> Rel: {Math.round(c.semantic_score * 100)}%
              </div>
              {c.change && (
                <div className="flex items-center gap-1 text-right justify-end text-blue-600 dark:text-blue-400">
                  Conf: {Math.round(c.change.confidence * 100)}%
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}