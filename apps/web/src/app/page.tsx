"use client";

import React, { useMemo, useRef, useState } from "react";
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
  const [errorType, setErrorType] = useState<'error' | 'warning' | 'info' | null>(null);
  const [errorSuggestion, setErrorSuggestion] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);
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
  const [callSid, setCallSid] = useState<string | null>(null);
  const [overlayInfo, setOverlayInfo] = useState<string | null>(null);
  const [finalMessage, setFinalMessage] = useState<string | null>(null);
  const [showFinalAnimation, setShowFinalAnimation] = useState(false);
  const [wasRandomYearClicked, setWasRandomYearClicked] = useState(false);
  
  // JWT Token management
  const [authToken, setAuthToken] = useState<string | null>(null);
  const [tokenExpiry, setTokenExpiry] = useState<number | null>(null);
  const pollIntervalRef = useRef<number | null>(null);
  const noAnswerTimeoutRef = useRef<number | null>(null);

  // JWT Helper Functions
  const getAuthHeaders = (): Record<string, string> => {
    if (!authToken) return {};
    return { Authorization: `Bearer ${authToken}` };
  };

  const isTokenExpired = () => {
    if (!tokenExpiry) return true;
    return Date.now() >= tokenExpiry;
  };

  const login = async () => {
    try {
      const backend = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
      const response = await fetch(`${backend}/auth/login`, { method: 'POST' });
      const data = await response.json();
      
      if (data.success) {
        const expiry = Date.now() + (data.expires_in * 1000);
        setAuthToken(data.token);
        setTokenExpiry(expiry);
        localStorage.setItem('time-traveler-token', data.token);
        localStorage.setItem('time-traveler-token-expiry', expiry.toString());
        return true;
      }
    } catch (error) {
      console.error('Login failed:', error);
    }
    return false;
  };

  const refreshToken = async () => {
    try {
      const backend = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
      const response = await fetch(`${backend}/auth/refresh`, {
        method: 'POST',
        headers: getAuthHeaders()
      });
      const data = await response.json();
      
      if (data.success) {
        const expiry = Date.now() + (data.expires_in * 1000);
        setAuthToken(data.token);
        setTokenExpiry(expiry);
        localStorage.setItem('time-traveler-token', data.token);
        localStorage.setItem('time-traveler-token-expiry', expiry.toString());
        return true;
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
    }
    return false;
  };

  // Smart API call with automatic retry on auth failure
  const makeAuthenticatedRequest = async (url: string, options: RequestInit = {}) => {
    const backend = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
    const fullUrl = url.startsWith('http') ? url : `${backend}${url}`;
    
    // First attempt with current token
    let response = await fetch(fullUrl, {
      ...options,
      headers: {
        ...options.headers,
        ...getAuthHeaders()
      }
    });
    
    // If 401, try to get a new token and retry once
    if (response.status === 401) {
      console.log('🔄 Token expired, getting new token...');
      const loginSuccess = await login();
      
      if (loginSuccess) {
        // Retry with new token
        response = await fetch(fullUrl, {
          ...options,
          headers: {
            ...options.headers,
            ...getAuthHeaders()
          }
        });
      }
    }
    
    return response;
  };

  // Initialize auth token on component mount
  React.useEffect(() => {
    const initializeAuth = async () => {
      const storedToken = localStorage.getItem('time-traveler-token');
      const storedExpiry = localStorage.getItem('time-traveler-token-expiry');
      
      if (storedToken && storedExpiry) {
        const expiry = parseInt(storedExpiry);
        if (Date.now() < expiry) {
          setAuthToken(storedToken);
          setTokenExpiry(expiry);
          return; // We have a valid token
        }
      }
      
      // No valid token, get a new one
      await login();
    };
    
    initializeAuth();
  }, []);

  const isValid = useMemo(() => {
    const fullPhone = `${phone.dial}${phone.number}`;
    const cleaned = fullPhone.replace(/[^\d+]/g, '');
    
    // Must start with + and have valid length
    if (!cleaned.startsWith('+') || cleaned.length < 12 || cleaned.length > 16) {
      return false;
    }
    
    // Check if it has valid country code (1-3 digits) and phone number (7-15 digits)
    const phoneMatch = cleaned.match(/^\+(\d{1,3})(\d{7,15})$/);
    return phoneMatch !== null;
  }, [phone.dial, phone.number]);

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
      callEnded: "Call ended.",
      callNotAnswered: "Call not answered.",
      returningToMachine: "Returning to the time machine...",
      about: "About",
      randomYear: "Random year",
      aboutTitle: "About this Time Machine",
      closePortal: "Close Portal",
      aboutContent: "This project combines artificial intelligence and a touch of imagination to recreate voices from different eras. It's not just about reproducing language, but providing context: how they thought, what they felt, and what concerns marked their time. Each response attempts to reflect the spirit of an era, with its doubts, certainties, and ways of understanding the world.\n\nSome ideas for your questions:\n\n• What was daily life like: what did they eat, how did they work, how did they pray or celebrate?\n• What great events do they remember from their time?\n• What advice or warnings would they give us today?\n• How do they imagine the future beyond their era?\n\nMore than a simple game, this experience opens a window to empathy and historical curiosity. It's a way to converse with the past and, at the same time, reflect on our present.\n\nThe voice interface is provided by <a href=\"https://elevenlabs.io/\" target=\"_blank\" rel=\"noreferrer\" class=\"font-semibold underline-offset-4 hover:underline\">ElevenLabs</a>, and mobile integration with <a href=\"https://www.twilio.com/\" target=\"_blank\" rel=\"noreferrer\" class=\"font-semibold underline-offset-4 hover:underline\">Twilio</a>. If you want to know more about how it's built, you can visit the repository <a href=\"https://github.com/dan1dr/time-traveler\" target=\"_blank\" rel=\"noreferrer\" class=\"font-semibold underline-offset-4 hover:underline\">here</a>.",
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
      callEnded: "Llamada finalizada.",
      callNotAnswered: "Llamada no contestada.",
      returningToMachine: "Regresando a la máquina del tiempo...",
      about: "Acerca de",
      randomYear: "Año aleatorio",
      aboutTitle: "Sobre esta Máquina del Tiempo",
      closePortal: "Cerrar Portal",
      aboutContent: "Este proyecto combina inteligencia artificial y un toque de imaginación para recrear voces de distintas épocas. No se trata solo de reproducir un lenguaje, sino de dar contexto: cómo pensaban, qué sentían y qué preocupaciones marcaban su tiempo. Cada respuesta intenta reflejar el espíritu de una era, con sus dudas, certezas y maneras de entender el mundo.\n\nAlgunas ideas para tus preguntas:\n\n• ¿Cómo era la vida cotidiana: qué comían, cómo trabajaban, cómo rezaban o celebraban?\n• ¿Qué grandes sucesos recuerdan de su tiempo?\n• ¿Qué consejos o advertencias nos darían hoy?\n• ¿Cómo se imaginan el futuro más allá de su época?\n\nMás que un simple juego, esta experiencia abre una ventana a la empatía y la curiosidad histórica. Es una forma de conversar con el pasado y, a la vez, reflexionar sobre nuestro presente.\n\nLa interfaz de voz está proporcionada por <a href=\"https://elevenlabs.io/\" target=\"_blank\" rel=\"noreferrer\" class=\"font-semibold underline-offset-4 hover:underline\">ElevenLabs</a>, y la integración móvil con <a href=\"https://www.twilio.com/\" target=\"_blank\" rel=\"noreferrer\" class=\"font-semibold underline-offset-4 hover:underline\">Twilio</a>. Si quieres conocer más sobre cómo está construido, puedes visitar el repositorio <a href=\"https://github.com/dan1dr/time-traveler\" target=\"_blank\" rel=\"noreferrer\" class=\"font-semibold underline-offset-4 hover:underline\">aquí</a>.",
    },
  } as const;

  const t = DICT[uiLang];

  // Error handling utilities
  const clearError = () => {
    setMessage(null);
    setErrorType(null);
    setErrorSuggestion(null);
  };

  const showError = (message: string, type: 'error' | 'warning' | 'info' = 'error', suggestion?: string) => {
    setMessage(message);
    setErrorType(type);
    setErrorSuggestion(suggestion || null);
  };

  const getErrorMessage = (error: any, uiLang: 'en' | 'es'): { message: string; type: 'error' | 'warning' | 'info'; suggestion?: string } => {
    // Network errors
    if (!error || error.name === 'TypeError' || error.message?.includes('fetch')) {
      return {
        message: uiLang === 'es' ? 'No se pudo conectar con el servidor' : 'Could not connect to server',
        type: 'error',
        suggestion: uiLang === 'es' ? 'Verifica tu conexión a internet e inténtalo de nuevo' : 'Check your internet connection and try again'
      };
    }

    // Parse error response
    const errorData = error.response?.data || error;
    const errorCode = errorData.error_code;
    const userMessage = errorData.error || errorData.message || error.message;
    const suggestion = errorData.suggestion;

    // Map specific error codes to user-friendly messages
    const errorMappings: Record<string, { message: string; type: 'error' | 'warning' | 'info'; suggestion: string }> = {
      'INVALID_PHONE_NUMBER': {
        message: uiLang === 'es' ? 'Formato de número de teléfono inválido' : 'Invalid phone number format',
        type: 'error',
        suggestion: uiLang === 'es' ? 'Asegúrate de incluir el código de país (ej: +1234567890)' : 'Make sure to include country code (e.g., +1234567890)'
      },
      'PHONE_NUMBER_NOT_REACHABLE': {
        message: uiLang === 'es' ? 'El número de teléfono no es alcanzable' : 'Phone number is not reachable',
        type: 'error',
        suggestion: uiLang === 'es' ? 'Verifica que el número sea correcto e inténtalo de nuevo' : 'Please verify the number is correct and try again'
      },
      'PHONE_NUMBER_BLOCKED': {
        message: uiLang === 'es' ? 'El número de teléfono está bloqueado' : 'Phone number is blocked',
        type: 'error',
        suggestion: uiLang === 'es' ? 'Intenta con un número diferente' : 'Please try a different number'
      },
      'VALIDATION_ERROR': {
        message: uiLang === 'es' ? 'Datos de entrada inválidos' : 'Invalid input data',
        type: 'error',
        suggestion: uiLang === 'es' ? 'Revisa los datos ingresados e inténtalo de nuevo' : 'Please check your input and try again'
      },
      'CONFIGURATION_ERROR': {
        message: uiLang === 'es' ? 'Servicio temporalmente no disponible' : 'Service temporarily unavailable',
        type: 'warning',
        suggestion: uiLang === 'es' ? 'Inténtalo de nuevo en unos minutos' : 'Please try again in a few minutes'
      },
      'AUTHENTICATION_FAILED': {
        message: uiLang === 'es' ? 'Error de autenticación del servicio' : 'Service authentication failed',
        type: 'error',
        suggestion: uiLang === 'es' ? 'Inténtalo de nuevo más tarde' : 'Please try again later'
      },
      'INTERNAL_ERROR': {
        message: uiLang === 'es' ? 'Error interno del servidor' : 'Internal server error',
        type: 'error',
        suggestion: uiLang === 'es' ? 'Inténtalo de nuevo en unos momentos' : 'Please try again in a few moments'
      }
    };

    if (errorCode && errorMappings[errorCode]) {
      return errorMappings[errorCode];
    }

    // Fallback to user message or generic error
    return {
      message: userMessage || (uiLang === 'es' ? 'Error desconocido' : 'Unknown error'),
      type: 'error',
      suggestion: suggestion || (uiLang === 'es' ? 'Inténtalo de nuevo' : 'Please try again')
    };
  };

  function randomizeYear() {
    // Toggle behavior: if already selected, apply to slider and unselect
    if (randYear != null) {
      // Do not move the slider or reveal the stored year
      setRandYear(null);
      setWasRandomYearClicked(false);
      setHasInteracted(true);
      return;
    }
    const y = Math.max(1, Math.floor(Math.random() * 3000));
    // Do not reveal in slider/title; store only for call
    setRandYear(y);
    setWasRandomYearClicked(true);
    setHasInteracted(true);
  }

  // Clear random selection when user adjusts the slider again
  function handleYearChange(y: number) {
    setYear(y);
    setRandYear(null);
    setWasRandomYearClicked(false);
    setHasInteracted(true);
  }

  async function initiateCall() {
    // Small click feedback only
    setFillSummon(true);
    setImpact(true);
    setTimeout(() => setFillSummon(false), 400);
    setTimeout(() => setImpact(false), 220);
    clearError();

    // Call backend first; only animate on success
    try {
      const backend = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
      const effectiveYear = randYear ?? year;
      const response = await makeAuthenticatedRequest("/outbound-call", {
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
        const errorInfo = getErrorMessage({ response: { data } }, uiLang);
        showError(errorInfo.message, errorInfo.type, errorInfo.suggestion);
        return;
      }

      const result = await response.json();
      if (!result.success) {
        const errorInfo = getErrorMessage(result, uiLang);
        showError(errorInfo.message, errorInfo.type, errorInfo.suggestion);
        return;
      }

      // Success → run spiral + overlay animation
      const newCallSid: string | undefined = result.callSid;
      if (newCallSid) {
        setCallSid(newCallSid);
      }
      setCallingYear(effectiveYear);
      setShowSpiral(true);
      setPreOverlay(true);
      setRetryCount(0); // Reset retry count on success
      const spiralDuration = 2000; // 2 seconds for spiral
      const preDelay = spiralDuration + 300; // extra delay after spiral

      setTimeout(() => {
        setPreOverlay(false);
        setLoading(true);
        setShowSpiral(false);
        setOverlayInfo(t.overlayStatus);
        if (newCallSid) {
          startCallStatusTracking(newCallSid);
        }
      }, preDelay);
    } catch (err: any) {
      const errorInfo = getErrorMessage(err, uiLang);
      showError(errorInfo.message, errorInfo.type, errorInfo.suggestion);
    }
  }

  function clearTimers() {
    if (pollIntervalRef.current != null) {
      clearInterval(pollIntervalRef.current);
      pollIntervalRef.current = null;
    }
    if (noAnswerTimeoutRef.current != null) {
      clearTimeout(noAnswerTimeoutRef.current);
      noAnswerTimeoutRef.current = null;
    }
  }

  function resetUIToHome() {
    setLoading(false);
    setShowSpiral(false);
    setCallingYear(null);
    setCallSid(null);
    setOverlayInfo(null);
    setFinalMessage(null);
    setShowFinalAnimation(false);
    setWasRandomYearClicked(false);
    setShowForm(false);
    setCurrentStep(0);
  }

  function showFinalMessageAndReset(message: string) {
    setFinalMessage(message);
    setShowFinalAnimation(true);
    setLoading(false); // Hide the main overlay
    
    // Show final message for 3 seconds, then reset to home
    setTimeout(() => {
      resetUIToHome();
    }, 3000);
  }

  async function startCallStatusTracking(callSidToTrack: string) {
    const backend = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
    let answered = false;

    // 20s no-answer timeout
    noAnswerTimeoutRef.current = window.setTimeout(async () => {
      if (!answered) {
        try {
          await makeAuthenticatedRequest(`/end-call/${callSidToTrack}?reason=no-answer`, { 
            method: 'POST'
          });
        } catch {}
        clearTimers();
        showFinalMessageAndReset(t.callNotAnswered);
      }
    }, 20000);

    // Poll status every 1.5s
    pollIntervalRef.current = window.setInterval(async () => {
      try {
        const res = await makeAuthenticatedRequest(`/call-status/${callSidToTrack}`);
        // If backend already cleaned up after we observed 'answered', treat 404 as ended
        if (res.status === 404 && answered) {
          clearTimers();
          showFinalMessageAndReset(t.callEnded);
          return;
        }
        if (!res.ok) return;
        const data = await res.json();
        const status = data.status as string;
        if (status === 'answered') {
          if (!answered) {
            answered = true;
            if (noAnswerTimeoutRef.current != null) {
              clearTimeout(noAnswerTimeoutRef.current);
              noAnswerTimeoutRef.current = null;
            }
            setOverlayInfo(t.overlayStatus);
          }
        }
        if (status === 'ended' || status === 'failed') {
          clearTimers();
          showFinalMessageAndReset(status === 'failed' ? t.callNotAnswered : t.callEnded);
        }
      } catch {
        // ignore transient errors
      }
    }, 1500);
  }

  // Retry function for failed calls
  const retryCall = () => {
    if (retryCount < 3) {
      setRetryCount(prev => prev + 1);
      initiateCall();
    }
  };

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
      {/* Global language icon toggle */}
      <div className="fixed top-3 right-3 sm:top-4 sm:right-4 z-40">
        <button
          type="button"
          onClick={() => setUiLang(uiLang === 'en' ? 'es' : 'en')}
          className="btn-primary btn-reflect h-8 sm:h-9 px-3 sm:px-4 text-xs sm:text-sm"
          aria-label="Toggle language"
          title={uiLang === 'en' ? 'Español' : 'English'}
        >
          {uiLang === 'en' ? 'EN' : 'ES'}
        </button>
      </div>
      <main className={`hero-bg min-h-screen flex items-center justify-center text-center px-4 sm:px-6 py-8 relative overflow-visible ${preOverlay ? 'pre-overlay-blur' : ''}`}>
        <div className="max-w-5xl w-full transition-all duration-700 ease-out">
          {/* Hero content */}
          <div 
            className={`transition-all duration-700 ease-out ${
              showForm ? 'opacity-0 transform -translate-y-8 pointer-events-none' : 'opacity-100 transform translate-y-0'
            }`}
          >
            <h1 className="text-4xl sm:text-5xl md:text-7xl lg:text-8xl font-extrabold leading-[1.08] fk-grotesk-light">
              {t.heroTitle}
            </h1>
            <p className="mt-5 text-slate-100 text-base sm:text-lg md:text-xl fk-grotesk-light max-w-2xl mx-auto">
              {t.heroSubtitle}
            </p>
            <div className="mt-8 flex items-center justify-center gap-3">
              <button
                className={`btn-primary btn-liquid btn-reflect h-12 px-6 sm:px-8 text-sm sm:text-base ${fillGuide ? 'is-filling' : ''}`}
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
                  <div className="text-center mb-6 px-4">
                    <h2 className="text-2xl sm:text-3xl md:text-4xl font-semibold mb-3 fk-grotesk-light">{t.chooseLanguage}</h2>
                    <p className="text-slate-300 text-sm sm:text-base fk-grotesk-light">{t.chooseLanguageSub}</p>
                  </div>
                  <div className="flex justify-center">
                    <LanguageToggle value={voiceLang} onChange={handleLanguageSelect} />
                  </div>
                </div>
              )}

              {/* Step 2: Phone Input */}
              {currentStep === 2 && (
                <div className="step-enter step-enter-active w-full">
                  <div className="text-center mb-6 px-4">
                    <h2 className="text-2xl sm:text-3xl md:text-4xl font-semibold mb-3 fk-grotesk-light max-w-md mx-auto">{t.phoneTitle}</h2>
                    <p className="text-slate-300 text-sm sm:text-base fk-grotesk-light max-w-sm mx-auto">{t.phoneSub}</p>
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
                          disabled={!isValid}
                          className={`btn-primary btn-liquid btn-reflect h-10 px-4 sm:px-6 text-sm sm:text-base disabled:opacity-50 disabled:cursor-not-allowed ${fillProceed ? 'is-filling' : ''}`}
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
                  <div className="text-center mb-6 px-4">
                    <h2 className="text-2xl sm:text-3xl md:text-4xl font-semibold mb-3 fk-grotesk-light">{t.step3Title}</h2>
                    <p className="text-slate-300 text-sm sm:text-base fk-grotesk-light">{t.step3Sub}</p>
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
                      className={`h-8 px-3 sm:px-4 text-xs sm:text-sm rounded-xl border text-slate-100 transition fk-grotesk-light ${randYear ? 'border-white/40 bg-white/30' : 'border-white/30 hover:bg-white/15'}`}
                    >
                      {t.randomYear}
                    </button>
                  </div>
                  <div className="text-center mt-9 px-4">
                    {hasInteracted && (
                      <button
                      onClick={initiateCall}
                      disabled={!isValid || loading}
                    className={`btn-primary btn-liquid btn-reflect btn-impact h-12 px-6 sm:px-8 text-sm sm:text-base disabled:opacity-50 disabled:cursor-not-allowed ${
                      loading ? 'travel-machine-activating' : ''
                    } ${fillSummon ? 'is-filling' : ''} ${impact ? 'is-impacting' : ''}`}
                    >
                    {loading ? t.loadingText : t.callMe}
                    </button>
                    )}
                    {message && (
                      <div className="mt-4 w-full text-center">
                        <div className={`text-sm mb-2 ${
                          errorType === 'error' ? 'text-red-300' : 
                          errorType === 'warning' ? 'text-yellow-300' : 
                          'text-blue-300'
                        }`}>
                          {message}
                        </div>
                        {errorSuggestion && (
                          <div className="text-xs text-slate-400 mb-3">
                            {errorSuggestion}
                          </div>
                        )}
                        {errorType === 'error' && retryCount < 3 && (
                          <button
                            onClick={retryCall}
                            className="text-xs px-4 py-2 rounded-lg border border-slate-500 hover:border-slate-400 hover:bg-slate-800/50 transition-colors"
                          >
                            {uiLang === 'es' ? 'Reintentar' : 'Retry'} ({retryCount}/3)
                          </button>
                        )}
                      </div>
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
              
              <div className="connecting-card-enhanced fk-grotesk-light relative z-10 mx-4">
                <div className="era-year text-lg sm:text-xl md:text-2xl">{uiLang === 'es' ? `Alguien del año ${wasRandomYearClicked ? '?' : (callingYear ?? year)} te está llamando…` : `Someone from the year ${wasRandomYearClicked ? '?' : (callingYear ?? year)} is calling you…`}</div>
                <div className="subtitle text-sm sm:text-base">{t.overlaySubtitle}</div>
                
                <div className="liquid-phone-orb">
                  <div className="phone-icon">📱</div>
                </div>

                <div className="connection-progress">
                  <div className="progress-fill"></div>
                </div>
                
                <div className="check-phone-btn" aria-disabled="true">
                  {t.checkPhone}
                </div>
                
                <div className="status-text">{overlayInfo || t.overlayStatus}</div>
              </div>
            </div>
          )}
          {/* Epic spiral animation - rendered outside overlay so it shows during delay */}
          {showSpiral && <div className="button-spiral" aria-hidden="true" />}
        </div>
      </main>

      {/* Final message animation */}
      {showFinalAnimation && (
        <div className="fixed inset-0 z-70 flex items-center justify-center p-4 asteroid-field" style={{background: 'rgba(0,0,0,0.8)'}}>
          {/* Floating asteroid particles */}
          {Array.from({length: 25}).map((_, i) => (
            <div key={i} className={`asteroid asteroid-${i + 1}`} />
          ))}
          
          <div className="final-message-modal fk-grotesk-light max-w-md relative z-10 mx-4">
            <div className="text-center">
              <div className="text-3xl sm:text-4xl mb-4">📞</div>
              <h3 className="text-xl sm:text-2xl font-semibold mb-2 text-white">{finalMessage}</h3>
              <div className="text-slate-300 text-xs sm:text-sm">{t.returningToMachine}</div>
            </div>
          </div>
        </div>
      )}

      {/* Footer mini-section with background continuation and fade */}
      <a
        href="https://github.com/dan1dr/time-traveler"
        target="_blank"
        rel="noreferrer"
        className="fixed bottom-3 right-3 sm:bottom-5 sm:right-5 p-2 hover:opacity-70 transition-opacity z-50"
        aria-label="Open repository"
      >
        {/* GitHub icon - pure icon, no background */}
        <svg viewBox="0 0 24 24" width="28" height="28" fill="currentColor" className="text-white sm:w-8 sm:h-8">
          <path d="M12 .5a12 12 0 00-3.79 23.4c.6.11.82-.26.82-.58 0-.29-.01-1.05-.02-2.06-3.34.73-4.04-1.61-4.04-1.61-.55-1.39-1.35-1.76-1.35-1.76-1.11-.76.08-.74.08-.74 1.22.09 1.86 1.26 1.86 1.26 1.09 1.86 2.86 1.33 3.56 1.02.11-.79.43-1.33.78-1.64-2.66-.3-5.46-1.33-5.46-5.91 0-1.31.47-2.38 1.24-3.22-.12-.3-.54-1.52.12-3.17 0 0 1.01-.32 3.31 1.23a11.5 11.5 0 016.02 0c2.3-1.55 3.31-1.23 3.31-1.23.66 1.65.24 2.87.12 3.17.77.84 1.24 1.91 1.24 3.22 0 4.59-2.8 5.61-5.47 5.91.44.38.83 1.12.83 2.27 0 1.64-.02 2.96-.02 3.36 0 .32.22.69.83.58A12 12 0 0012 .5z"/>
        </svg>
      </a>
      <section className="hero-continue min-h-[24vh] flex items-end justify-center pb-6 sm:pb-10 relative">
        <div className="text-center text-xs sm:text-sm md:text-base text-slate-200 fk-grotesk-light flex flex-col sm:flex-row items-center justify-center gap-1 sm:gap-2 px-4">
          <button 
            onClick={() => setShowAbout(true)}
            className="font-semibold underline-offset-4 hover:underline cursor-pointer"
          >
            {t.about}
          </button>
          <span className="text-slate-300 font-bold hidden sm:inline">•</span>
          <span className="text-center">Powered by <a href="https://elevenlabs.io/" target="_blank" rel="noreferrer" className="font-semibold underline-offset-4 hover:underline">ElevenLabs</a></span>
        </div>
      </section>

      {/* Mystical About Overlay */}
      {showAbout && (
        <div className="fixed inset-0 z-70 flex items-center justify-center p-4 asteroid-field" style={{background: 'rgba(0,0,0,0.7)'}}>
          {/* Floating asteroid particles */}
          {Array.from({length: 25}).map((_, i) => (
            <div key={i} className={`asteroid asteroid-${i + 1}`} />
          ))}
          
          <div className="about-modal fk-grotesk-light max-w-lg relative z-10 mx-4">
            <div className="text-center mb-4">
              <h3 className="text-xl sm:text-2xl font-semibold mb-2 text-white">{t.aboutTitle}</h3>
            </div>
            <div 
              className="text-slate-200 text-sm sm:text-base leading-relaxed mb-6 whitespace-pre-line max-h-[60vh] overflow-y-auto crystal-scroll" 
              dangerouslySetInnerHTML={{ __html: t.aboutContent }}
            />
            <div className="text-center">
              <button 
                onClick={() => setShowAbout(false)}
                className="btn-primary btn-reflect h-10 px-4 sm:px-6 text-sm sm:text-base"
              >
                ✨ {t.closePortal}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}



