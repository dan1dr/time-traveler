"use client";

import { useState } from "react";

export function LanguageToggle({
  value,
  onChange,
}: {
  value: "en" | "es";
  onChange: (val: "en" | "es") => void;
}) {
  const [filling, setFilling] = useState<"en" | "es" | null>(null);

  function handleClick(next: "en" | "es") {
    setFilling(next);
    onChange(next);
    setTimeout(() => setFilling(null), 500);
  }
  return (
    <div className="inline-flex rounded-2xl overflow-hidden" style={{
      background: 'linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.03))',
      border: '1px solid rgba(255,255,255,0.25)',
      backdropFilter: 'blur(15px) saturate(150%)',
      boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.2), 0 4px 16px rgba(0,0,0,0.1)'
    }}>
      <button
        type="button"
        onClick={() => handleClick("en")}
        className={`px-3 sm:px-4 py-2 sm:py-3 text-sm sm:text-base transition-all duration-200 relative overflow-hidden btn-reflect btn-liquid ${
          value === "en"
            ? "text-white"
            : "text-slate-200 hover:bg-white/10"
        } ${filling === 'en' ? 'is-filling' : ''}`}
        style={value === "en" ? {
          background: 'linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.08))',
          borderRight: '1px solid rgba(255,255,255,0.2)'
        } : {
          borderRight: '1px solid rgba(255,255,255,0.1)'
        }}
      >
        English
        <span className="pointer-events-none absolute inset-0 opacity-0 hover:opacity-100 transition-opacity" style={{background:'radial-gradient(40% 60% at 10% 50%, rgba(255,255,255,0.25), rgba(255,255,255,0))'}}/>
      </button>
      <button
        type="button"
        onClick={() => handleClick("es")}
        className={`px-3 sm:px-4 py-2 sm:py-3 text-sm sm:text-base transition-all duration-200 relative overflow-hidden btn-reflect btn-liquid ${
          value === "es"
            ? "text-white"
            : "text-slate-200 hover:bg-white/10"
        } ${filling === 'es' ? 'is-filling' : ''}`}
        style={value === "es" ? {
          background: 'linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.08))'
        } : {}}
      >
        Español
        <span className="pointer-events-none absolute inset-0 opacity-0 hover:opacity-100 transition-opacity" style={{background:'radial-gradient(40% 60% at 10% 50%, rgba(255,255,255,0.25), rgba(255,255,255,0))'}}/>
      </button>
    </div>
  );
}


