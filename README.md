# Regional Tuberculosis Case-Pattern Clustering (TB Insight)

> **INT 396 — Data Science & Machine Learning Capstone Project**  
> An exploratory unsupervised clustering platform and clinical decision-support system analyzing aggregated Indian regional tuberculosis surveillance indicators (Ministry of Health & Family Welfare / Central TB Division, 2019–2023).

[![Python 3.12](https://img.shields.io/badge/Python-3.12-38bdf8?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.42+-ff4b4b?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-Clustering-f59e0b?style=flat-square&logo=scikit-learn)](https://scikit-learn.org/)
[![Tests](https://img.shields.io/badge/Unit%20Tests-6%2F6%20Passing-10b981?style=flat-square)](tests/)
[![Status](https://img.shields.io/badge/Deployment-Live%20HTTPS-10b981?style=flat-square)](https://tb-insight-india.streamlit.app/)

---

## 🔗 Quick Project Links

* **Live Deployed Web Application:** [https://tb-insight-india.streamlit.app/](https://tb-insight-india.streamlit.app/)
* **GitHub Repository:** [https://github.com/revaank/INT396-PROJECT-TB](https://github.com/revaank/INT396-PROJECT-TB)
* **Coursework Presentation:** [`TB_Insight_Project_Presentation.pptx`](TB_Insight_Project_Presentation.pptx) (13 slides with embedded visual screenshots)

---

## 📌 Public Health Problem & Context

India accounts for approximately **27% of global tuberculosis notifications**. While the National Tuberculosis Elimination Program (NTEP) establishes unified guidelines, **India's 36 States and Union Territories exhibit stark epidemiological diversity**:

1. **High-Volume Agrarian States** (e.g., Uttar Pradesh, Bihar) face immense absolute patient volumes (>600k notifications), causing diagnostic backlogs in district laboratories and ongoing household transmission.
2. **Metabolic & Urbanizing States** (e.g., Kerala, Tamil Nadu) manage moderate caseloads but face a high prevalence of **diabetes-TB comorbidity (>18%)**, demanding concurrent glycemic management to prevent treatment relapse.
3. **Mountainous & Frontier States** (e.g., Sikkim, Ladakh, Arunachal Pradesh) deal with low total cases but extreme terrain dispersion, creating high sample-transit latency.

**The Solution:** This project utilizes **multivariate unsupervised clustering (Ward’s Hierarchical Agglomerative Clustering)** on standardized regional surveillance metrics. By discovering natural "Health Twins" across states, health administrators and civil servants can transition from uniform national mandates to targeted, evidence-based regional interventions.

---

## 🏛️ 4-Module Platform Architecture

The web platform is organized into 4 distinct, zero-clutter public health modules served through a unified Streamlit query router (`app/main.py`):

| Module | Core Purpose & Features | View |
|---|---|---|
| **1. Regional Cluster Map** | Interactive vector choropleth map of India. Visualizes cluster boundaries, notifications rank, treatment success rates, and diagnostic positivity. | `preview.html` |
| **2. State Compare** | Bilateral head-to-head benchmarking between any two Indian states. Automatically generates delta calculations and programmatic policy recommendations. | `compare_preview.html` |
| **3. Treatment & Recovery** | Executive public health dossiers for each state: primary operational bottlenecks, peer "Health Twins", a 3-tier budget allocation matrix, and a 90-day operational roadmap for IAS/CMOs. | `overcome_preview.html` |
| **4. Help & Resources** | Emergency 24×7 national TB lifelines (`1800-11-6666`), State TB Officer directory, verified zero-cost care guidelines (free diagnosis, free medicines, ₹1,000/mo Poshan DBT), and an interactive AI Care Assistant. | `knowledge_preview.html` |

---

## 🔬 Academic Coverage (Units II, III & IV)

| Unit | Syllabus Requirement | Implementation in Project |
|---|---|---|
| **Unit II** | **Data Preparation & Preprocessing** | • Missing value auditing (132 values preserved as genuine missingness; zero-imputation avoided).<br>• National aggregate (`All India`) filtered out to prevent statistical skew.<br>• Reshaped from long surveillance format to standardized state feature matrix.<br>• Z-score normalization via `StandardScaler` ($\mu=0, \sigma=1$) to prevent high-population states from dominating distance metrics. |
| **Unit III** | **Partition Clustering & Hierarchical Comparison** | • Evaluated $k \in [2, 5]$ across both K-Means and Agglomerative Hierarchical Clustering.<br>• Evaluated Euclidean vs. Manhattan distance metrics.<br>• Computed Silhouette Score, Davies-Bouldin Index, and Calinski-Harabasz Ratio.<br>• Generated full interactive Dendrogram using Ward's minimum-variance linkage. |
| **Unit IV** | **Dimensionality Reduction, Interpretation & Stability** | • 2-Component Principal Component Analysis (PCA) capturing >88% of multivariate variance.<br>• Quantitative cluster stability analysis across random initializations and distance metrics.<br>• Selection and clinical defense of optimal $k=3$ cluster configuration. |

---

## 📊 Summary of Identified Clusters ($k=3$)

```
                        ┌─────────────────────────────────────────────────────────┐
                        │      All 36 Indian States & Union Territories           │
                        └───────────────────────────┬─────────────────────────────┘
                                                    │
                 ┌──────────────────────────────────┼──────────────────────────────────┐
                 │                                  │                                  │
    ┌─────────────────────────┐        ┌─────────────────────────┐        ┌─────────────────────────┐
    │  Cluster 0: High-Volume │        │  Cluster 1: Comorbidity │        │  Cluster 2: Mountain &  │
    │         Giants          │        │      Burden States      │        │      Frontier Units     │
    ├─────────────────────────┤        ├─────────────────────────┤        ├─────────────────────────┤
    │ • UP, Bihar, MP, WB, RJ │        │ • Kerala, TN, AP, KA, MH│        │ • Sikkim, Ladakh, MZ, AN│
    │ • Caseloads > 200,000   │        │ • DM Comorbidity > 15%  │        │ • Low volume, rugged    │
    │ • Bottleneck: Lab lag   │        │ • Bottleneck: Glycemia  │        │ • Bottleneck: Transit   │
    │ • Priority: PHC Truenat │        │ • Priority: Dual Clinic │        │ • Priority: Mobile Vans │
    └─────────────────────────┘        └─────────────────────────┘        └─────────────────────────┘
```

---

## 🛡️ Public Health Ethics & Academic Guardrails

In compliance with academic data science ethics and clinical research standards:
1. **Aggregated Spatial Data Only:** No patient-level records, individual identifiers, or private medical records are collected or exposed.
2. **Reported Notifications $\neq$ True Incidence:** The models cluster *recorded notifications and screening outcomes*. These reflect health-seeking behavior and diagnostic capacity, which must not be conflated with true community infection rates.
3. **Non-Diagnostic Scope:** This platform is an exploratory public health intelligence tool designed for administrators. It does **not** diagnose individual patients or predict individual clinical outcomes.
4. **Factual Accuracy:** Reflects the official October 2024 Ministry update doubling the **Ni-kshay Poshan Yojana** financial assistance from ₹500/month to **₹1,000/month** per notified patient.

---

## 🎓 Key Viva Defense Questions & Answers

**Q1: Why did you choose Ward's Hierarchical Clustering instead of default K-Means?**  
> *Answer:* For a finite administrative geography of $N=36$ states, Ward's hierarchical clustering provides a deterministic, tree-structured dendrogram without stochastic centroid initialization. Ward's criterion minimizes within-cluster variance, yielding compact and operationally distinct policy cohorts.

**Q2: Why was feature scaling essential before clustering?**  
> *Answer:* Uttar Pradesh has a population exceeding 230 million, whereas Sikkim has approximately 680,000 (a >300× scale disparity). Without `StandardScaler`, Euclidean distances would be overwhelmed entirely by raw patient counts, grouping states merely by population rather than discovering clinical transmission patterns (e.g., comorbidity rates, treatment success %).

**Q3: How were missing values audited and handled?**  
> *Answer:* 132 missing surveillance indicators were audited. Rather than artificially imputing zeros (which would falsify disease absence), complete-case evaluation was enforced per feature slice, preserving mathematical fidelity.

---

## 💻 Installation & Local Reproduction

### Prerequisites
- Python 3.10+ (tested on Python 3.12)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/revaank/INT396-PROJECT-TB.git
cd INT396-PROJECT-TB
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux / macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Run Automated Unit Tests
```bash
python -m unittest discover tests -v
```
*(All 6 unit tests should report `OK`)*

### 4. Launch Interactive Application
```bash
# Windows one-click:
START_TB_INSIGHT.bat

# Or terminal:
streamlit run app/main.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📂 Repository File Tree

```
INT396-PROJECT-TB/
├── app/
│   └── main.py                     # Streamlit application core & query router
├── data/
│   ├── raw/dataful_20833/          # MoHFW TB surveillance datasets & dictionary
│   └── preview_state_data.json     # Grounded state telemetry baseline
├── notebooks/
│   └── reproducible_analysis.py    # Standalone terminal pipeline for viva execution
├── presentation_assets/            # High-resolution screenshots of the 4 platform views
├── results/                        # Exported cluster tables & reproducible outputs
├── scripts/
│   ├── build_upgraded_preview.py   # Generator for Module 1 (Map)
│   ├── build_clean_bento_overcome.py # Generator for Module 3 (Recovery)
│   ├── build_streamlined_knowledge_html.py # Generator for Module 4 (Resources)
│   └── generate_presentation_pptx.py # 13-slide PowerPoint generator script
├── src/
│   ├── __init__.py
│   ├── data.py                     # Ingestion, validation, complete-case pivoting
│   └── analysis.py                 # Clustering, Dendrogram, PCA & stability metrics
├── tests/
│   ├── __init__.py
│   └── test_analysis.py            # Automated unit test suite (6 test cases)
├── .gitignore                      # Git exclusion rules
├── AGENTS.md                       # Academic project specification & guidelines
├── compare_preview.html            # Standalone Module 2: State Comparison view
├── knowledge_preview.html          # Standalone Module 4: Help, Helplines & AI view
├── overcome_preview.html           # Standalone Module 3: Treatment & Recovery view
├── preview.html                    # Standalone Module 1: Regional Cluster Map view
├── requirements.txt                # Production Python dependencies
├── START_TB_INSIGHT.bat            # Windows one-click desktop startup script
├── TB_Insight_Project_Presentation.pptx # 13-Slide presentation deck
└── README.md                       # Comprehensive project documentation
```

---

## 📜 Academic Integrity & Attribution
* **Data Sources:** Central TB Division, Directorate General of Health Services, Ministry of Health & Family Welfare (MoHFW), Government of India.
* **Coursework:** INT 396 Machine Learning & Data Science.
* **Submission Date:** November 2026.
