"use client";

import { useMemo, useState } from "react";

export function YearSlider({
  value,
  onChange,
  lang = 'en',
  randomSelected = false,
}: {
  value: number;
  onChange: (val: number) => void;
  lang?: 'en' | 'es';
  randomSelected?: boolean;
}) {
  const era = useMemo(() => getEraForYear(value, lang), [value, lang]);
  const [isSliding, setIsSliding] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(parseInt(e.target.value, 10));
  };

  return (
    <div className="relative">
      {/* Centered Year Display with Zoom Animation */}
      <div className="text-center mb-6 year-header" style={{minHeight:'8.5rem'}}>
        <div className={`text-2xl font-semibold transition-transform duration-300 fk-grotesk-light will-change-transform`}
          style={{
            transform: isSliding ? 'scale(1.06)' : 'scale(1)',
            color: randomSelected ? 'rgba(200,200,200,0.9)' : (value >= 2026 ? 'rgba(72,209,204,0.9)' : 'rgba(255,255,255,0.9)')
          }}>
          {randomSelected ? (lang === 'es' ? 'Desconocido' : 'Unknown') : (value >= 2026 ? (lang === 'es' ? 'Futuro' : 'Future') : era.label)}
        </div>
        
        {/* Year with zoom effect */}
        <div className={`text-4xl font-bold transition-transform duration-200 fk-grotesk-light`}
          style={{transform: isSliding ? 'scale(1.12)' : 'scale(1)'}}>
          {randomSelected ? '?' : value}
        </div>
      </div>

      {/* Crystal Slider Container - 2x Wider */}
      <div className="relative px-2 w-full max-w-6xl mx-auto">
        {/* Elegant Axis Markers */}
        <div className="absolute inset-x-2 -bottom-6 flex justify-between text-xs axis-labels pointer-events-none">
          <span className="transform -translate-x-4">-1500</span>
          <span className="transform -translate-x-2">0</span>
          <span className="transform -translate-x-3">1500</span>
          <span className="transform translate-x-2">3000</span>
        </div>
        
        {/* Axis ticks */}
        <div className="absolute inset-x-2 top-4 flex justify-between pointer-events-none">
          {[-1500, 0, 1500, 3000].map((tick) => (
            <div key={tick} className="w-px h-2 bg-slate-600"></div>
          ))}
        </div>

        {/* Crystal Slider Track */}
        <div className="relative mt-8">
          <div className="absolute inset-x-0 top-1/2 transform -translate-y-1/2 h-3 rounded-full"
               style={{
                 background: value >= 2026 
                   ? 'linear-gradient(90deg, rgba(72,209,204,0.25), rgba(108,99,255,0.2), rgba(255,255,255,0.15))'
                   : 'linear-gradient(90deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05))',
                 border: `1px solid ${value >= 2026 ? 'rgba(72,209,204,0.3)' : 'rgba(255,255,255,0.2)'}`,
                 backdropFilter: 'blur(10px)',
                 boxShadow: value >= 2026 ? '0 0 20px rgba(72,209,204,0.3)' : ''
               }}
          />
          
          {/* Custom Range Input */}
          <input
            type="range"
            min={-1500}
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
      <div className="mt-10 text-center text-sm max-w-xs mx-auto fk-grotesk-light" style={{
        minHeight: '2.6rem',
        display: '-webkit-box',
        WebkitLineClamp: 2 as any,
        WebkitBoxOrient: 'vertical' as any,
        overflow: 'hidden',
        color: randomSelected ? 'transparent' : (value >= 2026 ? 'rgba(72,209,204,0.9)' : 'rgba(255,255,255,0.7)')
      }}>
        {randomSelected ? '' : (value >= 2026 ? (lang === 'es' ? 'Descubre el futuro' : 'Discover the future') : era.description)}
      </div>
    </div>
  );
}

function getEraForYear(year: number, lang: 'en' | 'es') {
  // Function to get specific historic event for a year
  const getHistoricEvent = (year: number, lang: 'en' | 'es') => {
    const events = lang === 'es' ? {
      [-1450]: 'Palacio de Cnosos en Creta',
      [-1200]: 'Invasión de los Pueblos del Mar',
      [-1000]: 'Fundación de reinos israelitas',
      [-776]: 'Primeros Juegos Olímpicos',
      [-753]: 'Fundación de Roma',
      [-586]: 'Destrucción del Primer Templo',
      [-508]: 'Democracia ateniense',
      [-490]: 'Batalla de Maratón',
      [-336]: 'Alejandro Magno',
      [-221]: 'Unificación de China',
      [-49]: 'César cruza el Rubicón',
      [-44]: 'Asesinato de César',
      [-31]: 'Batalla de Actium',
      [1]: 'Nacimiento de Cristo',
      [79]: 'Erupción del Vesubio',
      [313]: 'Edicto de Milán',
      [476]: 'Caída del Imperio Romano',
      [622]: 'Hégira de Mahoma',
      [800]: 'Carlomagno coronado emperador',
      [1066]: 'Batalla de Hastings',
      [1096]: 'Primera Cruzada',
      [1215]: 'Carta Magna firmada',
      [1347]: 'Peste Negra devasta Europa',
      [1453]: 'Caída de Constantinopla',
      [1455]: 'Biblia de Gutenberg',
      [1492]: 'Colón llega a América',
      [1517]: 'Reforma Protestante',
      [1543]: 'Copérnico publica sobre heliocentrismo',
      [1588]: 'Derrota de la Armada Invencible',
      [1620]: 'Mayflower llega a América',
      [1687]: 'Newton publica Principia',
      [1776]: 'Independencia de Estados Unidos',
      [1789]: 'Revolución Francesa',
      [1804]: 'Napoleón se corona emperador',
      [1825]: 'Primera locomotora de vapor',
      [1859]: 'Darwin publica El Origen de las Especies',
      [1865]: 'Abolición de la esclavitud',
      [1876]: 'Invención del teléfono',
      [1885]: 'Primer automóvil',
      [1903]: 'Primer vuelo de los Wright',
      [1914]: 'Primera Guerra Mundial',
      [1917]: 'Revolución Rusa',
      [1929]: 'Crack de Wall Street',
      [1939]: 'Segunda Guerra Mundial',
      [1945]: 'Bomba atómica en Hiroshima',
      [1957]: 'Sputnik lanzado',
      [1961]: 'Gagarin en el espacio',
      [1969]: 'Primer alunizaje',
      [1973]: 'Crisis del petróleo',
      [1989]: 'Caída del Muro de Berlín',
      [1991]: 'World Wide Web',
      [2001]: 'Atentados del 11-S',
      [2008]: 'Crisis financiera global',
      [2020]: 'Pandemia COVID-19',
      [2030]: 'IA supera inteligencia humana',
      [2040]: 'Ciudades flotantes',
      [2050]: 'Primera base en Marte',
      [2075]: 'Viajes interplanetarios comerciales',
      [2100]: 'Fusión nuclear comercial',
      [2150]: 'Colonización de Europa (luna)',
      [2200]: 'Primer viaje interestelar',
      [2300]: 'Terraformación de Venus',
      [2500]: 'Conciencia digital colectiva',
      [2750]: 'Viajes interdimensionales'
    } : {
      [-1450]: 'Palace of Knossos in Crete',
      [-1200]: 'Sea Peoples invasions',
      [-1000]: 'Foundation of Israelite kingdoms',
      [-776]: 'First Olympic Games',
      [-753]: 'Foundation of Rome',
      [-586]: 'Destruction of First Temple',
      [-508]: 'Athenian democracy',
      [-490]: 'Battle of Marathon',
      [-336]: 'Alexander the Great',
      [-221]: 'Unification of China',
      [-49]: 'Caesar crosses Rubicon',
      [-44]: 'Assassination of Caesar',
      [-31]: 'Battle of Actium',
      [1]: 'Birth of Christ',
      [79]: 'Vesuvius erupts',
      [313]: 'Edict of Milan',
      [476]: 'Fall of the Roman Empire',
      [622]: 'Muhammad\'s Hijra',
      [800]: 'Charlemagne crowned emperor',
      [1066]: 'Battle of Hastings',
      [1096]: 'First Crusade',
      [1215]: 'Magna Carta signed',
      [1347]: 'Black Death devastates Europe',
      [1453]: 'Fall of Constantinople',
      [1455]: 'Gutenberg Bible printed',
      [1492]: 'Columbus reaches America',
      [1517]: 'Protestant Reformation',
      [1543]: 'Copernicus publishes heliocentric theory',
      [1588]: 'Spanish Armada defeated',
      [1620]: 'Mayflower arrives in America',
      [1687]: 'Newton publishes Principia',
      [1776]: 'American Independence',
      [1789]: 'French Revolution',
      [1804]: 'Napoleon crowns himself emperor',
      [1825]: 'First steam locomotive',
      [1859]: 'Darwin publishes Origin of Species',
      [1865]: 'Slavery abolished',
      [1876]: 'Telephone invented',
      [1885]: 'First automobile',
      [1903]: 'Wright brothers first flight',
      [1914]: 'World War I begins',
      [1917]: 'Russian Revolution',
      [1929]: 'Wall Street Crash',
      [1939]: 'World War II begins',
      [1945]: 'Atomic bomb on Hiroshima',
      [1957]: 'Sputnik launched',
      [1961]: 'Gagarin in space',
      [1969]: 'First moon landing',
      [1973]: 'Oil crisis',
      [1989]: 'Berlin Wall falls',
      [1991]: 'World Wide Web',
      [2001]: '9/11 attacks',
      [2008]: 'Global financial crisis',
      [2020]: 'COVID-19 pandemic',
      [2030]: 'AI surpasses human intelligence',
      [2040]: 'Floating cities',
      [2050]: 'First Mars base',
      [2075]: 'Commercial interplanetary travel',
      [2100]: 'Commercial nuclear fusion',
      [2150]: 'Europa colonization',
      [2200]: 'First interstellar voyage',
      [2300]: 'Venus terraforming',
      [2500]: 'Collective digital consciousness',
      [2750]: 'Interdimensional travel'
    };
    
    // Find closest historic event
    const eventYears = Object.keys(events).map(Number).sort((a, b) => a - b);
    let closestYear = eventYears[0];
    for (const eventYear of eventYears) {
      if (Math.abs(eventYear - year) < Math.abs(closestYear - year)) {
        closestYear = eventYear;
      }
    }
    return events[closestYear as keyof typeof events];
  };

  const EN = [
    { until: -800, label: 'Late Bronze–Early Iron Age', description: getHistoricEvent(year, 'en') },
    { until: 0, label: 'Classical Antiquity', description: getHistoricEvent(year, 'en') },
    { until: 500, label: 'Roman Empire / Late Antiquity', description: getHistoricEvent(year, 'en') },
    { until: 1000, label: 'Early Middle Ages', description: getHistoricEvent(year, 'en') },
    { until: 1300, label: 'High Middle Ages', description: getHistoricEvent(year, 'en') },
    { until: 1400, label: 'Late Middle Ages', description: getHistoricEvent(year, 'en') },
    { until: 1600, label: 'Renaissance', description: getHistoricEvent(year, 'en') },
    { until: 1750, label: 'Baroque Era', description: getHistoricEvent(year, 'en') },
    { until: 1900, label: 'Industrial Revolution', description: getHistoricEvent(year, 'en') },
    { until: 1945, label: 'Modernism & World Wars', description: getHistoricEvent(year, 'en') },
    { until: 1991, label: 'Cold War', description: getHistoricEvent(year, 'en') },
    { until: 2008, label: 'Globalization & Early Internet', description: getHistoricEvent(year, 'en') },
    { until: 2030, label: 'Mobile • Social • Cloud', description: getHistoricEvent(year, 'en') },
    { until: 2050, label: 'AI Renaissance', description: getHistoricEvent(year, 'en') },
    { until: 2200, label: 'Interplanetary Era', description: getHistoricEvent(year, 'en') },
    { until: 2500, label: 'Transcendent Age', description: getHistoricEvent(year, 'en') },
    { until: 3000, label: 'Far Future', description: getHistoricEvent(year, 'en') },
  ];
  const ES = [
    { until: -800, label: 'Bronce tardío–Hierro temprano', description: getHistoricEvent(year, 'es') },
    { until: 0, label: 'Antigüedad clásica', description: getHistoricEvent(year, 'es') },
    { until: 500, label: 'Imperio Romano / Antigüedad tardía', description: getHistoricEvent(year, 'es') },
    { until: 1000, label: 'Alta Edad Media', description: getHistoricEvent(year, 'es') },
    { until: 1300, label: 'Plena Edad Media', description: getHistoricEvent(year, 'es') },
    { until: 1400, label: 'Baja Edad Media', description: getHistoricEvent(year, 'es') },
    { until: 1600, label: 'Renacimiento', description: getHistoricEvent(year, 'es') },
    { until: 1750, label: 'Era barroca', description: getHistoricEvent(year, 'es') },
    { until: 1900, label: 'Revolución Industrial', description: getHistoricEvent(year, 'es') },
    { until: 1945, label: 'Modernismo y guerras mundiales', description: getHistoricEvent(year, 'es') },
    { until: 1991, label: 'Guerra Fría', description: getHistoricEvent(year, 'es') },
    { until: 2008, label: 'Globalización e Internet temprano', description: getHistoricEvent(year, 'es') },
    { until: 2030, label: 'Móvil • Social • Nube', description: getHistoricEvent(year, 'es') },
    { until: 2050, label: 'Renacimiento IA', description: getHistoricEvent(year, 'es') },
    { until: 2200, label: 'Era interplanetaria', description: getHistoricEvent(year, 'es') },
    { until: 2500, label: 'Era trascendente', description: getHistoricEvent(year, 'es') },
    { until: 3000, label: 'Futuro lejano', description: getHistoricEvent(year, 'es') },
  ];
  const table = lang === 'es' ? ES : EN;
  const match = table.find(e => year <= e.until) || table[table.length - 1];
  return { label: match.label, description: match.description };
}


