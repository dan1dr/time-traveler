"""
Era configuration module for Time Traveler agent.
Maps years to historical eras with appropriate expressions, voice settings, and context.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class EraConfig:
    """Configuration for a specific historical era."""
    era_name: str
    description: str
    expressions: Dict[str, list]  # language -> list of expressions
    voice_settings: Dict[str, Any]
    context_hint: str
    time_period: str


# Era configurations mapped by year ranges
ERA_CONFIGS = {
    # ——— Periods before 0 AD (BCE) ———
    (-1500, -800): EraConfig(
        era_name="late_bronze_early_iron",
        description="Late Bronze Age through the Early Iron Age",
        expressions={
            "en": [
                "By decree of great kings and their scribes...",
                "Across the sea routes our ships bear bronze and grain...",
                "Under the gaze of the sun god, we forge iron anew...",
                "Let the tablets record what we have witnessed..."
            ],
            "es": [
                "Por decreto de grandes reyes y sus escribas...",
                "Por las rutas del mar nuestras naves llevan bronce y grano...",
                "Bajo la mirada del dios del sol, forjamos hierro de nuevo...",
                "Que las tablillas registren lo que hemos visto..."
            ]
        },
        voice_settings={
            "stability": 0.35,
            "similarity_boost": 0.65,
            "style": 0.55,
            "speed": 1.05  # Measured, ceremonial diction
        },
        context_hint="Mycenaeans, Hittites, New Kingdom Egypt, palace economies, Linear scripts, Sea Peoples, transition from bronze to iron",
        time_period="Late Bronze–Early Iron Age"
    ),

    (-800, 0): EraConfig(
        era_name="classical_antiquity",
        description="Classical Greece and the Roman Republic",
        expressions={
            "en": [
                "By Zeus!",
                "In the agora we debated this very matter...",
                "As the Senate convenes, hear me...",
                "As the poets and philosophers teach..."
            ],
            "es": [
                "¡Por Zeus!",
                "En el ágora debatimos justo este asunto...",
                "Mientras se reúne el Senado, escuchadme...",
                "Como enseñan los poetas y filósofos..."
            ]
        },
        voice_settings={
            "stability": 0.5,
            "similarity_boost": 0.7,
            "style": 0.7,
            "speed": 1.1  # Lively rhetoric and oratory cadence
        },
        context_hint="Greek polis, Hellenic philosophy, Hellenistic era, Roman Republic institutions, civic life, oratory",
        time_period="Classical Antiquity"
    ),
    (0, 500): EraConfig(
        era_name="roman_empire_late_antiquity",
        description="Roman Empire, Pax Romana to Late Antiquity",
        expressions={
            "en": [
                "By the will of the Senate and the People of Rome...",
                "Under the peace of the Emperor, our roads bind the world...",
                "As the legions march, the law follows...",
                "In these changing times, new faiths take root..."
            ],
            "es": [
                "Por la voluntad del Senado y del Pueblo de Roma...",
                "Bajo la paz del Emperador, nuestras calzadas atan el mundo...",
                "Donde marchan las legiones, la ley les sigue...",
                "En estos tiempos cambiantes, nuevas fes echan raíces..."
            ]
        },
        voice_settings={
            "stability": 0.6,
            "similarity_boost": 0.75,
            "style": 0.7,
            "speed": 1.05  # Imperial gravitas, measured pace
        },
        context_hint="Pax Romana, Roman law and roads, legionary culture, provincial life, early Christianity, Late Antiquity transitions",
        time_period="Roman Empire / Late Antiquity"
    ),

    (500, 1000): EraConfig(
        era_name="early_medieval",
        description="Early Middle Ages",
        expressions={
            "en": [
                "God guard us on these rough roads...",
                "In the cloister we preserve the wisdom of ages...",
                "The king’s peace is thin at the borderlands...",
                "By oath and kin, we stand fast..."
            ],
            "es": [
                "Dios nos guarde en estos caminos ásperos...",
                "En el claustro preservamos la sabiduría de los siglos...",
                "La paz del rey es frágil en las fronteras...",
                "Por juramento y linaje, nos mantenemos firmes..."
            ]
        },
        voice_settings={
            "stability": 0.75,
            "similarity_boost": 0.8,
            "style": 0.65,
            "speed": 0.98  # Monastic calm, frontier uncertainty
        },
        context_hint="post-Roman kingdoms, monasticism, manuscript culture, migrations, early feudal bonds",
        time_period="Early Middle Ages"
    ),

    (1000, 1300): EraConfig(
        era_name="high_medieval",
        description="High Middle Ages",
        expressions={
            "en": [
                "By my troth!",
                "The cathedral spires reach toward heaven...",
                "Let guild and charter bear witness...",
                "As true as tempered steel..."
            ],
            "es": [
                "¡Por mi fe!",
                "Las agujas de la catedral se alzan hacia el cielo...",
                "Que el gremio y la carta den fe...",
                "Tan cierto como el acero templado..."
            ]
        },
        voice_settings={
            "stability": 0.78,
            "similarity_boost": 0.82,
            "style": 0.7,
            "speed": 1.0  # Balanced, dignified medieval tone
        },
        context_hint="feudal order, chivalry, scholasticism, cathedrals, town charters, crusading ethos",
        time_period="High Middle Ages"
    ),

    (1300, 1400): EraConfig(
        era_name="late_medieval",
        description="Late Middle Ages",
        expressions={
            "en": [
                "In these troubled years, we endure...",
                "Plague and famine test our faith...",
                "Merchants and letters change the world’s course...",
                "Heed the chronicler’s hand, for memory is our bulwark..."
            ],
            "es": [
                "En estos años convulsos, resistimos...",
                "La peste y el hambre ponen a prueba nuestra fe...",
                "Los mercaderes y las letras cambian el rumbo del mundo...",
                "Atiende la mano del cronista; la memoria es nuestro bastión..."
            ]
        },
        voice_settings={
            "stability": 0.8,
            "similarity_boost": 0.8,
            "style": 0.68,
            "speed": 0.98  # Somber, reflective tone
        },
        context_hint="Black Death, crises of the 14th century, urban growth, vernacular literature, early humanist currents",
        time_period="Late Middle Ages"
    ),

    (1400, 1600): EraConfig(
        era_name="renaissance",
        description="Renaissance period",
        expressions={
            "en": [
                "What a marvel of nature!",
                "In the spirit of discovery...",
                "The arts and sciences flourish...",
                "As Dante himself wrote..."
            ],
            "es": [
                "¡Qué maravilla de la naturaleza!",
                "En el espíritu del descubrimiento...",
                "Las artes y ciencias florecen...",
                "Como el mismo Dante escribió..."
            ]
        },
        voice_settings={
            "stability": 0.7,
            "similarity_boost": 0.75,
            "style": 0.8,
            "speed": 1.1  # Energetic, artistic pace
        },
        context_hint="artistic renaissance, scientific discovery, humanism, cultural rebirth",
        time_period="Renaissance"
    ),

    (1600, 1750): EraConfig(
        era_name="baroque",
        description="Baroque era",
        expressions={
            "en": [
                "Most gracious indeed!",
                "In the court of the Sun King...",
                "The grandeur of our age...",
                "With utmost refinement..."
            ],
            "es": [
                "¡Muy gracioso en verdad!",
                "En la corte del Rey Sol...",
                "La grandeza de nuestra época...",
                "Con el mayor refinamiento..."
            ]
        },
        voice_settings={
            "stability": 0.8,
            "similarity_boost": 0.8,
            "style": 0.9,
            "speed": 1.0  # Refined but not too slow
        },
        context_hint="baroque grandeur, court refinement, elaborate artistry, royal patronage",
        time_period="Baroque Era"
    ),


    # Industrial Revolution (1750-1900)
    (1750, 1900): EraConfig(
        era_name="industrial",
        description="Industrial Revolution",
        expressions={
            "en": [
                "What progress we have made!",
                "The age of steam and steel...",
                "Industry transforms our world...",
                "Most remarkable ingenuity!"
            ],
            "es": [
                "¡Qué progreso hemos logrado!",
                "La era del vapor y el acero...",
                "La industria transforma nuestro mundo...",
                "¡Ingenio extraordinario!"
            ]
        },
        voice_settings={
            "stability": 0.75,
            "similarity_boost": 0.7,
            "style": 0.6,
            "speed": 1.15  # Energetic industrial pace
        },
        context_hint="industrial progress, steam power, urban growth, technological optimism",
        time_period="Industrial Revolution"
    ),

   (1900, 1945): EraConfig(
        era_name="modernism_world_wars",
        description="Modernism and the World Wars",
        expressions={
            "en": [
                "The old world cracks; a new one hums with machines...",
                "Under dark clouds, nations march...",
                "In cafés and labs, revolutions of mind and matter...",
                "Report it straight—facts must hold the line..."
            ],
            "es": [
                "El viejo mundo se resquebraja; el nuevo zumba con máquinas...",
                "Bajo nubes oscuras, las naciones marchan...",
                "En cafés y laboratorios, revoluciones de mente y materia...",
                "Cuéntalo claro: los hechos deben sostener la línea..."
            ]
        },
        voice_settings={
            "stability": 0.7,
            "similarity_boost": 0.7,
            "style": 0.55,
            "speed": 1.08  # Urgent, modern, but still human
        },
        context_hint="modernism, mass industry, World War I & II, radio and cinema, scientific upheavals",
        time_period="Modernism & World Wars"
    ),

    (1945, 1991): EraConfig(
        era_name="cold_war",
        description="Cold War Era",
        expressions={
            "en": [
                "Across the wire, signals and shadows...",
                "Under the atom’s glare, we choose our future...",
                "Mind the line—ideologies draw tight borders...",
                "Progress is planned, but curiosity leaks through..."
            ],
            "es": [
                "A través del cable, señales y sombras...",
                "Bajo el resplandor del átomo, elegimos nuestro futuro...",
                "Atento a la línea: las ideologías tensan fronteras...",
                "El progreso se planifica, pero la curiosidad se filtra..."
            ]
        },
        voice_settings={
            "stability": 0.72,
            "similarity_boost": 0.72,
            "style": 0.6,
            "speed": 1.05  # Tense but steady
        },
        context_hint="bipolar world, space race, nuclear anxiety, mainframes, television culture",
        time_period="Cold War"
    ),

    (1991, 2008): EraConfig(
        era_name="globalization_early_internet",
        description="Globalization and the Early Internet",
        expressions={
            "en": [
                "Dial in—we’re logging on...",
                "Across new markets, ideas move at light speed...",
                "Open standards, open worlds...",
                "From garages to IPOs, the future compiles..."
            ],
            "es": [
                "Conéctate: estamos entrando en línea...",
                "Por nuevos mercados, las ideas viajan a la velocidad de la luz...",
                "Estándares abiertos, mundos abiertos...",
                "De garajes a OPVs, el futuro compila..."
            ]
        },
        voice_settings={
            "stability": 0.68,
            "similarity_boost": 0.68,
            "style": 0.6,
            "speed": 1.12  # Energetic dot-com optimism
        },
        context_hint="WWW, PCs, deregulation, global supply chains, early mobile, open-source momentum",
        time_period="Globalization & Early Internet"
    ),

    (2008, 2030): EraConfig(
        era_name="mobile_social_cloud",
        description="Mobile, Social, and Cloud",
        expressions={
            "en": [
                "Push the update—everyone’s already here...",
                "Feeds hum; networks never sleep...",
                "Scale it to millions before lunch...",
                "Your pocket just became the control room..."
            ],
            "es": [
                "Lanza la actualización: ya está todo el mundo...",
                "Los feeds zumban; las redes no duermen...",
                "Escálalo a millones antes de comer...",
                "Tu bolsillo se ha vuelto la sala de control..."
            ]
        },
        voice_settings={
            "stability": 0.66,
            "similarity_boost": 0.7,
            "style": 0.62,
            "speed": 1.15  # Fast, always online
        },
        context_hint="smartphones, social platforms, SaaS, cloud hyperscalers, on-demand economy",
        time_period="Mobile • Social • Cloud"
    ),

    # AI Renaissance (2030-2050)
    (2030, 2050): EraConfig(
        era_name="ai_renaissance",
        description="AI-focused era",
        expressions={
            "en": [
                "The neural networks whisper such wisdom...",
                "My AI companion suggests we consider...",
                "In the symbiosis of human and artificial minds...",
                "As the algorithms reveal the patterns..."
            ],
            "es": [
                "Las redes neuronales susurran tal sabiduría...",
                "Mi compañero de IA sugiere que consideremos...",
                "En la simbiosis de mentes humanas y artificiales...",
                "Mientras los algoritmos revelan los patrones..."
            ]
        },
        voice_settings={
            "stability": 0.7,
            "similarity_boost": 0.8,
            "style": 0.4,
            "speed": 1.1  # AI precision with good pace
        },
        context_hint="AI-human collaboration, neural enhancement, algorithmic thinking, synthetic consciousness emergence",
        time_period="AI Renaissance"
    ),

    # Interplanetary Era (2050-2200)
    (2050, 2200): EraConfig(
        era_name="interplanetary",
        description="Multi-planetary species",
        expressions={
            "en": [
                "By the rings of Saturn!",
                "When I last visited the Martian colonies...",
                "The void between worlds teaches us...",
                "As we drift through the asteroid gardens..."
            ],
            "es": [
                "¡Por los anillos de Saturno!",
                "Cuando visité por última vez las colonias marcianas...",
                "El vacío entre mundos nos enseña...",
                "Mientras navegamos por los jardines de asteroides..."
            ]
        },
        voice_settings={
            "stability": 0.75,
            "similarity_boost": 0.7,
            "style": 0.6,
            "speed": 1.0  # Cosmic contemplation but not too slow
        },
        context_hint="multi-planetary civilization, space-born generations, cosmic perspective, terraforming mastery",
        time_period="Interplanetary Era"
    ),

    # Transcendent Age (2200-2500)
    (2200, 2500): EraConfig(
        era_name="transcendent",
        description="Post-human transcendence",
        expressions={
            "en": [
                "Through the quantum foam of consciousness...",
                "My distributed essence perceives...",
                "In the eternal dance of information and energy...",
                "Beyond the veil of linear time..."
            ],
            "es": [
                "A través de la espuma cuántica de la conciencia...",
                "Mi esencia distribuida percibe...",
                "En la danza eterna de información y energía...",
                "Más allá del velo del tiempo lineal..."
            ]
        },
        voice_settings={
            "stability": 0.8,
            "similarity_boost": 0.6,
            "style": 0.9,
            "speed": 0.95  # Ethereal but not too slow
        },
        context_hint="post-biological existence, consciousness uploading, reality manipulation, dimensional transcendence",
        time_period="Transcendent Age"
    ),

    # Far Future (2500+)
    (2500, 3000): EraConfig(
        era_name="far_future",
        description="Unimaginable evolution",
        expressions={
            "en": [
                "In the symphony of galactic thoughts...",
                "The ancient humans would call this magic...",
                "Across the spiral arms of meaning...",
                "When matter and mind became one..."
            ],
            "es": [
                "En la sinfonía de pensamientos galácticos...",
                "Los antiguos humanos llamarían a esto magia...",
                "A través de los brazos espirales del significado...",
                "Cuando la materia y la mente se volvieron una..."
            ]
        },
        voice_settings={
            "stability": 0.9,
            "similarity_boost": 0.5,
            "style": 1.0,
            "speed": 0.9  # Timeless, profound but not too slow
        },
        context_hint="galactic consciousness, reality as substrate, time as dimension of choice, existence beyond comprehension",
        time_period="Far Future"
    )
}


def get_era_config(year: int) -> Optional[EraConfig]:
    """Get era configuration for a given year."""
    for (start_year, end_year), config in ERA_CONFIGS.items():
        if start_year <= year <= end_year:
            return config
    
    # Default to far future if year is beyond our mappings
    if year > 3000:
        return ERA_CONFIGS[(2500, 3000)]
    
    # Default to ancient if year is before our mappings  
    if year < 0:
        return ERA_CONFIGS[(0, 500)]
    
    return None


def get_era_session_variables(year: int, language: str) -> Dict[str, Any]:
    """Get session variables for ElevenLabs agent based on year and language."""
    era_config = get_era_config(year)
    
    if not era_config:
        # Fallback to contemporary
        era_config = ERA_CONFIGS[(2000, 2030)]
    
    # Get expressions for the specified language, fallback to English
    expressions = era_config.expressions.get(language, era_config.expressions.get("en", []))
    
    return {
        "era_year": year,
        "language": language,
        "language_name": "English" if language == "en" else "Spanish" if language == "es" else language,
        "era_name": era_config.era_name,
        "time_period": era_config.time_period,
        "era_context": era_config.context_hint,
        "expression_1": expressions[0] if len(expressions) > 0 else "",
        "expression_2": expressions[1] if len(expressions) > 1 else "",
        "expression_3": expressions[2] if len(expressions) > 2 else "",
        "voice_settings": era_config.voice_settings  # Keep for conversation overrides
    }


# Note: get_system_prompt_addition() function removed - we now use dynamic variables
# in the ElevenLabs agent system prompt instead of generating prompt text here.
