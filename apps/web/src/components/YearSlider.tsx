"use client";

import { useMemo, useState } from "react";

export function YearSlider({
  value,
  onChange,
}: {
  value: number;
  onChange: (val: number) => void;
}) {
  const era = useMemo(() => getEraForYear(value), [value]);
  const [isSliding, setIsSliding] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(parseInt(e.target.value, 10));
  };

  return (
    <div className="relative">
      {/* Centered Year Display with Zoom Animation */}
      <div className="text-center mb-6 year-header" style={{minHeight:'8.5rem'}}>
        <div className="text-sm uppercase tracking-wider text-slate-400 mb-1">Era</div>
        <div className={`text-2xl font-semibold transition-transform duration-300 fk-grotesk-light will-change-transform`}
          style={{transform: isSliding ? 'scale(1.06)' : 'scale(1)'}}>
          {era.label}
        </div>
        <div className="text-slate-300 text-sm mb-4" style={{minHeight:'1.25rem'}}>{era.range}</div>
        
        {/* Year with zoom effect */}
        <div className={`text-4xl font-bold transition-transform duration-200`}
          style={{transform: isSliding ? 'scale(1.12)' : 'scale(1)'}}>
          {value}
        </div>
      </div>

      {/* Crystal Slider Container */}
      <div className="relative px-4">
        {/* Elegant Axis Markers */}
        <div className="absolute inset-x-4 -bottom-6 flex justify-between text-xs axis-labels pointer-events-none">
          <span className="transform -translate-x-2">0</span>
          <span className="transform -translate-x-3">1000</span>
          <span className="transform -translate-x-3">2000</span>
          <span className="transform translate-x-2">3000</span>
        </div>
        
        {/* Axis ticks */}
        <div className="absolute inset-x-4 top-4 flex justify-between pointer-events-none">
          {[0, 1000, 2000, 3000].map((tick) => (
            <div key={tick} className="w-px h-2 bg-slate-600"></div>
          ))}
        </div>

        {/* Crystal Slider Track */}
        <div className="relative mt-8">
          <div className="absolute inset-x-0 top-1/2 transform -translate-y-1/2 h-2 rounded-full"
               style={{
                 background: 'linear-gradient(90deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05))',
                 border: '1px solid rgba(255,255,255,0.2)',
                 backdropFilter: 'blur(10px)'
               }}
          />
          
          {/* Custom Range Input */}
          <input
            type="range"
            min={0}
            max={3000}
            step={1}
            value={value}
            onChange={handleChange}
            onMouseDown={() => setIsSliding(true)}
            onMouseUp={() => setIsSliding(false)}
            onTouchStart={() => setIsSliding(true)}
            onTouchEnd={() => setIsSliding(false)}
            className="crystal-slider w-full h-6 bg-transparent appearance-none cursor-pointer relative z-10"
            style={{
              background: 'transparent'
            }}
          />
        </div>
      </div>

      {/* Era Description */}
      <div className="mt-10 text-center text-sm text-slate-300 max-w-xs mx-auto" style={{
        minHeight: '2.6rem',
        display: '-webkit-box',
        WebkitLineClamp: 2 as any,
        WebkitBoxOrient: 'vertical' as any,
        overflow: 'hidden'
      }}>
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
  return { label: "Far Future", range: "2500–3000", description: "Galactic consciousness—beyond linear time." };
}


