"use client";

import { useMemo, useState } from "react";
import { CountryPhoneInput, PhoneValue } from "@/components/CountryPhoneInput";
import { YearSlider } from "@/components/YearSlider";
import { LanguageToggle } from "@/components/LanguageToggle";

export default function Home() {
  const [phone, setPhone] = useState<PhoneValue>({ dial: "+34", number: "" });
  const [year, setYear] = useState<number>(1580);
  const [lang, setLang] = useState<"en" | "es">("en");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const isValid = useMemo(() => {
    return phone.number.length >= 6; // simple check; Twilio will validate fully
  }, [phone.number]);

  async function initiateCall() {
    setLoading(true);
    setMessage(null);
    try {
      const backend =
        process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
      const res = await fetch(`${backend}/outbound-call`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          to: `${phone.dial}${phone.number}`,
          lang,
          year,
        }),
      });
      const data = await res.json();
      if (!res.ok || !data.success) {
        throw new Error(data?.error || "Failed to initiate call");
      }
      setMessage("📞 Call initiated! Answer the phone to meet your traveler.");
    } catch (err: any) {
      setMessage(`❌ ${err.message || "Something went wrong"}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center px-4">
      <div className="max-w-3xl w-full">
        <header className="mb-8 text-center">
          <h1 className="text-4xl font-extrabold tracking-tight">
            Time Traveler Hotline
          </h1>
          <p className="text-slate-300 mt-2">
            Receive a live call from any era—powered by ElevenLabs + Twilio
          </p>
        </header>

        <section className="glass rounded-2xl p-6 shadow-glow">
          <div className="grid gap-6">
            <div className="grid gap-2">
              <label className="text-sm text-slate-300">Language</label>
              <LanguageToggle value={lang} onChange={setLang} />
            </div>

            <div className="grid gap-2">
              <label className="text-sm text-slate-300">Your Phone</label>
              <CountryPhoneInput value={phone} onChange={setPhone} />
              <p className="text-xs text-slate-400">We will call this number immediately.</p>
            </div>

            <div className="grid gap-2">
              <label className="text-sm text-slate-300">Choose Year</label>
              <YearSlider value={year} onChange={setYear} />
            </div>

            <button
              onClick={initiateCall}
              disabled={!isValid || loading}
              className="btn-primary h-11 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Calling..." : "Call Me"}
            </button>

            {message && (
              <div className="text-sm text-slate-200">{message}</div>
            )}
          </div>
        </section>

        <footer className="text-center text-xs text-slate-500 mt-6">
          Built with ❤️ using ElevenLabs, Twilio, and FastAPI
        </footer>
      </div>
    </main>
  );
}


