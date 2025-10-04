"use client";

import { useMemo, useState } from "react";

type Country = {
  code: string; // ISO-2
  name: string;
  dial: string; // +xx
  flag: string; // emoji
};

// Comprehensive country list with dial codes
const COUNTRIES: Country[] = [
  { code: "US", name: "United States", dial: "+1", flag: "🇺🇸" },
  { code: "CA", name: "Canada", dial: "+1", flag: "🇨🇦" },
  { code: "MX", name: "Mexico", dial: "+52", flag: "🇲🇽" },
  { code: "AR", name: "Argentina", dial: "+54", flag: "🇦🇷" },
  { code: "BR", name: "Brazil", dial: "+55", flag: "🇧🇷" },
  { code: "CL", name: "Chile", dial: "+56", flag: "🇨🇱" },
  { code: "CO", name: "Colombia", dial: "+57", flag: "🇨🇴" },
  { code: "PE", name: "Peru", dial: "+51", flag: "🇵🇪" },
  { code: "VE", name: "Venezuela", dial: "+58", flag: "🇻🇪" },
  { code: "UY", name: "Uruguay", dial: "+598", flag: "🇺🇾" },
  { code: "PY", name: "Paraguay", dial: "+595", flag: "🇵🇾" },
  { code: "BO", name: "Bolivia", dial: "+591", flag: "🇧🇴" },
  { code: "EC", name: "Ecuador", dial: "+593", flag: "🇪🇨" },
  { code: "GT", name: "Guatemala", dial: "+502", flag: "🇬🇹" },
  { code: "CR", name: "Costa Rica", dial: "+506", flag: "🇨🇷" },
  { code: "PA", name: "Panama", dial: "+507", flag: "🇵🇦" },
  { code: "DO", name: "Dominican Republic", dial: "+1", flag: "🇩🇴" },
  { code: "PR", name: "Puerto Rico", dial: "+1", flag: "🇵🇷" },
  { code: "CU", name: "Cuba", dial: "+53", flag: "🇨🇺" },
  { code: "HN", name: "Honduras", dial: "+504", flag: "🇭🇳" },
  { code: "NI", name: "Nicaragua", dial: "+505", flag: "🇳🇮" },
  { code: "SV", name: "El Salvador", dial: "+503", flag: "🇸🇻" },
  { code: "JM", name: "Jamaica", dial: "+1", flag: "🇯🇲" },
  { code: "TT", name: "Trinidad and Tobago", dial: "+1", flag: "🇹🇹" },

  { code: "GB", name: "United Kingdom", dial: "+44", flag: "🇬🇧" },
  { code: "IE", name: "Ireland", dial: "+353", flag: "🇮🇪" },
  { code: "FR", name: "France", dial: "+33", flag: "🇫🇷" },
  { code: "ES", name: "Spain", dial: "+34", flag: "🇪🇸" },
  { code: "PT", name: "Portugal", dial: "+351", flag: "🇵🇹" },
  { code: "IT", name: "Italy", dial: "+39", flag: "🇮🇹" },
  { code: "DE", name: "Germany", dial: "+49", flag: "🇩🇪" },
  { code: "AT", name: "Austria", dial: "+43", flag: "🇦🇹" },
  { code: "CH", name: "Switzerland", dial: "+41", flag: "🇨🇭" },
  { code: "BE", name: "Belgium", dial: "+32", flag: "🇧🇪" },
  { code: "NL", name: "Netherlands", dial: "+31", flag: "🇳🇱" },
  { code: "LU", name: "Luxembourg", dial: "+352", flag: "🇱🇺" },
  { code: "NO", name: "Norway", dial: "+47", flag: "🇳🇴" },
  { code: "SE", name: "Sweden", dial: "+46", flag: "🇸🇪" },
  { code: "DK", name: "Denmark", dial: "+45", flag: "🇩🇰" },
  { code: "FI", name: "Finland", dial: "+358", flag: "🇫🇮" },
  { code: "IS", name: "Iceland", dial: "+354", flag: "🇮🇸" },
  { code: "PL", name: "Poland", dial: "+48", flag: "🇵🇱" },
  { code: "CZ", name: "Czechia", dial: "+420", flag: "🇨🇿" },
  { code: "SK", name: "Slovakia", dial: "+421", flag: "🇸🇰" },
  { code: "HU", name: "Hungary", dial: "+36", flag: "🇭🇺" },
  { code: "RO", name: "Romania", dial: "+40", flag: "🇷🇴" },
  { code: "BG", name: "Bulgaria", dial: "+359", flag: "🇧🇬" },
  { code: "GR", name: "Greece", dial: "+30", flag: "🇬🇷" },
  { code: "TR", name: "Türkiye", dial: "+90", flag: "🇹🇷" },
  { code: "UA", name: "Ukraine", dial: "+380", flag: "🇺🇦" },
  { code: "RU", name: "Russia", dial: "+7", flag: "🇷🇺" },
  { code: "BY", name: "Belarus", dial: "+375", flag: "🇧🇾" },
  { code: "LT", name: "Lithuania", dial: "+370", flag: "🇱🇹" },
  { code: "LV", name: "Latvia", dial: "+371", flag: "🇱🇻" },
  { code: "EE", name: "Estonia", dial: "+372", flag: "🇪🇪" },
  { code: "SI", name: "Slovenia", dial: "+386", flag: "🇸🇮" },
  { code: "HR", name: "Croatia", dial: "+385", flag: "🇭🇷" },
  { code: "RS", name: "Serbia", dial: "+381", flag: "🇷🇸" },
  { code: "BA", name: "Bosnia & Herzegovina", dial: "+387", flag: "🇧🇦" },
  { code: "ME", name: "Montenegro", dial: "+382", flag: "🇲🇪" },
  { code: "MK", name: "North Macedonia", dial: "+389", flag: "🇲🇰" },
  { code: "AL", name: "Albania", dial: "+355", flag: "🇦🇱" },
  { code: "MD", name: "Moldova", dial: "+373", flag: "🇲🇩" },
  { code: "GE", name: "Georgia", dial: "+995", flag: "🇬🇪" },
  { code: "AM", name: "Armenia", dial: "+374", flag: "🇦🇲" },
  { code: "AZ", name: "Azerbaijan", dial: "+994", flag: "🇦🇿" },

  { code: "CN", name: "China", dial: "+86", flag: "🇨🇳" },
  { code: "JP", name: "Japan", dial: "+81", flag: "🇯🇵" },
  { code: "KR", name: "South Korea", dial: "+82", flag: "🇰🇷" },
  { code: "HK", name: "Hong Kong", dial: "+852", flag: "🇭🇰" },
  { code: "TW", name: "Taiwan", dial: "+886", flag: "🇹🇼" },
  { code: "SG", name: "Singapore", dial: "+65", flag: "🇸🇬" },
  { code: "MY", name: "Malaysia", dial: "+60", flag: "🇲🇾" },
  { code: "TH", name: "Thailand", dial: "+66", flag: "🇹🇭" },
  { code: "VN", name: "Vietnam", dial: "+84", flag: "🇻🇳" },
  { code: "PH", name: "Philippines", dial: "+63", flag: "🇵🇭" },
  { code: "ID", name: "Indonesia", dial: "+62", flag: "🇮🇩" },
  { code: "IN", name: "India", dial: "+91", flag: "🇮🇳" },
  { code: "PK", name: "Pakistan", dial: "+92", flag: "🇵🇰" },
  { code: "BD", name: "Bangladesh", dial: "+880", flag: "🇧🇩" },
  { code: "LK", name: "Sri Lanka", dial: "+94", flag: "🇱🇰" },
  { code: "NP", name: "Nepal", dial: "+977", flag: "🇳🇵" },
  { code: "BT", name: "Bhutan", dial: "+975", flag: "🇧🇹" },
  { code: "MM", name: "Myanmar", dial: "+95", flag: "🇲🇲" },
  { code: "KH", name: "Cambodia", dial: "+855", flag: "🇰🇭" },
  { code: "LA", name: "Laos", dial: "+856", flag: "🇱🇦" },
  { code: "MN", name: "Mongolia", dial: "+976", flag: "🇲🇳" },

  { code: "AU", name: "Australia", dial: "+61", flag: "🇦🇺" },
  { code: "NZ", name: "New Zealand", dial: "+64", flag: "🇳🇿" },
  { code: "FJ", name: "Fiji", dial: "+679", flag: "🇫🇯" },
  { code: "PG", name: "Papua New Guinea", dial: "+675", flag: "🇵🇬" },

  { code: "AE", name: "United Arab Emirates", dial: "+971", flag: "🇦🇪" },
  { code: "SA", name: "Saudi Arabia", dial: "+966", flag: "🇸🇦" },
  { code: "IL", name: "Israel", dial: "+972", flag: "🇮🇱" },
  { code: "PS", name: "Palestine", dial: "+970", flag: "🇵🇸" },
  { code: "IR", name: "Iran", dial: "+98", flag: "🇮🇷" },
  { code: "IQ", name: "Iraq", dial: "+964", flag: "🇮🇶" },
  { code: "JO", name: "Jordan", dial: "+962", flag: "🇯🇴" },
  { code: "LB", name: "Lebanon", dial: "+961", flag: "🇱🇧" },
  { code: "QA", name: "Qatar", dial: "+974", flag: "🇶🇦" },
  { code: "KW", name: "Kuwait", dial: "+965", flag: "🇰🇼" },
  { code: "OM", name: "Oman", dial: "+968", flag: "🇴🇲" },
  { code: "BH", name: "Bahrain", dial: "+973", flag: "🇧🇭" },
  { code: "YE", name: "Yemen", dial: "+967", flag: "🇾🇪" },
  { code: "SY", name: "Syria", dial: "+963", flag: "🇸🇾" },

  { code: "EG", name: "Egypt", dial: "+20", flag: "🇪🇬" },
  { code: "ZA", name: "South Africa", dial: "+27", flag: "🇿🇦" },
  { code: "NG", name: "Nigeria", dial: "+234", flag: "🇳🇬" },
  { code: "KE", name: "Kenya", dial: "+254", flag: "🇰🇪" },
  { code: "TZ", name: "Tanzania", dial: "+255", flag: "🇹🇿" },
  { code: "UG", name: "Uganda", dial: "+256", flag: "🇺🇬" },
  { code: "GH", name: "Ghana", dial: "+233", flag: "🇬🇭" },
  { code: "CI", name: "Côte d’Ivoire", dial: "+225", flag: "🇨🇮" },
  { code: "SN", name: "Senegal", dial: "+221", flag: "🇸🇳" },
  { code: "MA", name: "Morocco", dial: "+212", flag: "🇲🇦" },
  { code: "DZ", name: "Algeria", dial: "+213", flag: "🇩🇿" },
  { code: "TN", name: "Tunisia", dial: "+216", flag: "🇹🇳" },
  { code: "ET", name: "Ethiopia", dial: "+251", flag: "🇪🇹" },
  { code: "CM", name: "Cameroon", dial: "+237", flag: "🇨🇲" },
  { code: "ZW", name: "Zimbabwe", dial: "+263", flag: "🇿🇼" },
  { code: "ZM", name: "Zambia", dial: "+260", flag: "🇿🇲" },
  { code: "BW", name: "Botswana", dial: "+267", flag: "🇧🇼" },
  { code: "NA", name: "Namibia", dial: "+264", flag: "🇳🇦" },
  { code: "AO", name: "Angola", dial: "+244", flag: "🇦🇴" },
  { code: "MZ", name: "Mozambique", dial: "+258", flag: "🇲🇿" },
  { code: "MG", name: "Madagascar", dial: "+261", flag: "🇲🇬" },
  { code: "RW", name: "Rwanda", dial: "+250", flag: "🇷🇼" },
  { code: "SN", name: "Senegal", dial: "+221", flag: "🇸🇳" },

  { code: "CN", name: "China", dial: "+86", flag: "🇨🇳" },
];

export type PhoneValue = {
  dial: string;
  number: string;
};

export function CountryPhoneInput({
  value,
  onChange,
  onOpenChange,
}: {
  value: PhoneValue;
  onChange: (val: PhoneValue) => void;
  onOpenChange?: (open: boolean) => void;
}) {
  const [open, setOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const validatePhoneNumber = (phone: string) => {
    const cleaned = phone.replace(/[^\d+]/g, '');
    
    if (!cleaned.startsWith('+')) {
      return 'Phone number must start with country code (e.g., +1234567890)';
    }
    
    // Check total length (country code + phone number)
    if (cleaned.length < 12 || cleaned.length > 16) {
      return 'Phone number must be between 11-15 digits total (including country code)';
    }
    
    // Check if it has valid country code (1-3 digits) and phone number (7-15 digits)
    const phoneMatch = cleaned.match(/^\+(\d{1,3})(\d{7,15})$/);
    if (!phoneMatch) {
      return 'Invalid phone number format. Check country code and number length.';
    }
    
    return null;
  };

  const selected = useMemo(() => {
    return COUNTRIES.find((c) => c.dial === value.dial) || COUNTRIES[0];
  }, [value.dial]);

  function toggleOpen(next: boolean) {
    setOpen(next);
    if (onOpenChange) onOpenChange(next);
  }

  return (
    <div className={`flex flex-col sm:flex-row gap-2 overflow-visible`}>
      <div className="relative">
        <button
          type="button"
          className="input pr-10 flex items-center gap-2 min-w-full sm:min-w-[140px] text-sm"
          onClick={() => toggleOpen(!open)}
        >
          <span className="text-lg sm:text-xl">{selected.flag}</span>
          <span className="text-xs sm:text-sm text-slate-300 truncate">{selected.name}</span>
          <span className="ml-auto text-white text-sm">{selected.dial}</span>
        </button>
        {open && (
          <div className="absolute z-50 mt-1 w-[min(26rem,90vw)] max-h-72 overflow-auto crystal-panel crystal-scroll rounded-xl p-1 shadow-2xl">
            {COUNTRIES.map((c) => (
              <button
                key={c.code}
                type="button"
                onClick={() => {
                  onChange({ dial: c.dial, number: value.number });
                  toggleOpen(false);
                }}
                className={`w-full text-left px-3 py-2 rounded-lg hover:bg-white/5 flex items-center gap-2 ${
                  c.dial === value.dial ? "bg-white/5" : ""
                }`}
              >
                <span className="text-xl">{c.flag}</span>
                <span className="text-sm">{c.name}</span>
                <span className="ml-auto text-slate-200">{c.dial}</span>
              </button>
            ))}
          </div>
        )}
      </div>
      <div className="w-full">
        <input
          type="tel"
          inputMode="tel"
          className={`input w-full text-sm sm:text-base ${error ? 'border-red-400 focus:border-red-400' : ''}`}
          placeholder="Phone number"
          value={value.number}
          onChange={(e) => {
            const digits = e.target.value.replace(/[^0-9]/g, "");
            const newValue = { dial: value.dial, number: digits };
            onChange(newValue);
            
            // Validate the full phone number
            const fullPhone = `${value.dial}${digits}`;
            const validationError = validatePhoneNumber(fullPhone);
            setError(validationError);
          }}
        />
        {error && (
          <div className="text-xs text-red-400 mt-1">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}


