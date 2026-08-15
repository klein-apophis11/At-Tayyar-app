# data_library.py
# Private, local storage for all Jafari Fiqh text blocks and transliterations

JAFARI_STEPS = {
    "takbeer": {
        "title": "Takbiratul Ihram", 
        "arabic": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\nاللهُ أَكْبَر", 
        "action": "Translit: Bismillahir-Rahmanir-Rahim. Allahu Akbar.\n\nIntend the prayer. Raise hands to shoulders and say the Takbeer."
    },
    "qiyam_1": {
        "title": "Rakah 1: Qiyam (Recitation)", 
        "arabic": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ...", 
        "action": "Recite Surah Al-Fatiha followed by a second full Surah.\nFocus your intent completely on Allah's presence."
    },
    "qiyam_2": {
        "title": "Rakah 2: Qiyam (Recitation)", 
        "arabic": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ...", 
        "action": "Recite Surah Al-Fatiha and a second full Surah seamlessly while sitting still."
    },
    "qiyam_generic": {
        "title": "Qiyam (Remaining Rakahs)", 
        "arabic": "سُبْحَانَ اللَّهِ وَالْحَمْدُ لِلَّهِ وَلَا إِلَٰهَ إِلَّا اللَّهُ وَاللَّهُ أَكْبَرُ", 
        "action": "Translit: Subhanallahi wal-hamdulillahi wa la ilaha illallahu wallahu Akbar.\n\nRecite this Tasbihat al-Arba'ah three times quietly."
    },
    "qunoot": {
        "title": "Rakah 2: Qunoot", 
        "arabic": "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ", 
        "action": "Translit: Rabbana atina fid-dunya hasanatan wa fil-akhirati hasanatan wa qina 'adhaban-nar.\n\n✨ JAFARI STEP: Raise your hands palms up in front of your face and supplicate."
    },
    "ruku": {
        "title": "Ruku' (Bowing)", 
        "arabic": "سُبْحَانَ رَبِّيَ الْعَظِيمِ وَبِحَمْدِهِ", 
        "action": "Translit: Subhana Rabbiyal-'Adheemi wa bihamdih.\n\nLean forward slightly. Hands on knees. Recite the praise."
    },
    "sujud_1": {
        "title": "First Sujud", 
        "arabic": "سُبْحَانَ رَبِّيَ الْأَعْلَىٰ وَبِحَمْدِهِ", 
        "action": "Translit: Subhana Rabbiyal-'A'la wa bihamdih.\n\nLean forward deeply. Face onto your thumb or back of hand as your valid substitute."
    },
    "jalsah": {
        "title": "Jalsah (Pause)", 
        "arabic": "أَسْتَغْفِرُ اللَّهَ رَبِّ وَأَتُوبُ إِلَيْهِ", 
        "action": "Translit: Astaghfirullaha Rabbi wa Atubu Ilayh.\n\nReturn to your upright sitting position and pause briefly."
    },
    "sujud_2": {
        "title": "Second Sujud", 
        "arabic": "سُبْحَانَ رَبِّيَ الْأَعْلَىٰ وَبِحَمْدِهِ", 
        "action": "Translit: Subhana Rabbiyal-'A'la wa bihamdih.\n\nLean forward deeply again, placing your forehead back onto your thumb."
    },
    "tashahhud_mid": {
        "title": "Mid-Prayer Tashahhud", 
        "arabic": "أَشْهَدُ أَنْ لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ\nوَأَشْهَدُ أَنَّ مُحَمَّدًا عَبْدُهُ وَرَسُولُهُ\nاللَّهُمَّ صَلِّ عَلَىٰ مُحَمَّدٍ وَآلِ مُحَمَّدٍ", 
        "action": "Translit:\n1. Ashhadu an la ilaha illallahu wahdahu la sharika lah.\n2. Wa ashhadu anna Muhammadan 'abduhu wa Rasuluh.\n3. Allahumma salli 'ala Muhammadin wa ali Muhammad."
    },
    "tashahhud_final": {
        "title": "Final Tashahhud & Tasleem", 
        "arabic": "السَّلَامُ عَلَيْكَ أَيُّهَا النَّبِيُّ وَرَحْمَةُ اللَّهِ وَبَرَكَاتُهُ\nالسَّلَامُ عَلَيْنَا وَعَلَىٰ عِبَادِ اللَّهِ الصَّالِحِينَ\nالسَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللَّهِ وَبَرَكَاتُهُ", 
        "action": "Translit:\n1. Assalamu 'alayka ayyuhan-Nabiyyu wa rahmatullahi wa barakatuh.\n2. Assalamu 'alayna wa 'ala 'ibadillahis-salihin.\n3. Assalamu 'alaykum wa rahmatullahi wa barakatuh."
    }
}

TASBIH_PHASES = [
    {"count": 34, "arabic": "اللهُ أَكْبَر", "translit": "Allahu Akbar", "meaning": "Allah is Greater"},
    {"count": 33, "arabic": "الْحَمْدُ لِلَّهِ", "translit": "Alhamdulillah", "meaning": "Praise be to Allah"},
    {"count": 33, "arabic": "سُبْحَانَ اللَّهِ", "translit": "Subhanallah", "meaning": "Glory be to Allah"}
]
