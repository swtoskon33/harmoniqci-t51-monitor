# T5.1 monitor, 2026-10-14

Changes: 4. Flags: 6. New candidates: 36.

## Needs expert review

- **qkd_kme_server**: no Dockerfile/compose in the root: to be checked
- **Open QKD Network (qkd-net)**: no commit since 2024-01-25
- **QuNetSim**: no commit since 2023-06-07
- **QuKayDee**: page offline: not reachable (ProxyError)
- **NetSquid**: page offline: not reachable (ProxyError)
- **qkd-simulator (HarmoniQCI)**: repository not found on GitHub (or private and the token has no access)

## Changes written to the Excel file

| Tool | Field | Old | New |
| --- | --- | --- | --- |
| qkd_kme_server | Last commit | 2026-04-01 | 2026-09-27 |
| QUBIP etsi-qkd-004 | Docker | To be checked | Yes |
| QKDNetSim v2.0 | Last commit | 2026-09-04 | 2026-10-08 |
| SeQUeNCe | Last commit | 2026-09-13 | 2026-10-13 |

## New candidates (decide in the sheet "Candidates": Add or Reject)

| Repository | Stars | Last push | Description |
| --- | --- | --- | --- |
| [LUMII-Syslab/qkd-stub](https://github.com/LUMII-Syslab/qkd-stub) | 0 | 2026-10-09 | Deterministic HTTPS stub for QKD integration testing. Implements the ETSI GS QKD 014 key-delivery API using a shared PSK |
| [QOJena/etsi014_rs](https://github.com/QOJena/etsi014_rs) | 0 | 2026-10-09 |  |
| [matteogrande/qsdn-adapter](https://github.com/matteogrande/qsdn-adapter) | 1 | 2026-10-09 | QKD Southbound Adapter for simulated SDN/ONOS and ETSI GS QKD 014 KMS orchestration. |
| [JNPRAutomate/Quantum-Safe-MACsec](https://github.com/JNPRAutomate/Quantum-Safe-MACsec) | 3 | 2026-10-06 | The quantum key distribution (QKD) MACSEC script is written in python3. The script allows the JUNOS devices to fetch key |
| [arnika-project/arnika](https://github.com/arnika-project/arnika) | 42 | 2026-10-04 | Arnika - Quantum secure VPN |
| [Rodolphe21/qkd-etsi014-poc](https://github.com/Rodolphe21/qkd-etsi014-poc) | 1 | 2026-08-09 | Wire-level analysis of the ETSI GS QKD 014 key delivery API — mTLS traces, test cases, and a Python client against a sim |
| [ait-crypto/kms-sdn-agent-interface-specification](https://github.com/ait-crypto/kms-sdn-agent-interface-specification) | 4 | 2026-09-17 | QUICKS: a KMS to SDN Agent interface specification for QKDN |
| [AndresRzCh/etsi-qkd-015](https://github.com/AndresRzCh/etsi-qkd-015) | 1 | 2026-03-21 | Python implementation of ETSI GS QKD 015 (SD-QKD control interface) with SDN controller, RESTCONF nodes, and full workfl |
| [sara-star-quant/perspectra-fold](https://github.com/sara-star-quant/perspectra-fold) | 0 | 2026-07-24 | Architecture and reference research for high-dimensional QKD (qudits), hybrid quantum-classical networks, and PQC alignm |
| [Filip2142/QKDNetSim-Reserve-Aware-QoS-for-Satellite-QKD](https://github.com/Filip2142/QKDNetSim-Reserve-Aware-QoS-for-Satellite-QKD) | 0 | 2026-06-01 |  |
| [QUBIP/hybridization-module](https://github.com/QUBIP/hybridization-module) | 0 | 2026-05-06 |  Hybrid Key Exchange module combining QKD and PQC using ETSI GS QKD 004 standard. Includes TLS setup, liboqs integration |
| [Qkd004/Qkd004](https://github.com/Qkd004/Qkd004) | 0 | 2025-09-25 |  |
| [diogoftm/minimal-etsi-qkd-004](https://github.com/diogoftm/minimal-etsi-qkd-004) | 0 | 2025-04-01 | Very simple adaptation of ETSI's QKD 004 server/client (edition3) to support oblivious key requests and minimal operatio |
| [cybermerqury/etsi-gs-qkd-020-referenceimplementation](https://github.com/cybermerqury/etsi-gs-qkd-020-referenceimplementation) | 0 | 2026-09-15 |  |
| [adrianML7t/TFG](https://github.com/adrianML7t/TFG) | 1 | 2025-08-25 | RESTful API based on ETSI GS QKD 020 |
| [next-door-key/qkd-trusted-node](https://github.com/next-door-key/qkd-trusted-node) | 7 | 2025-01-03 | QKD KMS system implementation that allows key sharing beyond 1 QKD link |
| [josephofir/resilient-qkd-macsec](https://github.com/josephofir/resilient-qkd-macsec) | 0 | 2026-08-21 | Resilient QKD Integration with MACsec — proof-of-concept KME emulator, MKA with a QKD_Key_Id TLV, and an overhead measur |
| [John-Jepsen/qkdsec](https://github.com/John-Jepsen/qkdsec) | 1 | 2026-07-15 | A developer toolkit for Quantum Key Distribution: ETSI GS QKD 014 client (sync + async), KME conformance probe, BB84 sim |
| [jhhdez/qkdPlugin](https://github.com/jhhdez/qkdPlugin) | 0 | 2026-07-07 | QKD Strongswan plugin for rfc 9370 with a KME graceful-degradation mechanism. |
| [vmosescu/QKD-Infra](https://github.com/vmosescu/QKD-Infra) | 0 | 2024-11-22 | Key Management Entity (KME) Simulator |
| [ganiganesh25/qkdnetsim-mini](https://github.com/ganiganesh25/qkdnetsim-mini) | 0 | 2026-08-02 | Minimal QKD network simulator with a Flask ETSI GS QKD 014 KMS and structured log emitters |
| [syndpk/hybrid-pqc-qkd-kms-logs](https://github.com/syndpk/hybrid-pqc-qkd-kms-logs) | 0 | 2026-05-27 | Structured JSON-line logs from the Key Management System (KMS) of a deployed hybrid Post-Quantum Cryptography (PQC) and  |
| [LUMII-Syslab/sgx-qkms](https://github.com/LUMII-Syslab/sgx-qkms) | 0 | 2026-02-26 | Intel SGX protected Q-KMS. Remotely-attested OTP key relaying in QKD networks. ETSI GS QKD 014 API. |
| [cyriltan/QKDFileEncryptApp](https://github.com/cyriltan/QKDFileEncryptApp) | 0 | 2025-10-09 | This code seeks to demonstrate how one can pull QKD keys from the Toshiba KMS emulator using ETSI GS QKD 014 interface a |
| [SAMIYE/QKD-Interoperable-KMS-API](https://github.com/SAMIYE/QKD-Interoperable-KMS-API) | 0 | 2025-04-01 |  |
| [ikiu99/qkd-sdn-graded-containment](https://github.com/ikiu99/qkd-sdn-graded-containment) | 0 | 2026-09-20 | Graded detection and containment of compromised trusted relays in software-defined QKD networks: simulator, sweeps and t |
| [Andryd22/SDN-QKD](https://github.com/Andryd22/SDN-QKD) | 1 | 2026-04-15 | Implementation of an SDN-enhanced digital twin for QKD networks |
| [raied11/RAIED](https://github.com/raied11/RAIED) | 0 | 2026-01-22 | Personal projects and hands-on experiments covering IoT, SDN, Raspberry Pi, Arduino, QKD, security, and cybersecurity. |
| [gianniniluca/Containerize-onos-controller](https://github.com/gianniniluca/Containerize-onos-controller) | 0 | 2025-10-13 | A containerized SDN controller for QKD networks: The objective of this repo is to containerize the ONOS controller withi |
| [Abbey-12/qkd-sdn-api](https://github.com/Abbey-12/qkd-sdn-api) | 0 | 2025-03-21 |  |
| [sajjanmdb123-cmd/SeQUeNCe_BB84_LM05_Comparison](https://github.com/sajjanmdb123-cmd/SeQUeNCe_BB84_LM05_Comparison) | 0 | 2026-09-12 | A Python-based comparison of BB84 and LM05 quantum key distribution protocols using the SeQUeNCe quantum network simulat |
| [qurbanaliq/qkdSim](https://github.com/qurbanaliq/qkdSim) | 0 | 2025-05-27 | Quantum Key Distribution network simulator, it was part of my university thesis on Trust Relay based Quantum Key Distrib |
| [Vishnupriya-saji/Sequence---Quantum-Mechanics-simulator](https://github.com/Vishnupriya-saji/Sequence---Quantum-Mechanics-simulator) | 0 | 2024-10-30 | 🧪 SeQUeNCe is a quantum network simulator designed to model and test quantum communication protocols like entanglement d |
| [Peti0918/SatelliteCommunication](https://github.com/Peti0918/SatelliteCommunication) | 0 | 2026-09-07 | Python simulator for modeling and visualizing time-varying satellite quantum communication and QKD networks. |
| [api-evangelist/aliro-quantum](https://github.com/api-evangelist/aliro-quantum) | 0 | 2026-10-04 | Aliro Quantum — independent third-party profile of a public API surface, by API Evangelist. Aliro Quantum (branded "Alir |
| [hamamh66/FreeEnergy-QKD-PQC-STIN](https://github.com/hamamh66/FreeEnergy-QKD-PQC-STIN) | 0 | 2026-10-01 | Reproducible simulation for free-energy-based stability and secure resource orchestration in hybrid QKD–PQC satellite–te |
