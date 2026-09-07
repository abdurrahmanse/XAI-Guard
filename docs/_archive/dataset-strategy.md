# XAI-Guard: Dataset Strategy & Unified Attack Taxonomy

To ensure the XAI-Guard model architectures generalize across diverse, real-world network topologies and are not overfit to a single organizational signature, the evaluation framework mandates cross-dataset benchmarking. We utilize four distinct cybersecurity datasets, each presenting a unique machine learning challenge.

---

## 1. Dataset Selections & Justifications

### 1.1. NSL-KDD (Historical Baseline)
- **Justification:** While dated, NSL-KDD remains the most widely cited benchmark in classical IDS literature. It serves as the baseline to ensure our deep learning architectures can fundamentally solve established problems before progressing to modern datasets.
- **Official URL:** [University of New Brunswick - NSL-KDD](https://www.unb.ca/cic/datasets/nsl.html)
- **License:** Open Academic Use
- **Record Count:** 125,973 (Train) / 22,544 (Test)
- **Feature Count:** 41 (plus 1 label)
- **Class Distribution:** Normal (53%), DoS (36%), Probe (9%), R2L (1%), U2R (<1%)
- **Primary Research Challenge:** Resolving the legacy U2R/R2L rare-class detection problem and verifying baseline classical ML implementation correctness.

### 1.2. CICIDS-2017 (Modern Flow Analysis)
- **Justification:** Represents modern, realistic background traffic (B-Profile) intertwined with up-to-date attack scenarios (M-Profile). It is captured via PCAP and processed through CICFlowMeter, representing the exact tabular feature space a modern SOC firewall would output.
- **Official URL:** [University of New Brunswick - CICIDS-2017](https://www.unb.ca/cic/datasets/ids-2017.html)
- **License:** Open Academic Use
- **Record Count:** ~2,830,743
- **Feature Count:** 78 (plus 1 label)
- **Class Distribution:** BENIGN (80.3%), DoS/DDoS (13.5%), PortScan (5.6%), BruteForce (0.5%), Web Attack (0.07%), Botnet (0.07%), Infiltration (0.001%)
- **Primary Research Challenge:** Severe class imbalance. The `Infiltration` class contains fewer than 40 samples, requiring advanced SMOTE/ADASYN augmentation or focal loss functions to detect.

### 1.3. UNSW-NB15 (Comprehensive Taxonomy)
- **Justification:** Specifically designed to capture a hybrid of modern normal activities and contemporary synthesized attack behaviors utilizing the IXIA PerfectStorm tool. Features include deep packet inspection (DPI) flow statistics.
- **Official URL:** [UNSW Canberra - NB15](https://research.unsw.edu.au/projects/unsw-nb15-dataset)
- **License:** Open Academic Use
- **Record Count:** 2,540,044 (Full) / 175,341 (Partitioned Train)
- **Feature Count:** 49
- **Class Distribution:** Normal (87%), Generic (7%), Exploits (3%), Fuzzers (1%), DoS (0.6%), Reconnaissance (0.5%), Analysis (0.1%), Backdoors (0.08%), Shellcode (0.06%), Worms (0.006%)
- **Primary Research Challenge:** High intra-class variance and multi-class decision boundary overlap.

### 1.4. BETH (Real-World Enterprise Temporal Drift)
- **Justification:** A modern dataset consisting of Linux host-level logs (syslog, auditd) captured on a globally distributed honeypot network. Unlike synthetic datasets, BETH is strictly chronological and exhibits significant temporal concept drift as adversaries change tactics over the collection period.
- **Official URL:** [Kaggle - BETH Dataset](https://www.kaggle.com/datasets/kateeesponda/beth-dataset)
- **License:** CC BY-NC-SA 4.0
- **Record Count:** 7,631,053 (Train) / 1,489,521 (Test)
- **Feature Count:** 14 (Host-level OS features)
- **Class Distribution:** Benign (90%), Suspect (10%)
- **Primary Research Challenge:** Evaluating model robustness to zero-day temporal data drift (RQ8) and host-level feature adaptation.

---

## 2. Unified Attack Taxonomy

To train a singular, generalized XAI-Guard classification engine capable of inferring across all datasets, we construct a unified $N=7$ `Enum` taxonomy. All heterogeneous, dataset-specific label strings are mapped deterministically to one of the following master classes:

| XAI-Guard Taxonomy | Description |
|--------------------|-------------|
| **`DDOS`** | Denial of Service / Distributed Denial of Service attacks aimed at resource exhaustion. |
| **`PORT_SCAN`** | Network reconnaissance, ping sweeps, and port probing. |
| **`BRUTE_FORCE`** | Password guessing, dictionary attacks (SSH, FTP, Telnet). |
| **`BOTNET`** | Command & Control (C2) beaconing, backdoor communication, and malware pivoting. |
| **`WEB_ATTACK`** | Application-layer exploits (SQLi, XSS, Path Traversal). |
| **`INFILTRATION`** | Internal network exploitation, privilege escalation, shellcode drops, and APT lateral movement. |
| **`NORMAL`** | Benign, expected enterprise background traffic. |

---

## 3. Deterministic Label Mapping Table

The data engineering pipeline (Phase 11) must strictly enforce the following mappings during the ETL phase. 
*Note: Any class marked with **(⚠️ Low-Resource)** contains insufficient training samples in its native dataset and will automatically trigger synthetic minority over-sampling in the ML pipeline.*

| XAI-Guard Label | NSL-KDD (Native) | CICIDS-2017 (Native) | UNSW-NB15 (Native) |
|-----------------|------------------|----------------------|--------------------|
| **`DDOS`** | `neptune`, `smurf`, `back`, `teardrop`, `pod`, `land`, `apache2`, `udpstorm`, `processtable`, `mailbomb` | `DDoS`, `DoS Hulk`, `DoS GoldenEye`, `DoS slowloris`, `DoS Slowhttptest` | `DoS` |
| **`PORT_SCAN`** | `satan`, `ipsweep`, `portsweep`, `nmap`, `mscan`, `saint` | `PortScan` | `Reconnaissance` |
| **`BRUTE_FORCE`** | `guess_passwd`, `dict`, `httptunnel`, `named`, `sendmail`, `snmpgetattack`, `snmpguess` | `FTP-Patator`, `SSH-Patator` | `Fuzzers` |
| **`BOTNET`** | *N/A (Mapped to Infiltration)* | `Bot` | `Backdoors`, `Worms` **(⚠️ Low-Resource)** |
| **`WEB_ATTACK`** | `phf`, `xlock`, `xsan` **(⚠️ Low-Resource)** | `Web Attack  Brute Force`, `Web Attack  XSS`, `Web Attack  Sql Injection` **(⚠️ Low-Resource)** | `Exploits`, `Generic` |
| **`INFILTRATION`**| `buffer_overflow`, `rootkit`, `loadmodule`, `perl`, `sqlattack` **(⚠️ Low-Resource)** | `Infiltration` **(⚠️ Low-Resource)** | `Shellcode`, `Analysis` **(⚠️ Low-Resource)** |
| **`NORMAL`** | `normal` | `BENIGN` | `Normal` |

*(Note: The BETH dataset operates on a strictly binary `Benign` / `Suspect` axis and is utilized exclusively for Temporal Drift evaluation (RQ8), mapping to `NORMAL` and `INFILTRATION`/`BOTNET` generically).*
