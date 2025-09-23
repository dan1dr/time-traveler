"use client";

export function LanguageToggle({
  value,
  onChange,
}: {
  value: "en" | "es";
  onChange: (val: "en" | "es") => void;
}) {
  return (
    <div className="inline-flex rounded-lg overflow-hidden border border-white/10">
      <button
        type="button"
        onClick={() => onChange("en")}
        className={`px-3 py-2 text-sm ${
          value === "en" ? "bg-primary text-white" : "bg-card/70 text-slate-300"
        }`}
      >
        English
      </button>
      <button
        type="button"
        onClick={() => onChange("es")}
        className={`px-3 py-2 text-sm ${
          value === "es" ? "bg-primary text-white" : "bg-card/70 text-slate-300"
        }`}
      >
        Español
      </button>
    </div>
  );
}


