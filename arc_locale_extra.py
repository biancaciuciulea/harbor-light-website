# -*- coding: utf-8 -*-
"""Extra ARC UI strings merged into ARC_I18N (nav/footer/script/chapters).

Keep romance ARC free of AI marketing. RO is intentionally absent.
"""

from __future__ import annotations

# Localized Harbor Light titles for ARC chrome (Amazon KDP titles where live).
ARC_BOOK_TITLES: dict[int, dict[str, tuple[str, str]]] = {
    1: {
        "en": ("Bound by Blood and Harbor Light", "Bound by Blood"),
        "de": ("Gebunden durch Blut und Hafenlicht", "Gebunden durch Blut"),
        "fr": ("Liés par le sang et la lumière du port", "Liés par le sang"),
        "es": ("Unidos por la sangre y la luz del puerto", "Unidos por la sangre"),
        "it": ("Legati dal sangue e dalla luce del porto", "Legati dal sangue"),
    },
    2: {
        "en": ("Bound by Soft Marks and Harbor Light", "Bound by Soft Marks"),
        "de": ("Gebunden durch sanfte Male und Hafenlicht", "Gebunden durch sanfte Male"),
        "fr": ("Liés par les marques douces et la lumière du port", "Liés par les marques douces"),
        "es": ("Unidos por marcas suaves y la luz del puerto", "Unidos por marcas suaves"),
        "it": ("Legati dai segni morbidi e dalla luce del porto", "Legati dai segni morbidi"),
    },
    3: {
        "en": ("Bound by Soft Hour and Harbor Light", "Bound by Soft Hour"),
        "it": ("Legati dall'ora morbida e dalla luce del porto", "Legati dall'ora morbida"),
    },
    4: {
        "en": ("Bound by Soft Gate and Harbor Light", "Bound by Soft Gate"),
    },
}

# Spoiler-light chapter map for ARC reading guidance (Book 1 known openers + series length).
ARC_CHAPTER_GUIDES: dict[int, dict[str, list[dict[str, str]]]] = {
    1: {
        "en": [
            {"title": "Chapter 1 — The Unsigned Contract", "blurb": "The pact is on the table. Elena counts locks. Julian does not negotiate."},
            {"title": "Chapter 2 — Shadows in the Kitchen", "blurb": "Protocol under the same roof. Trust is measured before heat."},
            {"title": "Chapters 3–24", "blurb": "Full slow-burn arc in the EPUB after you join — honest review if you finish."},
        ],
        "de": [
            {"title": "Kapitel 1 — Der unsignierte Vertrag", "blurb": "Der Pakt liegt auf dem Tisch. Elena zählt Schlösser. Julian verhandelt nicht."},
            {"title": "Kapitel 2 — Schatten in der Küche", "blurb": "Protokoll unter einem Dach. Vertrauen vor Hitze."},
            {"title": "Kapitel 3–24", "blurb": "Der volle Slow-Burn im EPUB nach der Anmeldung — ehrliche Rezension, wenn du fertig bist."},
        ],
        "fr": [
            {"title": "Chapitre 1 — Le contrat non signé", "blurb": "Le pacte est sur la table. Elena compte les verrous. Julian ne négocie pas."},
            {"title": "Chapitre 2 — Ombres dans la cuisine", "blurb": "Protocole sous le même toit. La confiance avant la chaleur."},
            {"title": "Chapitres 3–24", "blurb": "L’arc slow burn complet dans l’EPUB après inscription — avis honnête si vous terminez."},
        ],
        "es": [
            {"title": "Capítulo 1 — El contrato sin firmar", "blurb": "El pacto está sobre la mesa. Elena cuenta cerraduras. Julian no negocia."},
            {"title": "Capítulo 2 — Sombras en la cocina", "blurb": "Protocolo bajo el mismo techo. Confianza antes del calor."},
            {"title": "Capítulos 3–24", "blurb": "El slow burn completo en el EPUB tras unirte — reseña honesta si terminas."},
        ],
        "it": [
            {"title": "Capitolo 1 — Il contratto non firmato", "blurb": "Il patto è sul tavolo. Elena conta le serrature. Julian non negozia."},
            {"title": "Capitolo 2 — Ombre in cucina", "blurb": "Protocollo sotto lo stesso tetto. Fiducia prima del calore."},
            {"title": "Capitoli 3–24", "blurb": "Lo slow burn completo nell’EPUB dopo l’iscrizione — recensione onesta se finisci."},
        ],
    },
    2: {
        "en": [
            {"title": "Chapter 1 — The Soft Mark Arrives", "blurb": "Quiet List ink. Glass Holding stamp. Berths — or invisibility."},
            {"title": "Chapter 2 — Pier Seven", "blurb": "The harbor keeps score. Loyalty becomes a line item."},
            {"title": "Chapters 3–23", "blurb": "Full ledger-pressure arc in the EPUB after signup."},
        ],
        "de": [
            {"title": "Kapitel 1 — Das Soft Mark trifft ein", "blurb": "Quiet-List-Tinte. Glass-Holding-Stempel. Liegeplätze — oder Unsichtbarkeit."},
            {"title": "Kapitel 2 — Pier Sieben", "blurb": "Der Hafen führt Buch. Loyalität wird zur Position."},
            {"title": "Kapitel 3–23", "blurb": "Der volle Ledger-Druck im EPUB nach der Anmeldung."},
        ],
        "fr": [
            {"title": "Chapitre 1 — La marque douce arrive", "blurb": "Encre Quiet List. Cachet Glass Holding. Postes d’amarrage — ou invisibilité."},
            {"title": "Chapitre 2 — Jetée Sept", "blurb": "Le port tient les comptes. La loyauté devient une ligne."},
            {"title": "Chapitres 3–23", "blurb": "L’arc pression-ledger complet dans l’EPUB après inscription."},
        ],
        "es": [
            {"title": "Capítulo 1 — Llega la marca suave", "blurb": "Tinta Quiet List. Sello Glass Holding. Amarres — o invisibilidad."},
            {"title": "Capítulo 2 — Muelle Siete", "blurb": "El puerto lleva la cuenta. La lealtad se vuelve partida."},
            {"title": "Capítulos 3–23", "blurb": "El arco de presión del libro mayor completo en el EPUB tras unirte."},
        ],
        "it": [
            {"title": "Capitolo 1 — Arriva il segno morbido", "blurb": "Inchiostro Quiet List. Timbro Glass Holding. Ormeggi — o invisibilità."},
            {"title": "Capitolo 2 — Molo Sette", "blurb": "Il porto tiene i conti. La lealtà diventa una voce."},
            {"title": "Capitoli 3–23", "blurb": "L’arco di pressione del libro mastro completo nell’EPUB dopo l’iscrizione."},
        ],
    },
    3: {
        "en": [
            {"title": "Soft Hour opens", "blurb": "Basement clinic under empire. Mercy priced in blood and paperwork."},
            {"title": "Holding squeeze", "blurb": "Established bond. Visible cost. Kindle EPUB after signup."},
        ],
        "it": [
            {"title": "Si apre l’Ora morbida", "blurb": "Clinica nel seminterrato sotto l’impero. La misericordia ha un prezzo."},
            {"title": "Pressione Holding", "blurb": "Legame già consolidato. Costo visibile. EPUB Kindle dopo l’iscrizione."},
        ],
    },
    4: {
        "en": [
            {"title": "Soft Gate pressure", "blurb": "Sealed history as leverage. Pharmacy and berth denial."},
            {"title": "Series close", "blurb": "Earned ending with a visible price — full EPUB after signup."},
        ],
    },
}

# Nav / footer / intro script / chapter chrome — merged into ARC_I18N[lang].
ARC_I18N_EXTRA: dict[str, dict[str, str]] = {
    "en": {
        "nav_home": "Home",
        "nav_harbor": "Harbor Light",
        "nav_arc": "ARC",
        "nav_warnings": "Warnings",
        "nav_tropes": "Tropes",
        "nav_music": "Music",
        "nav_menu": "Open menu",
        "nav_primary": "Primary",
        "nav_lang_aria": "Soft Hour language",
        "nav_langs_aria": "Soft Hour languages",
        "footer_join_arc": "Join ARC",
        "footer_sample": "Sample Ch1",
        "cta_hub_ch1": "Free Chapter 1",
        "footer_summaries": "Summaries",
        "footer_glossary": "Glossary",
        "footer_guide": "Soft Hour guide",
        "footer_cinematic": "Cinematic",
        "footer_mafia_guide": "Mafia romance guide",
        "footer_warnings": "Content warnings",
        "footer_tropes": "Slow burn tropes",
        "footer_music": "Music",
        "footer_about": "About",
        "footer_faq": "FAQ",
        "footer_soft_hour": "Soft Hour:",
        "footer_spotify": "Spotify Soft Hour",
        "footer_gumroad": "Gumroad",
        "footer_amazon_series": "Amazon series",
        "cover_alt": "Cover — {title}",
        "tropes_heading": "Tropes",
        "trope_1": "Dark Mafia",
        "trope_2": "Marriage Pact",
        "trope_3": "Slow Burn",
        "trope_4": "Morally Grey",
        "trope_5": "Dual-POV",
        "script_heading": "ARC brief — read this first",
        "script_p1": (
            "You are joining the Harbor Light ARC Team for a free EPUB. "
            "No paid stars. No guaranteed five-star reviews. If you finish, leave an honest Amazon and/or Goodreads review."
        ),
        "script_p2": (
            "This is adult dark mafia romance: slow burn, protocol, and a visible price. "
            "DNF is fine — do not fake a finish. 18+ only."
        ),
        "script_p3": (
            "Submit the form below to unlock your EPUB download on this page. "
            "Optional: open a sample chapter first, then collapse it when you are ready to sign up."
        ),
        "chapters_heading": "Chapters & reading preview",
        "chapters_note": "Expand a chapter to peek. Collapse it when you want to focus on the signup form.",
        "chapters_map_heading": "Chapter map (spoiler-light)",
        "chapter_sample_label": "Read sample",
        "chapter_collapse_hint": "Tap the title to expand or collapse.",
        "books_collapse_hint": "Tap a book title to expand or collapse that ARC.",
        "fail_network": "network",
        "asin_label": "ASIN",
    },
    "de": {
        "nav_home": "Start",
        "nav_harbor": "Harbor Light",
        "nav_arc": "ARC",
        "nav_warnings": "Warnungen",
        "nav_tropes": "Motive",
        "nav_music": "Musik",
        "nav_menu": "Menü öffnen",
        "nav_primary": "Hauptnavigation",
        "nav_lang_aria": "Soft-Hour-Sprache",
        "nav_langs_aria": "Soft-Hour-Sprachen",
        "footer_join_arc": "ARC beitreten",
        "footer_sample": "Probe Kap. 1",
        "cta_hub_ch1": "Kap. 1 gratis",
        "footer_summaries": "Zusammenfassungen",
        "footer_glossary": "Glossar",
        "footer_guide": "Soft-Hour-Guide",
        "footer_cinematic": "Cinematisch",
        "footer_mafia_guide": "Mafia-Romance-Guide",
        "footer_warnings": "Inhaltswarnungen",
        "footer_tropes": "Slow-Burn-Motive",
        "footer_music": "Musik",
        "footer_about": "Über",
        "footer_faq": "FAQ",
        "footer_soft_hour": "Soft Hour:",
        "footer_spotify": "Spotify Soft Hour",
        "footer_gumroad": "Gumroad",
        "footer_amazon_series": "Amazon-Serie",
        "cover_alt": "Titelbild — {title}",
        "tropes_heading": "Motive",
        "trope_1": "Dunkle Mafia",
        "trope_2": "Ehevertrag",
        "trope_3": "Langsamer Spannungsbogen",
        "trope_4": "Moralisch grau",
        "trope_5": "Doppelperspektive",
        "script_heading": "ARC-Briefing — zuerst lesen",
        "script_p1": (
            "Du trittst dem Harbor-Light-ARC-Team für ein kostenloses EPUB bei. "
            "Keine bezahlten Sterne. Keine garantierten fünf Sterne. Wenn du fertig bist: ehrliche Amazon-/Goodreads-Rezension."
        ),
        "script_p2": (
            "Das ist Dark Romance für Erwachsene: langsamer Spannungsbogen, Protokoll und ein sichtbarer Preis. "
            "Nicht zu Ende lesen ist ok — keinen Abschluss vortäuschen. Nur 18+."
        ),
        "script_p3": (
            "Formular unten absenden → EPUB-Download bleibt auf dieser Seite. "
            "Wahlweise: Probekapitel zuerst öffnen, dann einklappen, wenn du dich anmelden willst."
        ),
        "fact_epub": "Kostenloses EPUB (primär) — Kindle-Apps, Apple Books, Kobo. PDF wahlweise, falls verfügbar.",
        "fact_slow": "Langsamer Spannungsbogen — Vertrauen und Protokoll vor Hitze. Kein Spice ab Kapitel eins.",
        "chapters_heading": "Kapitel & Lesevorschau",
        "chapters_note": "Kapitel aufklappen zum Lesen. Wieder zuklappen, wenn du dich aufs Formular konzentrieren willst.",
        "chapters_map_heading": "Kapitelkarte (wenig Spoiler)",
        "chapter_sample_label": "Probe lesen",
        "chapter_collapse_hint": "Titel antippen zum Auf-/Zuklappen.",
        "books_collapse_hint": "Buchtitel antippen, um dieses ARC auf- oder zuzuklappen.",
        "fail_network": "Netzwerk",
        "asin_label": "ASIN",
        "fact_reviews": (
            "Keine bezahlten Rezensionen. Keine garantierten 5★. Schreib, was du wirklich denkst. "
            "Nicht zu Ende lesen ist ok — keinen Abschluss vortäuschen."
        ),
        "edition_lede": (
            "{title} — dunkle Mafia, Protokoll im gesicherten Raum, langsamer Spannungsbogen (kein schnelles Spice). "
            "Happy End mit sichtbarem Preis."
        ),
        "edition_note": (
            "Wenn du fertig bist: ehrliche Amazon-/Goodreads-Rezension. "
            "Sterne sind nicht käuflich. Nicht zu Ende lesen ist ok — keinen Abschluss vortäuschen."
        ),
        "optional_pdf": "PDF-Innenlayout (wahlweise)",
        "tile_arc_only": "Nur ARC · noch kein Amazon",
    },
    "fr": {
        "nav_home": "Accueil",
        "nav_harbor": "Harbor Light",
        "nav_arc": "ARC",
        "nav_warnings": "Avertissements",
        "nav_tropes": "Tropes",
        "nav_music": "Musique",
        "nav_menu": "Ouvrir le menu",
        "nav_primary": "Navigation principale",
        "nav_lang_aria": "Langue Soft Hour",
        "nav_langs_aria": "Langues Soft Hour",
        "footer_join_arc": "Rejoindre l’ARC",
        "footer_sample": "Extrait ch. 1",
        "cta_hub_ch1": "Chap. 1 gratuit",
        "footer_summaries": "Résumés",
        "footer_glossary": "Glossaire",
        "footer_guide": "Guide Soft Hour",
        "footer_cinematic": "Cinématique",
        "footer_mafia_guide": "Guide romance mafia",
        "footer_warnings": "Avertissements de contenu",
        "footer_tropes": "Tropes slow burn",
        "footer_music": "Musique",
        "footer_about": "À propos",
        "footer_faq": "FAQ",
        "footer_soft_hour": "Soft Hour :",
        "footer_spotify": "Spotify Soft Hour",
        "footer_gumroad": "Gumroad",
        "footer_amazon_series": "Série Amazon",
        "cover_alt": "Couverture — {title}",
        "tropes_heading": "Tropes",
        "trope_1": "Mafia sombre",
        "trope_2": "Pacte de mariage",
        "trope_3": "Tension lente",
        "trope_4": "Moralement gris",
        "trope_5": "Double point de vue",
        "script_heading": "Brief ARC — à lire d’abord",
        "script_p1": (
            "Vous rejoignez l’équipe ARC Harbor Light pour un EPUB gratuit. "
            "Pas d’étoiles payées. Pas de cinq étoiles garanties. Si vous terminez : avis Amazon et/ou Goodreads honnête."
        ),
        "script_p2": (
            "Romance sombre adulte : tension lente, protocole, prix visible. "
            "Abandonner en cours de route est acceptable — ne feignez pas d’avoir fini. 18+ uniquement."
        ),
        "script_p3": (
            "Envoyez le formulaire ci-dessous pour débloquer l’EPUB sur cette page. "
            "Au choix : ouvrez un extrait, puis repliez-le avant de vous inscrire."
        ),
        "fact_epub": "EPUB gratuit (principal) — apps Kindle, Apple Books, Kobo. PDF intérieur au choix si disponible.",
        "fact_slow": "Tension lente — confiance et protocole avant la chaleur. Pas de spice dès le chapitre un.",
        "chapters_heading": "Chapitres & aperçu lecture",
        "chapters_note": "Dépliez un chapitre pour lire. Repliez-le pour vous concentrer sur le formulaire.",
        "chapters_map_heading": "Carte des chapitres (peu de spoilers)",
        "chapter_sample_label": "Lire l’extrait",
        "chapter_collapse_hint": "Touchez le titre pour ouvrir ou fermer.",
        "books_collapse_hint": "Touchez un titre de livre pour ouvrir ou fermer cet ARC.",
        "fail_network": "réseau",
        "asin_label": "ASIN",
        "fact_reviews": (
            "Pas d’avis payés. Pas de 5★ garantis. Dites ce que vous avez vraiment pensé. "
            "Abandonner en cours de route est OK — ne feignez pas d’avoir fini."
        ),
        "edition_lede": (
            "{title} — mafia sombre, protocole de salle verrouillée, tension lente (pas de spice rapide). "
            "Fin heureuse avec un prix visible."
        ),
        "edition_note": (
            "Si vous terminez : avis Amazon et/ou Goodreads honnête. "
            "Les étoiles ne s’achètent pas. Abandonner en cours de route est acceptable — ne feignez pas d’avoir fini."
        ),
        "fact_reviews": (
            "Pas d’avis payés. Pas de 5★ garantis. Dites ce que vous avez vraiment pensé. "
            "Abandonner en cours de route est acceptable — ne feignez pas d’avoir fini."
        ),
    },
    "es": {
        "nav_home": "Inicio",
        "nav_harbor": "Harbor Light",
        "nav_arc": "ARC",
        "nav_warnings": "Avisos",
        "nav_tropes": "Tropos",
        "nav_music": "Música",
        "nav_menu": "Abrir menú",
        "nav_primary": "Navegación principal",
        "nav_lang_aria": "Idioma Soft Hour",
        "nav_langs_aria": "Idiomas Soft Hour",
        "footer_join_arc": "Unirse al ARC",
        "footer_sample": "Muestra cap. 1",
        "cta_hub_ch1": "Cap. 1 gratis",
        "footer_summaries": "Resúmenes",
        "footer_glossary": "Glosario",
        "footer_guide": "Guía Soft Hour",
        "footer_cinematic": "Cinemático",
        "footer_mafia_guide": "Guía romance mafia",
        "footer_warnings": "Avisos de contenido",
        "footer_tropes": "Tropos slow burn",
        "footer_music": "Música",
        "footer_about": "Acerca de",
        "footer_faq": "FAQ",
        "footer_soft_hour": "Soft Hour:",
        "footer_spotify": "Spotify Soft Hour",
        "footer_gumroad": "Gumroad",
        "footer_amazon_series": "Serie Amazon",
        "cover_alt": "Portada — {title}",
        "tropes_heading": "Tropos",
        "trope_1": "Mafia oscura",
        "trope_2": "Pacto matrimonial",
        "trope_3": "Tensión lenta",
        "trope_4": "Moralmente gris",
        "trope_5": "Doble punto de vista",
        "script_heading": "Briefing ARC — lee esto primero",
        "script_p1": (
            "Te unes al equipo ARC de Harbor Light por un EPUB gratis. "
            "Sin estrellas pagadas. Sin cinco estrellas garantizadas. Si terminas: reseña honesta en Amazon y/o Goodreads."
        ),
        "script_p2": (
            "Romance oscuro para adultos: tensión lenta, protocolo y un precio visible. "
            "Dejarlo a medias está bien — no finjas haber terminado. Solo 18+."
        ),
        "script_p3": (
            "Envía el formulario de abajo para desbloquear el EPUB en esta página. "
            "Si quieres: abre una muestra y ciérrala cuando quieras registrarte."
        ),
        "fact_epub": "EPUB gratis (principal) — apps Kindle, Apple Books, Kobo. PDF interior si lo hay.",
        "fact_slow": "Tensión lenta — confianza y protocolo antes del calor. No spice desde el capítulo uno.",
        "chapters_heading": "Capítulos y vista previa",
        "chapters_note": "Abre un capítulo para leer. Ciérralo para centrarte en el formulario.",
        "chapters_map_heading": "Mapa de capítulos (pocos spoilers)",
        "chapter_sample_label": "Leer muestra",
        "chapter_collapse_hint": "Toca el título para abrir o cerrar.",
        "books_collapse_hint": "Toca un título de libro para abrir o cerrar ese ARC.",
        "fail_network": "red",
        "asin_label": "ASIN",
        "fact_reviews": (
            "Sin reseñas pagadas. Sin 5★ garantizadas. Di lo que de verdad pensaste. "
            "Dejarlo a medias está bien — no finjas haber terminado."
        ),
        "edition_lede": (
            "{title} — mafia oscura, protocolo de sala cerrada, tensión lenta (sin spice rápido). "
            "Final feliz con un precio visible."
        ),
        "edition_note": (
            "Si terminas: reseña honesta en Amazon y/o Goodreads. "
            "Las estrellas no se compran. Dejarlo a medias está bien — no finjas haber terminado."
        ),
        "fact_reviews": (
            "Sin reseñas pagadas. Sin 5★ garantizadas. Di lo que de verdad pensaste. "
            "Dejarlo a medias está bien — no finjas haber terminado."
        ),
    },
    "it": {
        "nav_home": "Inizio",
        "nav_harbor": "Harbor Light",
        "nav_arc": "ARC",
        "nav_warnings": "Avvisi",
        "nav_tropes": "Tropi",
        "nav_music": "Musica",
        "nav_menu": "Apri menu",
        "nav_primary": "Navigazione principale",
        "nav_lang_aria": "Lingua Soft Hour",
        "nav_langs_aria": "Lingue Soft Hour",
        "footer_join_arc": "Unisciti all’ARC",
        "footer_sample": "Campione cap. 1",
        "cta_hub_ch1": "Mostra Cap. 1",
        "footer_summaries": "Riassunti",
        "footer_glossary": "Glossario",
        "footer_guide": "Guida Soft Hour",
        "footer_cinematic": "Cinematografico",
        "footer_mafia_guide": "Guida romance mafia",
        "footer_warnings": "Avvisi sui contenuti",
        "footer_tropes": "Tropi slow burn",
        "footer_music": "Musica",
        "footer_about": "Chi sono",
        "footer_faq": "FAQ",
        "footer_soft_hour": "Soft Hour:",
        "footer_spotify": "Spotify Soft Hour",
        "footer_gumroad": "Gumroad",
        "footer_amazon_series": "Serie Amazon",
        "cover_alt": "Copertina — {title}",
        "tropes_heading": "Tropi",
        "trope_1": "Mafia oscura",
        "trope_2": "Patto matrimoniale",
        "trope_3": "Tensione lenta",
        "trope_4": "Moralmente grigio",
        "trope_5": "Doppio punto di vista",
        "script_heading": "Brief ARC — leggi prima questo",
        "script_p1": (
            "Entri nel team ARC Harbor Light per un EPUB gratuito. "
            "Niente stelle pagate. Niente cinque stelle garantite. Se finisci: recensione onesta Amazon e/o Goodreads."
        ),
        "script_p2": (
            "Dark romance per adulti: tensione lenta, protocollo e un prezzo visibile. "
            "Abbandonare a metà va bene — non fingere di aver finito. Solo 18+."
        ),
        "script_p3": (
            "Invia il modulo sotto per sbloccare l’EPUB su questa pagina. "
            "Se vuoi: apri un campione, poi chiudilo quando vuoi iscriverti."
        ),
        "fact_epub": "EPUB gratuito (principale) — app Kindle, Apple Books, Kobo. PDF interno se disponibile.",
        "fact_slow": "Tensione lenta — fiducia e protocollo prima del calore. Niente spice dal capitolo uno.",
        "chapters_heading": "Capitoli e anteprima lettura",
        "chapters_note": "Apri un capitolo per leggere. Chiudilo per concentrarti sul modulo.",
        "chapters_map_heading": "Mappa dei capitoli (pochi spoiler)",
        "chapter_sample_label": "Leggi il campione",
        "chapter_collapse_hint": "Tocca il titolo per aprire o chiudere.",
        "books_collapse_hint": "Tocca un titolo di libro per aprire o chiudere quell’ARC.",
        "fail_network": "rete",
        "asin_label": "ASIN",
        "fact_reviews": (
            "Niente recensioni pagate. Niente 5★ garantite. Di’ cosa hai davvero pensato. "
            "Abbandonare a metà va bene — non fingere di aver finito."
        ),
        "edition_lede": (
            "{title} — mafia oscura, protocollo di sala chiusa, tensione lenta (niente calore immediato). "
            "Finale felice con un prezzo visibile."
        ),
        "edition_note": (
            "Se finisci: recensione onesta Amazon e/o Goodreads. "
            "Le stelle non si comprano. Abbandonare a metà va bene — non fingere di aver finito."
        ),
        "fact_reviews": (
            "Niente recensioni pagate. Niente 5★ garantite. Di’ cosa hai davvero pensato. "
            "Abbandonare a metà va bene — non fingere di aver finito."
        ),
    },
}


def merge_arc_i18n_extra(arc_i18n: dict[str, dict[str, str]]) -> None:
    """Mutate ARC_I18N in place with chrome/script/chapter strings."""
    for lang, extra in ARC_I18N_EXTRA.items():
        bucket = arc_i18n.setdefault(lang, {})
        bucket.update(extra)


def localized_arc_titles(book: int, lang: str, fallback_title: str, fallback_short: str) -> tuple[str, str]:
    """Return (full_title, short_title) for ARC edition chrome."""
    code = str(lang or "en").lower()[:2]
    row = (ARC_BOOK_TITLES.get(int(book)) or {}).get(code)
    if row:
        return row[0], row[1]
    en = (ARC_BOOK_TITLES.get(int(book)) or {}).get("en")
    if en and code == "en":
        return en[0], en[1]
    if en and code != "en":
        # Prefer lang-specific; if missing keep EN product title only for EN pages —
        # callers should pass lang that exists in ARC_BOOK_TITLES.
        return en[0], en[1]
    return fallback_title, fallback_short


def chapter_guide_for(book: int, lang: str) -> list[dict[str, str]]:
    """Spoiler-light chapter blurbs for ARC accordion."""
    code = str(lang or "en").lower()[:2]
    by_book = ARC_CHAPTER_GUIDES.get(int(book)) or {}
    return list(by_book.get(code) or by_book.get("en") or [])
