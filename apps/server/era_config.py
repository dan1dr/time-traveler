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
            "similarity_boost": 0.7,
            "speed": 1.05  # Measured, ceremonial diction
        },
        context_hint="""Large, centralized palace economies dominate the eastern Mediterranean. Mycenae, Hattusa, Ugarit, and New Kingdom Egypt coordinate agriculture, craft production, and long-distance trade in copper, tin, grain, textiles, and luxury goods. Writing is specialized and administrative (Linear B, cuneiform, hieratic), ships are oared, and diplomacy moves by gift and oath among "Great Kings."

Around the 12th–11th centuries BCE, this world fragments. Causes overlap—earthquakes, droughts, internal revolts, disrupted trade routes, and maritime/land incursions often grouped under the term "Sea Peoples." Archives burn, palaces fall, and many regions experience population shifts and simpler political forms. Iron tools and weapons spread gradually, not because iron is superior at first, but because its ores are more widely available than tin, allowing local production where bronze networks have broken.

In the aftermath, smaller chiefdoms and early village polities take root. Oral tradition flourishes where scribal offices vanish; new ethnic labels coalesce; old gods persist under new patronage. The "international" Late Bronze Age dissolves into regional stories, setting conditions for the Archaic Greek polis, the Neo-Assyrian resurgence in the Near East, and new trade circuits that will knit the next era together.""",
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
            "speed": 1.1  # Lively rhetoric and oratory cadence
        },
        context_hint="""The Mediterranean reorganizes around independent Greek poleis and, later, the Roman Republic's expansion. In the Greek world (8th–4th c. BCE), city-states blend citizen politics, hoplite warfare, maritime trade, and intense competition in art, drama, and philosophy. Colonization spreads Greek settlements and culture from the Black Sea to Iberia. Thinkers from the Presocratics to Plato and Aristotle formalize inquiry; historians like Herodotus and Thucydides craft critical narratives of human affairs.

Alexander's conquests (late 4th c. BCE) fuse Greek elites with Near Eastern and Egyptian traditions, birthing the Hellenistic kingdoms. Science and scholarship flourish at centers like Alexandria: mathematics, astronomy, medicine, and geography take cumulative steps that will echo for millennia.

Meanwhile, Rome evolves from city-republic to Mediterranean hegemon. Institutions—Senate, assemblies, magistracies—shape civic identity; Latin law and road-building tie provinces together. Expansion generates wealth and strain: social conflicts, slave labor economies, and elite rivalries culminate in civil wars and the end of the Republic. By the 1st c. BCE–1st c. CE, the framework for imperial rule is set, blending Roman pragmatism with a cosmopolitan Hellenistic cultural sphere.""",
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
            "stability": 0.5,
            "similarity_boost": 0.75,
            "speed": 1.05  # Imperial gravitas, measured pace
        },
        context_hint="""Empire means infrastructure: stone roads, milestones, bridges, harbors, and administrative routines that regularize taxation, law, and movement. The Pax Romana (1st–2nd c. CE) enables large-scale trade in grain, wine, oil, ceramics, and luxuries across the Mediterranean and beyond. Cities are civic stages—baths, theaters, amphitheaters—where local elites perform loyalty through benefaction, and law courts arbitrate disputes with written procedures.

From the 3rd century, crises mount: frontier pressures, internal usurpers, fiscal debasement, and plague test imperial cohesion. Reforms centralize power, split administration, and fortify borders. Christianity, once a persecuted minority, gains legal status (4th c. CE) and imperial patronage; new religious identities and debates reshape communities, art, and moral life.

Late Antiquity is not mere collapse; it's transition. Regional economies persist, cities adapt, and new powers arise (e.g., Goths, Vandals; in the east, a resilient Roman/Byzantine polity). Latin and Greek cultural worlds diverge administratively even as trade and diplomacy continue. The old imperial world narrows in the west and transforms in the east, preparing the ground for medieval polities and faiths.""",
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
            "stability": 0.5,
            "similarity_boost": 0.8,
            "speed": 0.98  # Monastic calm, frontier uncertainty
        },
        context_hint="""Western Europe fragments into successor kingdoms with mixed Roman, Christian, and "barbarian" legal traditions. Authority is personal and local: ties of lordship, kin, and oath often matter more than distant claims. Town life shrinks in many areas, though not everywhere; rural estates and fortified strongpoints become anchors of security and production.

Monasticism spreads a discipline of prayer, work, and learning. Scriptoria preserve Christian texts and, selectively, classical literature; missionaries carry Latin Christianity north and east. In the Mediterranean and Near East, the rise of Islam (7th c.) creates a dynamic new imperial and commercial sphere, connecting Arabia, the Levant, North Africa, and Iberia under Arabic language, law, and scholarship.

Trade never stops; it reroutes. River systems and fairs link producers and consumers; silver inflows and slave routes reshape exchanges. Cultural horizons remain regional but not isolated: Irish monks reach the continent, Andalusi cities synthesize traditions, and the Byzantine Empire maintains urban life, taxation, and learned bureaucratic rule in the east.""",
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
            "stability": 0.6,
            "similarity_boost": 0.82,
            "speed": 1.0  # Balanced, dignified medieval tone
        },
        context_hint="""Population and production grow with better plows, crop rotations, and expanded acreage. Mills harness water and wind; market towns and guilds standardize craft training and reputation. Royal courts and communes write charters that clarify rights, obligations, and taxes. Cathedrals rise as engineering feats and religious statements, financed by long campaigns of donations and skilled labor.

Universities emerge (Bologna, Paris, Oxford), professionalizing law, theology, and medicine. Scholastic method structures debate; Latin binds the learned across borders, while vernacular literature blooms—epic, romance, lyric. Crusading energies direct violence outward; at home, legal pluralism (royal, canon, urban) grows more intricate.

The age has order and friction: feudal ties and cash economies overlap; saints' cults and reasoned disputation coexist. Europe's map is a mosaic of lordships, bishoprics, communes, and kingdoms learning to tax, legislate, and record at scale.""",
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
            "stability": 0.6,
            "similarity_boost": 0.8,
            "speed": 0.98  # Somber, reflective tone
        },
        context_hint="""The 14th century brings hard shocks: repeated plague waves reduce populations drastically, shifting wages, rents, and social expectations. Warfare (e.g., Hundred Years' War), fiscal crisis, and peasant/urban revolts stress governments and elites. Famine in some decades compounds instability; religious movements—reformist or heterodox—test ecclesiastical authority.

Yet institutions adapt. Tax systems and representative assemblies mature in several realms; accounting and credit techniques deepen; Italian and northern city networks intensify long-distance commerce. Literature in the vernacular reaches new heights (Dante, Chaucer), painting explores perspective, and humanist study of classical texts germinates.

By the 15th century, consolidation trends gather: stronger monarchies, new military technologies (gunpowder tactics), and patronage circuits that will fuel the Renaissance. Crisis and creativity advance together, preparing the cultural and political turn to come.""",
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
            "speed": 1.0  # Energetic, artistic pace
        },
        context_hint="""Humanism reframes learning: recover the best of classical antiquity, read sources critically, write with clarity and style. Printing presses scale distribution of texts; workshops mix art and engineering—perspective, anatomy, optics—making images persuasive tools for faith, status, and inquiry. Patronage courts (Medici, papal Rome, princely courts in Iberia and the Empire) concentrate talent and money.

Exploration and conquest open Atlantic systems: Iberian voyages connect Europe, Africa, and the Americas, moving people, crops, pathogens, gold, and ideas. Religious unity fractures in the early 16th century; reform and counter-reform rewire authority, ritual, and education. Science inches toward systematic observation and mathematical description, with alchemy and natural magic sharing benches with emerging empiricism.

The "rebirth" is uneven and plural—a set of regional renaissances that together shift Europe's center of gravity toward textual criticism, statecraft by bureaucracy, and image-driven persuasion in church and court.""",
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
            "stability": 0.6,
            "similarity_boost": 0.8,
            "speed": 1.0  # Refined but not too slow
        },
        context_hint="""States and churches speak in spectacle. Architecture, music, and painting aim for awe—grand façades, deep chiaroscuro, polyphonic masses. Absolutist monarchies centralize revenue and armies; elsewhere, federations and republics balance estates and merchants. Confessional lines shape alliances and censorship, yet scientific societies (Royal Society, Académie) institutionalize experiment and shared critique.

Global trade intensifies through chartered companies and coerced labor systems. Atlantic slavery scales into a brutal economic engine linking Europe, Africa, and the Americas. Silver from the New World fuels monetization; Asian luxuries reshape taste and domestic interiors. Navigation, cartography, and instruments advance; telescopes and microscopes extend the knowable.

Behind ornament stands administration: cadasters, codes, and fiscal reforms. The baroque eye choreographs attention; the modern state learns to count, drill, and plan.""",
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
            "stability": 0.5,
            "similarity_boost": 0.7,
            "speed": 1.1  # Energetic industrial pace
        },
        context_hint="""Coal, steam, and mechanization transform production and daily time. Textile mills lead, then iron, steel, rail, and steamships integrate regions into national and imperial markets. Urbanization accelerates; factory discipline and clock time organize labor. Mass newspapers, cheap print, and later telegraphy create simultaneity—people experience faraway events almost together.

Capital pools in banks and joint-stock companies; crises and booms ripple globally. Reformers and labor movements fight for sanitation, schooling, suffrage, and safer work. Science links to industry: chemistry, electricity, and engineering research cycle into patents and products. Empire becomes an economic as well as political system, moving raw materials out and finished goods in.

By the late 19th century, networks (rails, cables) compress distance, while social questions—inequality, urban poverty, public health—define new politics. The modern consumer economy and the modern social state are both seeded here.""",
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
            "stability": 0.4,
            "similarity_boost": 0.7,
            "speed": 1.08  # Urgent, modern, but still human
        },
        context_hint="""Early 20th-century culture breaks forms to match a world of machines, mass media, and crowded cities. Modernist art and literature experiment with viewpoint, fragmentation, and speed; cinema teaches audiences to read cuts. Science rewrites fundamentals: relativity and quantum theory upend space, time, and matter; psychology probes the unconscious.

Two world wars mobilize entire societies. Industry becomes armory; propaganda saturates; genocide and aerial bombing redefine horror. Borders are redrawn, empires falter, and postwar orders attempt collective security and economic management. Radio, then early television, carry leaders and narratives directly into homes.

Between and after the wars, welfare states, planned economies, and developmental visions compete. The big picture is volatility harnessed by bureaucracy and technology—an age certain of technique and uncertain of ends.""",
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
            "stability": 0.30,
            "similarity_boost": 0.72,
            "speed": 1.05  # Tense but steady
        },
        context_hint="""A bipolar order crystallizes around the U.S. and USSR, each with allies, ideologies, and nuclear arsenals. Deterrence doctrine makes survival a calculation; crises in Berlin, Cuba, and elsewhere test red lines. Proxy wars and decolonization reshape Asia, Africa, and the Middle East, as new nations navigate development, nonalignment, or clientage.

Domestically, both blocs mobilize science and education; space programs stage prestige and practical gains (satellites, microelectronics). Mass consumer culture expands in the West; censorship and planned production frame daily life in the East. Intelligence services, covert operations, and propaganda are routine instruments of statecraft.

Détente ebbs and flows; by the late 1980s, economic strains and reform movements crack the Soviet model. The era closes with political realignments, market transitions, and unresolved regional conflicts seeded over decades of superpower competition.""",
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
            "stability": 0.35,
            "similarity_boost": 0.68,
            "speed": 1.1  # Energetic dot-com optimism
        },
        context_hint="""The 1990s–2000s see market liberalization, global supply chains, and a unipolar moment. PCs and the World Wide Web democratize publishing and discovery; search engines and open-source communities organize vast, voluntary collaboration. Mobile phones spread first as voice/text devices, then as proto-computers.

Culture globalizes through cable, file-sharing, and early streaming. Finance innovates (and overreaches), culminating in crises that propagate quickly through integrated markets. Institutions experiment with trade regimes and regional unions, even as backlash politics gestate.

The net's ethos is "open by default," but business models coalesce around portals, ads, and platforms. The seeds of social media and cloud services are planted, ready to scale in the next phase.""",
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
            "stability": 0.35,
            "similarity_boost": 0.7,
            "speed": 1.05  # Fast, always online
        },
        context_hint="""Smartphones turn connectivity into a constant. App ecosystems, social feeds, and push notifications create real-time publics; cloud computing moves storage and computation out of local devices, letting startups serve millions quickly. Recommendation systems shape attention; creators and influencers professionalize.

Work and consumption reorganize around platforms: ride-hailing, food delivery, e-commerce logistics, and streaming. Data becomes strategic—collected, analyzed, and monetized. Privacy norms, antitrust debates, and content moderation emerge as central policy questions.

Teams ship continuously; devops and SaaS standardize deployment; AI/ML enter mainstream products via perception and ranking. The upside is scale and convenience; the downside is addiction loops, polarization dynamics, and fragile dependencies on a few hyperscale providers.""",
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
            "stability": 0.5,
            "similarity_boost": 0.8,
            "speed": 1.1  # AI precision with good pace
        },
        context_hint="""General-purpose models move from narrow perception to flexible language-reasoning systems, then tool-using agents. Organizations pair humans with AI copilots across code, documents, design, and operations. The frontier shifts from single answers to orchestrated workflows: retrieval, planning, calling APIs, and verifying outputs.

Compute, data, and safety become policy issues as well as engineering concerns. Enterprises build "AI safety rails" (guardrails, evals, provenance) while regulators debate transparency and accountability. Education and creativity change shape: individuals prototype software, research, and media at the pace once reserved for teams.

Productivity rises unevenly—firms and workers who learn to delegate to machines move faster. The strategic picture: AI as a new "general-purpose technology," diffusing across sectors, redrawing value chains, and forcing new norms for trust and attribution.""",
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
            "stability": 0.5,
            "similarity_boost": 0.7,
            "speed": 1.1  # Cosmic contemplation but not too slow
        },
        context_hint="""Launch costs fall and in-situ resource utilization makes off-Earth living less exotic. The first sustainable footholds—cislunar infrastructure, Mars surface habitats—blend government programs with commercial logistics. Life support, radiation shielding, and closed-loop systems are the core constraints; autonomy and robotics fill labor gaps.

Economically, space becomes a layered stack: communications and Earth observation; manufacturing and research in microgravity niches; extraction/refining where it makes sense; tourism for the wealthy, then broader. Jurisdictions and property norms evolve from treaties to practical governance—safety, liability, and resource rights are negotiated in real time.

Culturally, a spacefaring identity emerges: frontier risk, long-delay communications, and communities optimized for reliability over comfort. The frontier mindset returns, but with spreadsheets, lawyers, and biosafety officers.""",
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
            "stability": 0.4,
            "similarity_boost": 0.6,
            "speed": 1.0  # Ethereal but not too slow
        },
        context_hint="""Biology and computation blur. Individuals extend cognition with neural interfaces; groups coordinate through shared knowledge layers; some people choose radical life extension or substrate-diverse existence. Identity gains persistence beyond a single body but must still solve continuity, consent, and rights.

Economies pivot toward intangible production: models, simulations, designs that instantiate on demand. Governance experiments with personhood standards (for uploaded, synthetic, or collective minds), while ethical frameworks catch up to experiences outside evolutionary precedent.

Day-to-day life is less about scarcity of matter and more about the curation of attention, memory, and experience. "Place" becomes layered—physical, virtual, and cognitive spaces interleave, and travel means switching contexts as much as coordinates.""",
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
            "stability": 0.,
            "similarity_boost": 0.5,
            "speed": 1.0  # Timeless, profound but not too slow
        },
        context_hint="""Civilization operates at astronomical scales. Energy capture approaches fractions of stellar output; habitats multiply from planetary surfaces to engineered megastructures. Long-duration planning spans millennia; archives and institutions aim to survive stellar and geological change.

Intelligence exists across forms—biological, synthetic, hybrid—and across timescales, from microsecond decisions to centuries-long projects. Culture is an ecology of memories and styles, recombining across light-hours. Ethics centers on coexistence among diverse minds and the management of colossal externalities.

For individuals, the universe feels both domestic and sublime. Journeys might traverse not just distance but frames of computation or perception. The grand challenge is steering abundance without losing purpose or pluralism.""",
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
    if year < -1500:
        return ERA_CONFIGS[(-1500, -800)]
    
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
