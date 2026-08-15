# At-Tayyar (الطَّيَّار): Seated Jafari Salat Guide 📿♿

**At-Tayyar** is a lightweight, privacy-focused, offline desktop companion application specifically designed by and for Muslim wheelchair users and individuals facing physical mobility challenges. 

Named in honor of **Ja'far al-Tayyar**—the noble companion whom Allah granted wings in Paradise—this application provides an intuitive visual guide to performing daily prayers accurately from a seated position according to the **Jafari (Shia) jurisprudence (Fiqh)**.

---

## Key Features ✨

*   **Jafari Multi-Rakah Layouts**: Supports accurate structures for Fajr (2 Rakahs), Maghrib (3 Rakahs), and Dhuhr/Asr/Isha (4 Rakahs) prayers, complete with automated transitions for mid-prayer Tashahhud intervals.
*   **Seated Sujud Guidelines**: Built-in textual references explicitly detailing the legitimate Jafari *Rukhsah* (concession) of using the thumb or the back of the hand as a valid Turbah/Mohr substitution for prostration when external clay tablets are unreachable.
*   **Integrated Tasbih Counter**: Automatically transitions into a dedicated, hands-free tracking board for the **Tasbih of Lady Fatima Zahra (sa)** right after the final Tasleem.
*   **High-Visibility Corner Counter**: Features a massive, ultra-bright red indicator (`Rakah: X / Y`) in the top-right margin for easy readability during lower postures (Ruku' and Sujud).
*   **Total Security & Complete Privacy**: Operates 100% offline. Zero tracking scripts, zero internet connectivity, zero database logins, and **absolutely no microphone or camera access**. 

---

## Control Mechanisms 📲

To maintain complete physical peace and security without the threat of being spied on, the application features an interface controlled purely by manual input hardware:
*   **Spacebar and Backspace Control**: Follow the steps of making du'a and the Tasbih counter seamlessly by hitting your wireless keyboard's spacebar. You can use the backspace if you make a mistake as well.

---

## How to Install and Run Locally 💻

### Prerequisites
Ensure your computer has **Python 3.10+** installed. This project uses Python's native `tkinter` library, meaning it requires **zero external library installations (`pip`)**.

### Repository Structure
Ensure the following files remain grouped within the same folder directory:
1.  `jafari_app.py` — The core user interface and navigation engine.
2.  `data_library.py` — Local dictionary storing all Arabic texts, actions, and phonetic English transliterations.
3.  `salat_history.txt` — (Automatically generated) Private, offline local data file tracking your daily habits.

### Execution
Open your terminal directory or command prompt and run the primary script:
```bash
python jafari_app.py
```

*Windows Users*: You can execute the app via your desktop background using a shortcut batch file (`.bat`) pointing to your installation directory:
```cmd
@echo off
start pythonw "C:\YourFolder\jafari_app.py"
```

---

## Fiqh Foundation 📖
A guide and tool for praying seated and ease of worship (*Rukhsah*) for disabled individuals following the Jafari madhab, utilizing proper recitations during bowing and prostrations. This is something I wished and looked for when I first converted to Islam.

---

## License 📜
This software is shared as open-source code for the spiritual and physical benefit of the global Ummah. Feel free to copy, modify, and distribute it to any brother or sister in need of help with prayer.

*Designed and Developed by klein-apophis11.*
