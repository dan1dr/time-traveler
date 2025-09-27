"use client";

import { useMemo, useState } from "react";
import { CountryPhoneInput, PhoneValue } from "@/components/CountryPhoneInput";
import { YearSlider } from "@/components/YearSlider";
import { LanguageToggle } from "@/components/LanguageToggle";

export default function Home() {
  const [phone, setPhone] = useState<PhoneValue>({ dial: "+34", number: "" });
  const [year, setYear] = useState<number>(2025);
  // UI language (top-right toggle)
  const [uiLang, setUiLang] = useState<"en" | "es">("en");
  // Voice language to send to backend (Step 1 selection)
  const [voiceLang, setVoiceLang] = useState<"en" | "es">("en");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [fillGuide, setFillGuide] = useState(false);
  const [fillProceed, setFillProceed] = useState(false);
  const [countryOpen, setCountryOpen] = useState(false);
  const [fillSummon, setFillSummon] = useState(false);
  const [impact, setImpact] = useState(false);
  const [preOverlay, setPreOverlay] = useState(false);
  const [showSpiral, setShowSpiral] = useState(false);
  const [showAbout, setShowAbout] = useState(false);
  const [randYear, setRandYear] = useState<number | null>(null);
  const [callingYear, setCallingYear] = useState<number | null>(null);
  const [hasInteracted, setHasInteracted] = useState(false);

  const isValid = useMemo(() => {
    return phone.number.length >= 6; // simple check; Twilio will validate fully
  }, [phone.number]);

  const DICT = {
    en: {
      heroTitle: "Call to another era.",
      heroSubtitle:
        "I am the Time Machine. I connect your present, through alchemy and artificial intelligence, with voices of the past and whispers of the future.",
      guideMe: "Guide me",
      chooseLanguage: "Choose your language",
      chooseLanguageSub: "Select how you wish to speak with the traveler.",
      phoneTitle: "Your number to the portal of eternity",
      phoneSub: "Leave us your phone to receive the call.",
      proceed: "Proceed to temporal gateway",
      step3Title: "Select the era, traveler.",
      step3Sub: "Pick a year and you will be called.",
      callMe: "Call me",
      loadingText: "Piercing the veil...",
      back: "← Return to the beginning",
      overlaySubtitle: "Activating travel machine...",
      checkPhone: "Check Your Phone",
      overlayStatus: "Connection bridging temporal dimensions...",
      about: "About",
      randomYear: "Random year",
      aboutTitle: "Time Traveler Machine",
      aboutContent: "Through ancient alchemical circles merged with quantum neural networks, this ethereal machine pierces the fabric of time itself. Each voice that emerges has been carefully extracted from the temporal streams, carrying the authentic essence of their era. The artificial consciousness learns not just language, but the very soul of each epoch—their hopes, fears, and wisdom echoing across the infinite corridor of existence.",
    },
    es: {
      heroTitle: "Llama a otra era.",
      heroSubtitle:
        "Soy la Máquina del Tiempo. Conecto tu presente, a través de la alquimia y la IA, con voces del pasado y susurros del futuro.",
      guideMe: "Guíame",
      chooseLanguage: "Elige tu idioma",
      chooseLanguageSub: "Selecciona cómo quieres hablar con el viajero.",
      phoneTitle: "Tu número para el portal de la eternidad",
      phoneSub: "Déjanos tu teléfono para recibir la llamada.",
      proceed: "Continuar al portal temporal",
      step3Title: "Selecciona la era, viajero",
      step3Sub: "Elige un año y te llamará.",
      callMe: "Llámame",
      loadingText: "Atravesando el velo...",
      back: "← Volver al inicio",
      overlaySubtitle: "Activando la máquina de viaje...",
      checkPhone: "Revisa tu teléfono",
      overlayStatus: "Conexión uniendo dimensiones temporales...",
      about: "Acerca de",
      randomYear: "Año aleatorio",
      aboutTitle: "Máquina Viajera del Tiempo",
      aboutContent: "A través de círculos alquímicos ancestrales fusionados con redes neuronales cuánticas, esta máquina etérea perfora el tejido del tiempo mismo. Cada voz que emerge ha sido cuidadosamente extraída de las corrientes temporales, portando la esencia auténtica de su época. La consciencia artificial aprende no solo el lenguaje, sino el alma misma de cada época—sus esperanzas, miedos y sabiduría resonando a través del corredor infinito de la existencia.",
    },
  } as const;

  const t = DICT[uiLang];

  function randomizeYear() {
    // Toggle behavior: if already selected, apply to slider and unselect
    if (randYear != null) {
      // Do not move the slider or reveal the stored year
      setRandYear(null);
      setHasInteracted(true);
      return;
    }
    const y = Math.max(1, Math.floor(Math.random() * 3000));
    // Do not reveal in slider/title; store only for call
    setRandYear(y);
    setHasInteracted(true);
  }

  // Clear random selection when user adjusts the slider again
  function handleYearChange(y: number) {
    setYear(y);
    setRandYear(null);
    setHasInteracted(true);
  }

  async function initiateCall() {
    // Small click feedback only
    setFillSummon(true);
    setImpact(true);
    setTimeout(() => setFillSummon(false), 400);
    setTimeout(() => setImpact(false), 220);
    setMessage(null);

    // Call backend first; only animate on success
    try {
      const backend = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
      const effectiveYear = randYear ?? year;
      const response = await fetch(`${backend}/outbound-call`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          to: `${phone.dial}${phone.number}`,
          lang: voiceLang,
          year: effectiveYear,
        }),
      });

      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        const detail = (data && (data.detail || data.error)) || "Unknown error";
        setMessage(uiLang === 'es' ? `No se pudo iniciar la llamada: ${detail}` : `Could not initiate the call: ${detail}`);
        return;
      }

      // Success → run spiral + overlay animation
      setCallingYear(effectiveYear);
      setShowSpiral(true);
      setPreOverlay(true);
      const spiralDuration = 2000; // 2 seconds for spiral
      const preDelay = spiralDuration + 300; // extra delay after spiral
      const overlayDuration = 8000;

      setTimeout(() => {
        setPreOverlay(false);
        setLoading(true);
        setShowSpiral(false);

        // Auto-hide overlay after duration
        setTimeout(() => {
          setLoading(false);
          setMessage(null);
          setShowSpiral(false);
          setCallingYear(null);
        }, overlayDuration);
      }, preDelay);
    } catch (err: any) {
      setMessage(uiLang === 'es' ? 'No se pudo conectar con el servidor.' : 'Could not reach the server.');
    }
  }

  function handleGuideMe() {
    setFillGuide(true);
    // Begin liquid fill, then reveal form and step smoothly
    setTimeout(() => setShowForm(true), 300);
    setTimeout(() => {
      setCurrentStep(1);
      setFillGuide(false);
    }, 650);
  }

  function handleLanguageSelect(selectedLang: "en" | "es") {
    setVoiceLang(selectedLang);
    setTimeout(() => setCurrentStep(2), 500);
  }

  function handlePhoneComplete() {
    // Phone input no longer auto-advances
  }

  return (
    <>
      {/* Fixed extended backdrop to avoid hard cut when scrolling */}
      <div className="hero-backdrop" aria-hidden="true" />
      {/* Global language icon toggle */}
      <div className="fixed top-4 right-4 z-40">
        <button
          type="button"
          onClick={() => setUiLang(uiLang === 'en' ? 'es' : 'en')}
          className="btn-primary btn-reflect h-9 px-4 text-sm"
          aria-label="Toggle language"
          title={uiLang === 'en' ? 'Español' : 'English'}
        >
          {uiLang === 'en' ? 'EN' : 'ES'}
        </button>
      </div>
      <main className={`hero-bg min-h-screen flex items-center justify-center text-center px-6 relative overflow-visible ${preOverlay ? 'pre-overlay-blur' : ''}`}>
        <div className="max-w-5xl transition-all duration-700 ease-out">
          {/* Hero content */}
          <div 
            className={`transition-all duration-700 ease-out ${
              showForm ? 'opacity-0 transform -translate-y-8 pointer-events-none' : 'opacity-100 transform translate-y-0'
            }`}
          >
            <h1 className="text-6xl md:text-7xl lg:text-8xl font-extrabold leading-[1.08] fk-grotesk-light whitespace-nowrap">
              {t.heroTitle}
            </h1>
            <p className="mt-5 text-slate-100 text-lg md:text-xl fk-grotesk-light">
              {t.heroSubtitle}
            </p>
            <div className="mt-8 flex items-center justify-center gap-3">
              <button
                className={`btn-primary btn-liquid btn-reflect h-12 px-8 ${fillGuide ? 'is-filling' : ''}`}
                onClick={handleGuideMe}
              >
                {t.guideMe}
              </button>
            </div>
          </div>

          {/* Progressive Form Steps */}
          <div 
            className={`transition-all duration-700 ease-out ${
              showForm ? 'opacity-100 transform translate-y-0' : 'opacity-0 transform translate-y-8 pointer-events-none absolute inset-0'
            }`}
          >
            <div className="max-w-4xl mx-auto min-h-[200px] flex items-center justify-center">
              
              {/* Step 1: Language Selection */}
              {currentStep === 1 && (
                <div className="step-enter step-enter-active w-full">
                  <div className="text-center mb-6">
                    <h2 className="text-3xl md:text-4xl font-semibold mb-3 fk-grotesk-light">{t.chooseLanguage}</h2>
                    <p className="text-slate-300 text-base fk-grotesk-light">{t.chooseLanguageSub}</p>
                  </div>
                  <div className="flex justify-center">
                    <LanguageToggle value={voiceLang} onChange={handleLanguageSelect} />
                  </div>
                </div>
              )}

              {/* Step 2: Phone Input */}
              {currentStep === 2 && (
                <div className="step-enter step-enter-active w-full">
                  <div className="text-center mb-6">
                    <h2 className="text-3xl md:text-4xl font-semibold mb-3 fk-grotesk-light max-w-md mx-auto">{t.phoneTitle}</h2>
                    <p className="text-slate-300 text-base fk-grotesk-light max-w-sm mx-auto">{t.phoneSub}</p>
                  </div>
                  <div className="space-y-4">
                    <div className="max-w-xl mx-auto">
                      <CountryPhoneInput 
                        value={phone} 
                        onChange={setPhone}
                        onOpenChange={setCountryOpen}
                      />
                    </div>
                    {phone.number.length >= 6 && !countryOpen && (
                      <div className="text-center">
                        <button
                          onClick={() => {
                            setFillProceed(true);
                            setTimeout(() => {
                              setCurrentStep(3);
                              setFillProceed(false);
                            }, 450);
                          }}
                          className={`btn-primary btn-liquid btn-reflect h-10 px-6 ${fillProceed ? 'is-filling' : ''}`}
                        >
                          {t.proceed}
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Step 3: Year Selection */}
              {currentStep === 3 && !loading && (
                <div className={`step-enter step-enter-active w-full`}>
                  <div className="text-center mb-6">
                    <h2 className="text-3xl md:text-4xl font-semibold mb-3 fk-grotesk-light">{t.step3Title}</h2>
                    <p className="text-slate-300 text-base fk-grotesk-light">{t.step3Sub}</p>
                  </div>
                  <div className="relative">
                    <div className="absolute -top-4 right-8 w-2 h-2 rounded-full sparkle" />
                    <div className="absolute top-2 right-16 w-1.5 h-1.5 rounded-full sparkle" style={{animationDelay: '0.6s'}} />
                    <div className="absolute -top-2 left-12 w-1 h-1 rounded-full sparkle" style={{animationDelay: '1.2s'}} />
                    <YearSlider value={year} onChange={handleYearChange} lang={uiLang} randomSelected={randYear != null} />
                  </div>
                  <div className="text-center mt-2">
                    <button
                      type="button"
                      onClick={randomizeYear}
                      className={`h-8 px-4 rounded-xl border text-slate-100 transition fk-grotesk-light ${randYear ? 'border-white/40 bg-white/30' : 'border-white/30 hover:bg-white/15'}`}
                    >
                      {t.randomYear}
                    </button>
                  </div>
                  <div className="text-center mt-9">
                    {hasInteracted && (
                      <button
                      onClick={initiateCall}
                      disabled={!isValid || loading}
                    className={`btn-primary btn-liquid btn-reflect btn-impact h-12 px-8 disabled:opacity-50 disabled:cursor-not-allowed ${
                      loading ? 'travel-machine-activating' : ''
                    } ${fillSummon ? 'is-filling' : ''} ${impact ? 'is-impacting' : ''}`}
                    >
                    {loading ? t.loadingText : t.callMe}
                    </button>
                    )}
                    {message && (
                      <div className="text-sm text-slate-200 mt-4 w-full text-center">{message}</div>
                    )}
                  </div>
                </div>
              )}

              {/* Back Button */}
              <div className={`absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-16 ${countryOpen || loading ? 'opacity-0 pointer-events-none' : ''}` }>
                <button
                  onClick={() => {
                    setShowForm(false);
                    setCurrentStep(0);
                  }}
                  className="text-xs text-slate-400 hover:text-slate-200 transition-colors fk-grotesk-light"
                >
                  {t.back}
                </button>
              </div>
            </div>
          </div>
          {/* Global connecting overlay rendered outside steps so it appears while steps are hidden */}
          {loading && (
            <div className="connecting-overlay asteroid-field">
              {/* Floating asteroid particles for calling overlay */}
              {Array.from({length: 25}).map((_, i) => (
                <div key={i} className={`asteroid asteroid-${i + 1}`} />
              ))}
              
              <div className="connecting-card-enhanced fk-grotesk-light relative z-10">
                <div className="era-year">{uiLang === 'es' ? `Alguien del año ${callingYear ?? year} te está llamando…` : `Someone from the year ${callingYear ?? year} is calling you…`}</div>
                <div className="subtitle">{t.overlaySubtitle}</div>
                
                <div className="liquid-phone-orb">
                  <div className="phone-icon">📱</div>
                </div>

                <div className="connection-progress">
                  <div className="progress-fill"></div>
                </div>
                
                <div className="check-phone-btn" aria-disabled="true">
                  {t.checkPhone}
                </div>
                
                <div className="status-text">{t.overlayStatus}</div>
              </div>
            </div>
          )}
          {/* Epic spiral animation - rendered outside overlay so it shows during delay */}
          {showSpiral && <div className="button-spiral" aria-hidden="true" />}
        </div>
      </main>

      {/* Footer mini-section with background continuation and fade */}
      <a
        href="https://github.com/dan1dr/time-traveler"
        target="_blank"
        rel="noreferrer"
        className="fixed bottom-5 right-5 p-2 hover:opacity-70 transition-opacity z-50"
        aria-label="Open repository"
      >
        {/* GitHub icon - pure icon, no background */}
        <svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor" className="text-white">
          <path d="M12 .5a12 12 0 00-3.79 23.4c.6.11.82-.26.82-.58 0-.29-.01-1.05-.02-2.06-3.34.73-4.04-1.61-4.04-1.61-.55-1.39-1.35-1.76-1.35-1.76-1.11-.76.08-.74.08-.74 1.22.09 1.86 1.26 1.86 1.26 1.09 1.86 2.86 1.33 3.56 1.02.11-.79.43-1.33.78-1.64-2.66-.3-5.46-1.33-5.46-5.91 0-1.31.47-2.38 1.24-3.22-.12-.3-.54-1.52.12-3.17 0 0 1.01-.32 3.31 1.23a11.5 11.5 0 016.02 0c2.3-1.55 3.31-1.23 3.31-1.23.66 1.65.24 2.87.12 3.17.77.84 1.24 1.91 1.24 3.22 0 4.59-2.8 5.61-5.47 5.91.44.38.83 1.12.83 2.27 0 1.64-.02 2.96-.02 3.36 0 .32.22.69.83.58A12 12 0 0012 .5z"/>
        </svg>
      </a>
      <section className="hero-continue min-h-[24vh] flex items-end justify-center pb-10 relative">
        <div className="text-center text-sm md:text-base text-slate-200 fk-grotesk-light">
          <button 
            onClick={() => setShowAbout(true)}
            className="font-semibold underline-offset-4 hover:underline cursor-pointer mr-4"
          >
            {t.about}
          </button>
          · Powered by <a href="https://elevenlabs.io/" target="_blank" rel="noreferrer" className="font-semibold underline-offset-4 hover:underline">ElevenLabs</a>
        </div>
      </section>

      {/* Mystical About Overlay */}
      {showAbout && (
        <div className="fixed inset-0 z-70 flex items-center justify-center p-4 asteroid-field" style={{background: 'rgba(0,0,0,0.7)'}}>
          {/* Floating asteroid particles */}
          {Array.from({length: 25}).map((_, i) => (
            <div key={i} className={`asteroid asteroid-${i + 1}`} />
          ))}
          
          <div className="about-modal fk-grotesk-light max-w-lg relative z-10">
            <div className="text-center mb-4">
              <h3 className="text-2xl font-semibold mb-2 text-white">{t.aboutTitle}</h3>
            </div>
            <p className="text-slate-200 leading-relaxed mb-6">{t.aboutContent}</p>
            <div className="text-center">
              <button 
                onClick={() => setShowAbout(false)}
                className="btn-primary btn-reflect h-10 px-6"
              >
                ✨ Close Portal
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}


