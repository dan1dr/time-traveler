"use client";

export function LanguageToggle({
  value,
  onChange,
}: {
  value: "en" | "es";
  onChange: (val: "en" | "es") => void;
}) {
  return (
    <div className="inline-flex rounded-2xl overflow-hidden" style={{
      background: 'linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.03))',
      border: '1px solid rgba(255,255,255,0.25)',
      backdropFilter: 'blur(15px) saturate(150%)',
      boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.2), 0 4px 16px rgba(0,0,0,0.1)'
    }}>
      <button
        type="button"
        onClick={() => onChange("en")}
        className={`px-3 py-2 text-sm transition-all duration-200 ${
          value === "en"
            ? "text-white"
            : "text-slate-200 hover:bg-white/10"
        }`}
        style={value === "en" ? {
          background: 'linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.08))',
          borderRight: '1px solid rgba(255,255,255,0.2)'
        } : {
          borderRight: '1px solid rgba(255,255,255,0.1)'
        }}
      >
        English
      </button>
      <button
        type="button"
        onClick={() => onChange("es")}
        className={`px-3 py-2 text-sm transition-all duration-200 ${
          value === "es"
            ? "text-white"
            : "text-slate-200 hover:bg-white/10"
        }`}
        style={value === "es" ? {
          background: 'linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.08))'
        } : {}}
      >
        Español
      </button>
    </div>
  );
}


