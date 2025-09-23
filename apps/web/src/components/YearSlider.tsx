"use client";

import { useMemo } from "react";

export function YearSlider({
  value,
  onChange,
}: {
  value: number;
  onChange: (val: number) => void;
}) {
  const era = useMemo(() => getEraForYear(value), [value]);

  return (
    <div>
      <div className="flex items-end justify-between mb-2">
        <div>
          <div className="text-sm uppercase tracking-wider text-slate-400">Era</div>
          <div className="text-xl font-semibold">{era.label}</div>
          <div className="text-slate-400 text-sm">{era.range}</div>
        </div>
        <div className="text-right">
          <div className="text-sm uppercase tracking-wider text-slate-400">Year</div>
          <div className="text-2xl font-bold">{value}</div>
        </div>
      </div>
      <input
        type="range"
        min={0}
        max={5000}
        step={1}
        value={value}
        onChange={(e) => onChange(parseInt(e.target.value, 10))}
        className="w-full accent-primary"
      />
      <div className="mt-2 text-sm text-slate-400">
        {era.description}
      </div>
    </div>
  );
}

function getEraForYear(year: number) {
  if (year <= 500) return { label: "Ancient Times", range: "0–500", description: "Philosophy, myth, empire—reverence for gods and nature." };
  if (year <= 1500) return { label: "Medieval", range: "500–1500", description: "Honor and faith—feudal order and chivalry." };
  if (year <= 1600) return { label: "Renaissance", range: "1400–1600", description: "Arts and sciences flourish—curiosity awakens." };
  if (year <= 1750) return { label: "Baroque", range: "1600–1750", description: "Refinement and grandeur—courts and ornament." };
  if (year <= 1900) return { label: "Industrial", range: "1750–1900", description: "Steam and steel—cities, factories, invention." };
  if (year <= 1950) return { label: "Early Modern", range: "1900–1950", description: "Acceleration and upheaval—radio to rockets." };
  if (year <= 2000) return { label: "Mid-Late 20th", range: "1950–2000", description: "Groovy modernity—space age and culture waves." };
  if (year <= 2030) return { label: "Contemporary", range: "2000–2030", description: "Connected world—digital transformation everywhere." };
  if (year <= 2050) return { label: "AI Renaissance", range: "2030–2050", description: "Human–AI symbiosis—short, sharp insights." };
  if (year <= 2200) return { label: "Interplanetary", range: "2050–2200", description: "Multi-planetary—Martian colonies, orbital links." };
  if (year <= 2500) return { label: "Transcendent", range: "2200–2500", description: "Post-human perspectives—energy and information." };
  return { label: "Far Future", range: "2500+", description: "Galactic consciousness—beyond linear time." };
}


