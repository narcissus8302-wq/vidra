"use client";

import { useEffect, useState } from "react";
import { CandidateDetail, getCandidate, getTimeline, getChange, reviewCandidate } from "@/lib/api";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Loader2, Check, X, HelpCircle, ArrowRight } from "lucide-react";
import { Separator } from "@/components/ui/separator";

interface CandidatePanelProps {
  candidateId: string;
  onClose: () => void;
}

export function CandidatePanel({ candidateId, onClose }: CandidatePanelProps) {
  const [detail, setDetail] = useState<CandidateDetail | null>(null);
  const [timeline, setTimeline] = useState<Record<string, unknown> | null>(null);
  const [change, setChange] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(true);
  const [reviewStatus, setReviewStatus] = useState<string>("unreviewed");

  const [selectedObsIdx, setSelectedObsIdx] = useState<number>(0);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const [d, t, c] = await Promise.all([
          getCandidate(candidateId),
          getTimeline(candidateId),
          getChange(candidateId)
        ]);
        setDetail(d);
        setTimeline(t);
        setChange(c);
        if (d.review) setReviewStatus(d.review.decision);
        if (t.observations && t.observations.length > 0) setSelectedObsIdx(t.observations.length - 1);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [candidateId]);

  const handleReview = async (decision: string) => {
    setReviewStatus(decision); // optimistic
    await reviewCandidate(candidateId, decision);
  };

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (!detail || !timeline) return <div className="p-4">Failed to load data.</div>;

  const obs = (timeline.observations as Record<string, unknown>[]) || [];
  const selectedObs = obs[selectedObsIdx];
  const firstObs = obs[0];
  const lastObs = obs[obs.length - 1];

  return (
    <div className="flex flex-col h-full bg-background">
      <div className="p-4 flex items-center justify-between border-b">
        <div>
          <h2 className="font-semibold">LOCATION {detail.id.split('-')[1]}</h2>
          <div className="text-xs text-muted-foreground">
            {detail.location.lat.toFixed(4)}° N, {detail.location.lon.toFixed(4)}° E
          </div>
        </div>
        <Button variant="ghost" size="sm" onClick={onClose}>Close</Button>
      </div>

      <Tabs defaultValue="visual" className="flex-1 flex flex-col min-h-0">
        <TabsList className="w-full rounded-none border-b bg-transparent justify-start h-auto p-0">
          <TabsTrigger value="visual" className="rounded-none data-[state=active]:border-b-2 data-[state=active]:border-primary py-3">Visual</TabsTrigger>
          <TabsTrigger value="details" className="rounded-none data-[state=active]:border-b-2 data-[state=active]:border-primary py-3">Details</TabsTrigger>
        </TabsList>

        <TabsContent value="visual" className="flex-1 overflow-auto p-4 flex flex-col gap-6 m-0">
          {/* Before/After Viewer Mock */}
          <div className="space-y-4">
            <div className="flex justify-between items-center text-sm font-medium">
              <span>{firstObs ? (firstObs.date as string) : ''}</span>
              <ArrowRight className="h-4 w-4 text-muted-foreground" />
              <span>{lastObs ? (lastObs.date as string) : ''}</span>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <div className="aspect-video bg-muted rounded-md overflow-hidden relative">
                   {/* eslint-disable-next-line @next/next/no-img-element */}
                   <img src={`http://localhost:8000${firstObs ? String(firstObs.image) : ''}`} className="object-cover w-full h-full" alt="Before" />
                </div>
                <div className="text-center text-xs text-muted-foreground">BEFORE</div>
              </div>
              <div className="space-y-2">
                <div className="aspect-video bg-muted rounded-md overflow-hidden relative group">
                   {/* eslint-disable-next-line @next/next/no-img-element */}
                   <img src={`http://localhost:8000${lastObs ? String(lastObs.image) : ''}`} className="object-cover w-full h-full" alt="After" />
                   {/* Change Mask Overlay */}
                   {change?.change_mask_url ? (
                     <div className="absolute inset-0 opacity-75 group-hover:opacity-100 transition-opacity">
                       {/* eslint-disable-next-line @next/next/no-img-element */}
                       <img src={`http://localhost:8000${String(change.change_mask_url)}`} className="object-cover w-full h-full mix-blend-multiply" alt="Mask" />
                     </div>
                   ) : null}
                </div>
                <div className="text-center text-xs text-muted-foreground">AFTER & MASK</div>
              </div>
            </div>
          </div>

          <Separator />

          {/* Timeline Mock */}
          <div className="space-y-3">
             <div className="text-sm font-medium">Timeline</div>
             <div className="flex justify-between items-center relative py-4">
                <div className="absolute left-0 right-0 h-0.5 bg-muted top-1/2 -translate-y-1/2 z-0" />
                {obs.map((o: Record<string, unknown>, i: number) => (
                  <button
                    key={i}
                    onClick={() => setSelectedObsIdx(i)}
                    className={`relative z-10 flex flex-col items-center gap-2 outline-none group`}
                  >
                    <div className={`w-4 h-4 rounded-full border-2 transition-colors ${i === selectedObsIdx ? 'bg-primary border-primary ring-4 ring-primary/20' : 'bg-background border-muted-foreground group-hover:border-primary'}`} />
                    <span className={`text-xs ${i === selectedObsIdx ? 'font-medium text-foreground' : 'text-muted-foreground'}`}>{typeof o.date === 'string' ? o.date.split('-')[0] : ''}</span>
                  </button>
                ))}
             </div>
          </div>

        </TabsContent>

        <TabsContent value="details" className="flex-1 overflow-auto p-4 space-y-6 m-0">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <div className="text-xs text-muted-foreground">SEMANTIC RELEVANCE</div>
              <div className="font-mono text-lg">{Math.round(detail.semantic_score * 100)}%</div>
            </div>
            <div className="space-y-1">
              <div className="text-xs text-muted-foreground">CHANGE CONFIDENCE</div>
              <div className="font-mono text-lg text-blue-600 dark:text-blue-400">{detail.change ? Math.round(detail.change.confidence * 100) : 0}%</div>
            </div>
            <div className="space-y-1">
              <div className="text-xs text-muted-foreground">TYPE</div>
              <div className="font-medium uppercase">{detail.change ? detail.change.type : 'Unknown'}</div>
            </div>
            <div className="space-y-1">
              <div className="text-xs text-muted-foreground">FIRST SUPPORTED CHANGE</div>
              <div className="font-medium">{detail.change ? detail.change.earliest_supported : 'N/A'}</div>
            </div>
          </div>

          <Separator />

          <div className="space-y-2">
            <div className="text-sm font-semibold text-muted-foreground uppercase">Provenance</div>
            <div className="text-xs space-y-1 font-mono text-muted-foreground bg-muted/50 p-3 rounded-md">
               <div>Sensor: Sentinel-2</div>
               <div>Acquired: {selectedObs ? (selectedObs.date as string) : ''}</div>
               <div>Scene ID: {selectedObs ? (selectedObs.scene_id as string) : ''}</div>
               <div>Quality: {selectedObs ? Number(selectedObs.quality) * 100 : 0}%</div>
               <div className="mt-2 pt-2 border-t border-border">Model Version: v0.3-shell</div>
               <div>Processing: Demo Mode</div>
            </div>
          </div>
        </TabsContent>
      </Tabs>

      {/* Review Actions */}
      <div className="p-4 border-t bg-muted/20">
        <div className="text-xs font-semibold text-muted-foreground mb-3 uppercase tracking-wider">Analyst Review</div>
        <div className="flex gap-2">
          <Button
            className="flex-1"
            variant={reviewStatus === 'confirmed' ? 'default' : 'outline'}
            onClick={() => handleReview('confirmed')}
          >
            <Check className="mr-2 h-4 w-4" /> Confirm
          </Button>
          <Button
            className="flex-1"
            variant={reviewStatus === 'rejected' ? 'destructive' : 'outline'}
            onClick={() => handleReview('rejected')}
          >
            <X className="mr-2 h-4 w-4" /> Reject
          </Button>
          <Button
            className="flex-1"
            variant={reviewStatus === 'uncertain' ? 'secondary' : 'outline'}
            onClick={() => handleReview('uncertain')}
          >
            <HelpCircle className="mr-2 h-4 w-4" /> Uncertain
          </Button>
        </div>
      </div>
    </div>
  );
}