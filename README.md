# ForensIQ – Offline Investigation Intelligence Platform 🕵️‍♂️

**The CPU-First Hackathon Project**
*Transform scattered evidence into connected investigation intelligence—completely offline.*

## The Problem
Criminal investigations involve hundreds of unstructured documents: FIRs, witness statements, forensic reports, and evidence logs. Investigators spend countless hours manually connecting information across these sources, increasing the chances of missing critical links or contradictions. Uploading this highly sensitive data to cloud AI is legally prohibited.

## The Solution
**ForensIQ** is an offline-first, CPU-powered AI platform that ingests unstructured investigation documents and extracts structured entities (people, locations, events, evidence). It automatically links related evidence and builds a chronological investigation timeline. 

All processing happens locally on the investigator's machine, ensuring sensitive case data never leaves the device.

## Core Features
1. **Entity Extraction**: Uses local Small Language Models (SLMs) to pull out suspects, witnesses, locations, and timestamps from raw text.
2. **Timeline Generation**: Automatically maps extracted events onto a chronological timeline.
3. **Contradiction Detection**: Flags conflicting statements across different documents.
4. **100% Air-Gapped**: Runs entirely on local CPU inference (`llama.cpp`), strictly adhering to the "Network OFF" hackathon rule.

## License
Open Source under GPL-3.0 (Strong Copyleft).
