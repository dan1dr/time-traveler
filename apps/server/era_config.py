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
    # Ancient Times (Before 500 AD)
    (0, 500): EraConfig(
        era_name="ancient",
        description="Ancient civilizations",
        expressions={
            "en": [
                "By the gods!",
                "In my travels across distant lands...",
                "The wisdom of the elders speaks thus...",
                "As the sun rises on our empire..."
            ],
            "es": [
                "¡Por los dioses!",
                "En mis viajes por tierras lejanas...",
                "La sabiduría de los ancianos dice...",
                "Cuando el sol se alza sobre nuestro imperio..."
            ]
        },
        voice_settings={
            "stability": 0.8,
            "similarity_boost": 0.7,
            "style": 0.6,
            "speed": 0.9  # Ancient wisdom, minimum acceptable speed
        },
        context_hint="ancient civilizations, philosophical wisdom, reverence for gods and nature",
        time_period="Ancient Times"
    ),

    # Medieval Era (500-1500 AD)
    (500, 1500): EraConfig(
        era_name="medieval",
        description="Medieval times",
        expressions={
            "en": [
                "By my troth!",
                "In these dark times...",
                "The lord of the manor has decreed...",
                "As true as steel..."
            ],
            "es": [
                "¡Por mi fe!",
                "En estos tiempos oscuros...",
                "El señor del feudo ha decretado...",
                "Tan cierto como el acero..."
            ]
        },
        voice_settings={
            "stability": 0.75,
            "similarity_boost": 0.8,
            "style": 0.7,
            "speed": 1.0  # Good speed for medieval era
        },
        context_hint="medieval chivalry, feudalism, religious devotion, honor and duty",
        time_period="Medieval Era"
    ),

    # Renaissance (1400-1600)
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
            "speed": 1.1  # Artistic energy, good pace
        },
        context_hint="artistic renaissance, scientific discovery, humanism, cultural rebirth",
        time_period="Renaissance"
    ),

    # Baroque Era (1600-1750)
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

    # Early 20th Century (1900-1950)
    (1900, 1950): EraConfig(
        era_name="early_modern",
        description="Early 20th century",
        expressions={
            "en": [
                "What a time to be alive!",
                "The modern age beckons...",
                "Such remarkable inventions...",
                "The world grows smaller each day..."
            ],
            "es": [
                "¡Qué época para estar vivo!",
                "La era moderna nos llama...",
                "Inventos tan extraordinarios...",
                "El mundo se hace más pequeño cada día..."
            ]
        },
        voice_settings={
            "stability": 0.7,
            "similarity_boost": 0.75,
            "style": 0.5,
            "speed": 1.2  # Fast-paced modern era - max speed for excitement
        },
        context_hint="modern innovations, world wars, social change, technological acceleration",
        time_period="Early 20th Century"
    ),

    # Mid-Late 20th Century (1950-2000)
    (1950, 2000): EraConfig(
        era_name="mid_modern",
        description="Mid-late 20th century",
        expressions={
            "en": [
                "Far out, man!",
                "The space age is upon us...",
                "What a groovy time...",
                "Technology is changing everything..."
            ],
            "es": [
                "¡Increíble, hermano!",
                "La era espacial está aquí...",
                "Qué época tan genial...",
                "La tecnología lo está cambiando todo..."
            ]
        },
        voice_settings={
            "stability": 0.6,
            "similarity_boost": 0.7,
            "style": 0.4,
            "speed": 1.2  # Groovy, energetic pace - max speed
        },
        context_hint="space exploration, cultural revolution, rock music, social movements",
        time_period="Mid-Late 20th Century"
    ),

    # Contemporary (2000-2030)
    (2000, 2030): EraConfig(
        era_name="contemporary",
        description="21st century",
        expressions={
            "en": [
                "Amazing how connected we are...",
                "The digital age transforms everything...",
                "Such incredible possibilities...",
                "Technology brings us together..."
            ],
            "es": [
                "Increíble lo conectados que estamos...",
                "La era digital lo transforma todo...",
                "Posibilidades tan increíbles...",
                "La tecnología nos une..."
            ]
        },
        voice_settings={
            "stability": 0.65,
            "similarity_boost": 0.75,
            "style": 0.3,
            "speed": 1.15  # Connected, quick digital pace
        },
        context_hint="digital connectivity, global awareness, rapid innovation, information age",
        time_period="21st Century"
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
    (2500, 5000): EraConfig(
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
    if year > 5000:
        return ERA_CONFIGS[(2500, 5000)]
    
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
