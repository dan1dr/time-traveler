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
  const [showForm, setShowForm] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);

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

  function handleGuideMe() {
    setShowForm(true);
    setTimeout(() => setCurrentStep(1), 300);
  }

  function handleLanguageSelect(selectedLang: "en" | "es") {
    setLang(selectedLang);
    setTimeout(() => setCurrentStep(2), 500);
  }

  function handlePhoneComplete() {
    // Phone input no longer auto-advances
  }

  return (
    <main className="hero-bg min-h-screen flex items-center justify-center text-center px-6 relative overflow-hidden">
      <div className="max-w-5xl transition-all duration-700 ease-out">
        {/* Hero content */}
        <div 
          className={`transition-all duration-700 ease-out ${
            showForm ? 'opacity-0 transform -translate-y-8 pointer-events-none' : 'opacity-100 transform translate-y-0'
          }`}
        >
          <h1 className="text-6xl md:text-7xl lg:text-8xl font-extrabold leading-[1.08] fk-grotesk-light whitespace-nowrap">
            Call to another era.
          </h1>
          <p className="mt-5 text-slate-100 text-lg md:text-xl fk-grotesk-light">
            I am the Time Traveler Machine. Through quantum threads that bind all moments, I can bridge your present with voices from antiquity's depths or tomorrow's distant shores, delivering echoes across the eternal continuum directly to your realm.
          </p>
          <div className="mt-8 flex items-center justify-center gap-3">
            <button
              className="btn-primary h-12 px-8"
              onClick={handleGuideMe}
            >
              Guide me
            </button>
          </div>
        </div>

        {/* Progressive Form Steps */}
        <div 
          className={`transition-all duration-700 ease-out ${
            showForm ? 'opacity-100 transform translate-y-0' : 'opacity-0 transform translate-y-8 pointer-events-none absolute inset-0'
          }`}
        >
          <div className="max-w-md mx-auto min-h-[200px] flex items-center justify-center">
            
            {/* Step 1: Language Selection */}
            {currentStep === 1 && (
              <div className="step-enter step-enter-active w-full">
                <div className="text-center mb-6">
                  <h2 className="text-2xl font-semibold mb-2 fk-grotesk-light">Choose your tongue</h2>
                  <p className="text-slate-300 text-sm">In which ancient words shall we speak?</p>
                </div>
                <div className="flex justify-center">
                  <LanguageToggle value={lang} onChange={handleLanguageSelect} />
                </div>
              </div>
            )}

            {/* Step 2: Phone Input */}
            {currentStep === 2 && (
              <div className="step-enter step-enter-active w-full">
                <div className="text-center mb-6">
                  <h2 className="text-2xl font-semibold mb-2 fk-grotesk-light">Your number to the portal of eternity</h2>
                  <p className="text-slate-300 text-sm">Through which vessel shall the call manifest?</p>
                </div>
                <div className="space-y-4">
                  <CountryPhoneInput 
                    value={phone} 
                    onChange={setPhone}
                  />
                  {phone.number.length >= 6 && (
                    <div className="text-center">
                      <button
                        onClick={() => setCurrentStep(3)}
                        className="btn-primary h-10 px-6"
                      >
                        Proceed to temporal gateway
                      </button>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Step 3: Year Selection */}
            {currentStep === 3 && (
              <div className="step-enter step-enter-active w-full">
                <div className="text-center mb-6">
                  <h2 className="text-2xl font-semibold mb-2 fk-grotesk-light">Navigate the temporal void</h2>
                  <p className="text-slate-300 text-sm">Drift through epochs... where will you anchor?</p>
                </div>
                <div className="relative">
                  <div className="absolute -top-4 right-8 w-2 h-2 rounded-full sparkle" />
                  <div className="absolute top-2 right-16 w-1.5 h-1.5 rounded-full sparkle" style={{animationDelay: '0.6s'}} />
                  <div className="absolute -top-2 left-12 w-1 h-1 rounded-full sparkle" style={{animationDelay: '1.2s'}} />
                  <YearSlider value={year} onChange={setYear} />
                </div>
                <div className="text-center mt-8">
                  <button
                    onClick={initiateCall}
                    disabled={!isValid || loading}
                    className={`btn-primary h-12 px-8 disabled:opacity-50 disabled:cursor-not-allowed ${
                      loading ? 'travel-machine-activating' : ''
                    }`}
                  >
                    {loading ? "Piercing the veil..." : "Summon the Voice"}
                  </button>
                  
                  {message && (
                    <div className="text-sm text-slate-200 mt-4">{message}</div>
                  )}
                </div>
              </div>
            )}

            {/* Back Button */}
            <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-12">
              <button
                onClick={() => {
                  setShowForm(false);
                  setCurrentStep(0);
                }}
                className="text-xs text-slate-400 hover:text-slate-200 transition-colors"
              >
                ← Return to the beginning
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}


