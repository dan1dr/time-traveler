"use client";

import { useMemo, useState } from "react";

type Country = {
  code: string; // ISO-2
  name: string;
  dial: string; // +xx
  flag: string; // emoji
};

const COUNTRIES: Country[] = [
  { code: "US", name: "United States", dial: "+1", flag: "🇺🇸" },
  { code: "ES", name: "Spain", dial: "+34", flag: "🇪🇸" },
  { code: "GB", name: "United Kingdom", dial: "+44", flag: "🇬🇧" },
  { code: "DE", name: "Germany", dial: "+49", flag: "🇩🇪" },
  { code: "FR", name: "France", dial: "+33", flag: "🇫🇷" },
  { code: "MX", name: "Mexico", dial: "+52", flag: "🇲🇽" },
  { code: "AR", name: "Argentina", dial: "+54", flag: "🇦🇷" },
];

export type PhoneValue = {
  dial: string;
  number: string;
};

export function CountryPhoneInput({
  value,
  onChange,
}: {
  value: PhoneValue;
  onChange: (val: PhoneValue) => void;
}) {
  const [open, setOpen] = useState(false);

  const selected = useMemo(() => {
    return COUNTRIES.find((c) => c.dial === value.dial) || COUNTRIES[0];
  }, [value.dial]);

  return (
    <div className="flex gap-2">
      <div className="relative">
        <button
          type="button"
          className="input pr-10 flex items-center gap-2 min-w-[120px]"
          onClick={() => setOpen((v) => !v)}
        >
          <span className="text-xl">{selected.flag}</span>
          <span className="text-sm text-slate-300">{selected.name}</span>
          <span className="ml-auto text-slate-400">{selected.dial}</span>
        </button>
        {open && (
          <div className="absolute z-20 mt-1 w-full max-h-60 overflow-auto glass rounded-lg p-1">
            {COUNTRIES.map((c) => (
              <button
                key={c.code}
                type="button"
                onClick={() => {
                  onChange({ dial: c.dial, number: value.number });
                  setOpen(false);
                }}
                className={`w-full text-left px-3 py-2 rounded-md hover:bg-white/5 flex items-center gap-2 ${
                  c.dial === value.dial ? "bg-white/5" : ""
                }`}
              >
                <span className="text-xl">{c.flag}</span>
                <span className="text-sm">{c.name}</span>
                <span className="ml-auto text-slate-400">{c.dial}</span>
              </button>
            ))}
          </div>
        )}
      </div>
      <input
        type="tel"
        inputMode="tel"
        className="input w-full"
        placeholder="Phone number"
        value={value.number}
        onChange={(e) => {
          const digits = e.target.value.replace(/[^0-9]/g, "");
          onChange({ dial: value.dial, number: digits });
        }}
      />
    </div>
  );
}


