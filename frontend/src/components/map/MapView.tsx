"use client";

import { useEffect, useRef } from 'react';
import * as maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import { Candidate } from '@/lib/api';

interface MapViewProps {
  candidates: Candidate[];
  selectedCandidateId: string | null;
  onSelectCandidate: (id: string) => void;
}

export function MapView({ candidates, selectedCandidateId, onSelectCandidate }: MapViewProps) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const markers = useRef<{ [id: string]: maplibregl.Marker }>({});

  useEffect(() => {
    if (!mapContainer.current) return;

    if (!map.current) {
      map.current = new maplibregl.Map({
        container: mapContainer.current,
        style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
        center: [73.8567, 18.5204],
        zoom: 12
      });

      map.current.addControl(new maplibregl.NavigationControl(), 'top-right');
    }
  }, []);

  useEffect(() => {
    if (!map.current) return;

    // Clear old markers
    Object.values(markers.current).forEach(marker => marker.remove());
    markers.current = {};

    // Add new markers
    candidates.forEach(candidate => {
      const el = document.createElement('div');
      el.className = `w-6 h-6 rounded-full border-2 cursor-pointer shadow-md transition-all ${
        candidate.id === selectedCandidateId
          ? 'bg-blue-500 border-white scale-125 z-10'
          : 'bg-red-500 border-white hover:scale-110'
      }`;

      el.addEventListener('click', (e) => {
        e.stopPropagation();
        onSelectCandidate(candidate.id);
      });

      const marker = new maplibregl.Marker({ element: el })
        .setLngLat([candidate.location.lon, candidate.location.lat])
        .addTo(map.current!);

      markers.current[candidate.id] = marker;
    });

    if (selectedCandidateId && markers.current[selectedCandidateId]) {
      const selected = candidates.find(c => c.id === selectedCandidateId);
      if (selected && map.current) {
        map.current.flyTo({
          center: [selected.location.lon, selected.location.lat],
          zoom: 15,
          duration: 1000
        });
      }
    }

  }, [candidates, selectedCandidateId, onSelectCandidate]);

  return (
    <div ref={mapContainer} className="w-full h-full" />
  );
}