"""
PQC Transition Toolkit — Streamlit Dashboard
Implements & extends: Birgin & Celiktas (2026), IEEE Access
  DOI: 10.1109/ACCESS.2026.3669437

Team: Muhammad Ahmad (F2023332067) | Muhammad Aftab Ahmad (F2023332010) | Murtaza Ijaz (F2023332105)
Course: Information Security | UMT Lahore | Spring 2026
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from modules.qrs_engine import (
    evaluate_assets, evaluate_custom, generate_qrs_json, cicd_gate,
    PAPER_ASSETS, EXTENDED_ASSETS, AHP_WEIGHTS, THRESHOLDS
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PQC Transition Toolkit",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Colour map ────────────────────────────────────────────────────────────────
POLICY_COLORS = {
    "MIGRATE": "#C00000",
    "HYBRID":  "#E07000",
    "MONITOR": "#0070C0",
    "DEFER":   "#548235"
}

# ── Sidebar nav ───────────────────────────────────────────────────────────────
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/6/6b/UMT_logo.png/200px-UMT_logo.png",
                 width=120, use_column_width=False)
st.sidebar.title("🔐 PQC Transition Toolkit")
st.sidebar.caption("Implementing Birgin & Celiktas (2026)\nIEEE Access — DOI: 10.1109/ACCESS.2026.3669437")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigation", [
    "🏠 Home",
    "📊 QRS Dashboard — Paper Assets",
    "🌐 Extended QRS — New Contribution",
    "✏️ Custom Asset Assessment",
    "🚦 CI/CD Enforcement Gate",
    "📋 Evidence & Audit Log"
])

st.sidebar.markdown("---")
st.sidebar.markdown("**Team**")
st.sidebar.caption("Muhammad Ahmad · F2023332067\nMuhammad Aftab Ahmad · F2023332010\nMurtaza Ijaz · F2023332105")
st.sidebar.caption("UMT Lahore · Spring 2026")


# ═══════════════════════════════════════════════════════════
# PAGE: HOME
# ═══════════════════════════════════════════════════════════
if page == "🏠 Home":
    st.title("🔐 Post-Quantum Cryptography Transition Toolkit")
    st.subheader("Operationalizing the Birgin & Celiktas (2026) Framework")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Base Paper Assets", "6", "Reproduced")
    col2.metric("Extended Assets", "14", "+8 New ✨")
    col3.metric("Sectors Covered", "4", "New Contribution")
    col4.metric("Framework Phases", "7", "Fully Implemented")

    st.markdown("---")
    st.markdown("""
    ### About This Tool
    This toolkit **reproduces and extends** the seven-phase PQC Transition Framework proposed by
    Birgin & Celiktas (2026) in IEEE Access (DOI: `10.1109/ACCESS.2026.3669437`).

    The original paper formalises PQC transition as an operational systems-engineering problem centred on
    **Quantum Risk Scoring (QRS)** — a deterministic, AHP-calibrated scoring model — and **CI/CD enforcement gates**.

    This tool implements the full framework in Python/Streamlit and **extends** it with:
    - A cross-sector extended asset dataset (Healthcare, Finance, Energy, Education) — **new contribution**
    - Sector-level aggregated risk analysis — **new finding**
    - Interactive custom asset scoring — **new utility**
    - Real-time CI/CD gate simulation with audit artifact export
    """)

    st.markdown("---")
    st.markdown("### 7-Phase Framework (Birgin & Celiktas, 2026)")
    phases = [
        ("P1", "Asset Inventory", "Discover all cryptographic assets including shadow cryptography"),
        ("P2", "Classification", "Tag by exposure, sensitivity, regulatory dependency"),
        ("P3", "Risk Modeling", "Compute QRS scores using AHP-weighted formula"),
        ("P4", "Algorithm Selection", "Choose Kyber/Dilithium/SPHINCS+ per risk level"),
        ("P5", "Deployment", "CI/CD-enforced cryptographic validation gates"),
        ("P6", "Monitoring", "Prometheus/Grafana telemetry and fallback detection"),
        ("P7", "Governance", "OPA policy enforcement and audit alignment"),
    ]
    cols = st.columns(7)
    for i, (pid, title, desc) in enumerate(phases):
        with cols[i]:
            st.markdown(f"**{pid}**")
            st.markdown(f"*{title}*")
            st.caption(desc)

    st.markdown("---")
    st.info("📌 **QRS Formula** (Equation 1, paper p.33544):  \n"
            "`QRS = (0.30 × Data Longevity) + (0.25 × Algorithm Vulnerability) + (0.25 × Key Exposure) + (0.20 × System Dependence)`")


# ═══════════════════════════════════════════════════════════
# PAGE: QRS DASHBOARD — PAPER ASSETS
# ═══════════════════════════════════════════════════════════
elif page == "📊 QRS Dashboard — Paper Assets":
    st.title("📊 QRS Dashboard — Reproducing Paper Table 8")
    st.caption("Source: Birgin & Celiktas (2026), Table 8, p.33546 — exact reproduction")

    results = evaluate_assets(PAPER_ASSETS)
    df = pd.DataFrame(results)

    # Summary metrics
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("MIGRATE", len(df[df.policy=="MIGRATE"]), delta="Immediate action required", delta_color="inverse")
    c2.metric("HYBRID",  len(df[df.policy=="HYBRID"]),  delta="Hybrid controls needed")
    c3.metric("MONITOR", len(df[df.policy=="MONITOR"]), delta="Under telemetry")
    c4.metric("DEFER",   len(df[df.policy=="DEFER"]),   delta="Low risk")

    st.markdown("---")

    # Table
    st.subheader("QRS Results Table (Reproduced from Paper Table 8)")
    display_cols = ["id","name","algorithm","dl","av","ke","sd","qrs_score","policy"]
    display_df = df[display_cols].copy()
    display_df.columns = ["ID","Asset Name","Algorithm","Data Longevity","Algo Vuln","Key Exposure","Sys Depend","QRS Score","Policy"]

    def color_policy(val):
        colors = {"MIGRATE":"background-color:#FFD7D7","HYBRID":"background-color:#FFE8C0",
                  "MONITOR":"background-color:#C0DCFF","DEFER":"background-color:#D7F0C0"}
        return colors.get(val, "")

    styled = display_df.style.applymap(color_policy, subset=["Policy"])
    st.dataframe(styled, use_container_width=True)

    st.caption("Table 1: QRS evaluation of original six institutional assets reproduced from Birgin & Celiktas (2026), Table 8. "
               "Scores computed using AHP weights W=(0.30, 0.25, 0.25, 0.20). Policy thresholds: MIGRATE≥8.0, HYBRID≥7.0, MONITOR≥6.0.")

    st.markdown("---")

    # Bar chart
    st.subheader("QRS Score Comparison")
    fig = go.Figure()
    for policy, color in POLICY_COLORS.items():
        subset = df[df.policy == policy]
        if not subset.empty:
            fig.add_trace(go.Bar(
                x=subset["name"], y=subset["qrs_score"],
                name=policy, marker_color=color,
                text=subset["policy"], textposition="outside"
            ))
    fig.add_hline(y=8.0, line_dash="dash", line_color="red",   annotation_text="MIGRATE threshold (8.0)")
    fig.add_hline(y=7.0, line_dash="dash", line_color="orange",annotation_text="HYBRID threshold (7.0)")
    fig.add_hline(y=6.0, line_dash="dash", line_color="blue",  annotation_text="MONITOR threshold (6.0)")
    fig.update_layout(
        xaxis_title="Asset", yaxis_title="QRS Score", yaxis_range=[0, 10.5],
        legend_title="Policy", height=420,
        plot_bgcolor="white", paper_bgcolor="white"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Fig. 1: QRS scores for reproduced paper assets with policy threshold lines. "
               "Assets A1 and A2 exceed the MIGRATE threshold (8.0), requiring immediate PQC migration.")

    # Radar chart per asset
    st.subheader("Risk Factor Radar — Per Asset")
    asset_names = df["name"].tolist()
    sel = st.selectbox("Select asset", asset_names)
    row = df[df["name"]==sel].iloc[0]
    fig2 = go.Figure(go.Scatterpolar(
        r=[row.dl, row.av, row.ke, row.sd, row.dl],
        theta=["Data Longevity","Algo Vulnerability","Key Exposure","System Dependence","Data Longevity"],
        fill="toself", name=sel,
        line_color=POLICY_COLORS.get(row.policy,"#333")
    ))
    fig2.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,10])),
                       title=f"{sel} — Policy: {row.policy}  |  QRS: {row.qrs_score}")
    st.plotly_chart(fig2, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# PAGE: EXTENDED QRS — NEW CONTRIBUTION
# ═══════════════════════════════════════════════════════════
elif page == "🌐 Extended QRS — New Contribution":
    st.title("🌐 Extended Cross-Sector QRS Analysis")
    st.markdown("""
    > **New Contribution** — This section extends the original paper (Birgin & Celiktas, 2026) beyond its
    > single public-sector scenario to **four sectors: Healthcare, Finance, Energy, and Education**.
    > The 14-asset extended dataset and sector-level aggregated findings below represent original work
    > by the UMT team (Ahmad, Aftab, Ijaz, 2026).
    """)

    results = evaluate_assets(EXTENDED_ASSETS)
    df = pd.DataFrame(results)

    # Sector filter
    sectors = ["All"] + sorted(df["sector"].unique().tolist())
    sel_sector = st.selectbox("Filter by sector", sectors)
    if sel_sector != "All":
        df_view = df[df["sector"]==sel_sector]
    else:
        df_view = df

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("MIGRATE", len(df_view[df_view.policy=="MIGRATE"]))
    c2.metric("HYBRID",  len(df_view[df_view.policy=="HYBRID"]))
    c3.metric("MONITOR", len(df_view[df_view.policy=="MONITOR"]))
    c4.metric("DEFER",   len(df_view[df_view.policy=="DEFER"]))

    st.markdown("---")
    st.subheader("Extended Asset QRS Table — New Finding")
    disp = df_view[["id","sector","name","algorithm","dl","av","ke","sd","qrs_score","policy"]].copy()
    disp.columns = ["ID","Sector","Asset Name","Algorithm","DL","AV","KE","SD","QRS Score","Policy"]

    def color_policy(val):
        c = {"MIGRATE":"background-color:#FFD7D7","HYBRID":"background-color:#FFE8C0",
             "MONITOR":"background-color:#C0DCFF","DEFER":"background-color:#D7F0C0"}
        return c.get(val,"")

    st.dataframe(disp.style.applymap(color_policy, subset=["Policy"]), use_container_width=True)
    st.caption("Table 2: Extended QRS evaluation across 14 assets in four sectors. "
               "New contribution extending the original paper's 6-asset single-sector scenario. "
               "DL=Data Longevity, AV=Algorithm Vulnerability, KE=Key Exposure, SD=System Dependence.")

    st.markdown("---")
    st.subheader("Sector-Level Risk Distribution — New Finding")
    sector_summary = df.groupby(["sector","policy"]).size().reset_index(name="count")
    fig = px.bar(sector_summary, x="sector", y="count", color="policy",
                 color_discrete_map=POLICY_COLORS,
                 title="Policy State Distribution by Sector",
                 labels={"sector":"Sector","count":"Asset Count","policy":"Policy"})
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", height=380)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Fig. 2: Distribution of QRS-derived policy states across sectors. "
               "Finance and Energy sectors show the highest MIGRATE urgency, consistent with long-lived "
               "sensitive data and critical infrastructure dependencies.")

    st.markdown("---")
    st.subheader("Average QRS Score by Sector — New Finding")
    avg_scores = df.groupby("sector")["qrs_score"].mean().reset_index()
    avg_scores.columns = ["Sector","Avg QRS Score"]
    avg_scores["Avg QRS Score"] = avg_scores["Avg QRS Score"].round(3)
    fig2 = px.bar(avg_scores, x="Sector", y="Avg QRS Score",
                  color="Avg QRS Score", color_continuous_scale=["#548235","#0070C0","#E07000","#C00000"],
                  title="Average QRS Score per Sector", text="Avg QRS Score")
    fig2.add_hline(y=8.0, line_dash="dash", line_color="red",   annotation_text="MIGRATE (8.0)")
    fig2.add_hline(y=7.0, line_dash="dash", line_color="orange",annotation_text="HYBRID (7.0)")
    fig2.update_layout(plot_bgcolor="white", paper_bgcolor="white", height=380)
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Fig. 3: Average QRS scores per sector. Finance (avg 8.73) and Energy (avg 8.20) exceed "
               "the MIGRATE threshold, indicating these sectors require immediate PQC migration action. "
               "This cross-sector pattern was not analysed in the original paper.")

    st.success("✅ **New Contribution Summary:** The extended 14-asset cross-sector analysis reveals that "
               "Finance and Energy sectors demonstrate average QRS scores above the MIGRATE threshold (8.0), "
               "indicating sector-level systemic risk not identifiable from single-sector validation alone. "
               "This finding extends Birgin & Celiktas (2026) beyond their public-sector proof-of-concept.")


# ═══════════════════════════════════════════════════════════
# PAGE: CUSTOM ASSET ASSESSMENT
# ═══════════════════════════════════════════════════════════
elif page == "✏️ Custom Asset Assessment":
    st.title("✏️ Custom Asset Assessment")
    st.caption("Score your own cryptographic asset using the QRS model")

    with st.form("custom_form"):
        c1, c2 = st.columns(2)
        name      = c1.text_input("Asset Name", "My Server")
        algorithm = c2.text_input("Current Algorithm", "RSA-2048, TLS 1.2")
        sector    = c1.selectbox("Sector", ["Healthcare","Finance","Energy","Education","Government","Other"])

        st.markdown("**Rate each factor (1 = low risk, 10 = high risk)**")
        st.caption("Scoring rubric from paper Table 6")

        c1,c2,c3,c4 = st.columns(4)
        dl = c1.slider("Data Longevity", 1, 10, 7,
                       help="How long must this data remain confidential? (1=<1yr, 10=>10yrs)")
        av = c2.slider("Algorithm Vulnerability", 1, 10, 8,
                       help="Is the current algorithm classically vulnerable? (1=PQC-ready, 10=RSA/ECC only)")
        ke = c3.slider("Key Exposure", 1, 10, 6,
                       help="How widely distributed are keys? (1=HSM-backed, 10=widely distributed)")
        sd = c4.slider("System Dependence", 1, 10, 7,
                       help="How critical is this system? (1=non-critical, 10=mission-critical PKI)")

        submitted = st.form_submit_button("Compute QRS Score", type="primary")

    if submitted:
        result = evaluate_custom(name, algorithm, dl, av, ke, sd, sector)
        score  = result["qrs_score"]
        policy = result["policy"]
        color  = POLICY_COLORS[policy]

        st.markdown("---")
        st.markdown(f"## Result: <span style='color:{color}'>{policy}</span> — QRS Score: **{score}**",
                    unsafe_allow_html=True)

        meanings = {
            "MIGRATE": "⚠️ **Immediate action required.** This asset uses classical-only public-key cryptography on a high-risk profile. Begin PQC migration immediately using ML-KEM (Kyber) or ML-DSA (Dilithium).",
            "HYBRID":  "🔶 **Hybrid controls required.** Transition to hybrid classical+PQC negotiation. Maintain backward compatibility while introducing Kyber-768 or Dilithium-3.",
            "MONITOR": "🔵 **Monitor and plan.** Asset is below immediate risk threshold. Implement telemetry and plan migration within 12–24 months.",
            "DEFER":   "✅ **Defer.** Asset poses low quantum risk. Reassess annually or when NIST guidelines update."
        }
        st.info(meanings[policy])

        # Breakdown
        st.markdown("### Score Breakdown")
        breakdown = pd.DataFrame({
            "Factor": ["Data Longevity","Algorithm Vulnerability","Key Exposure","System Dependence"],
            "Raw Score": [dl, av, ke, sd],
            "AHP Weight": [0.30, 0.25, 0.25, 0.20],
            "Weighted": [round(dl*0.30,3), round(av*0.25,3), round(ke*0.25,3), round(sd*0.20,3)]
        })
        st.dataframe(breakdown, use_container_width=True)
        st.metric("Total QRS Score", score, f"Policy: {policy}")


# ═══════════════════════════════════════════════════════════
# PAGE: CI/CD ENFORCEMENT GATE
# ═══════════════════════════════════════════════════════════
elif page == "🚦 CI/CD Enforcement Gate":
    st.title("🚦 CI/CD Enforcement Gate")
    st.caption("Algorithm 1 — Crypto-Aware CI/CD Validation Gate (Birgin & Celiktas, 2026, p.33542)")

    dataset = st.radio("Select asset dataset", ["Paper Assets (6)", "Extended Assets (14)"])
    if "Paper" in dataset:
        results = evaluate_assets(PAPER_ASSETS)
    else:
        results = evaluate_assets(EXTENDED_ASSETS)

    audit = cicd_gate(results)
    decision = audit["decision"]

    decision_colors = {"ALLOW":"#548235","RESTRICT":"#E07000","BLOCK":"#C00000"}
    decision_icons  = {"ALLOW":"✅","RESTRICT":"⚠️","BLOCK":"🚫"}

    st.markdown(f"## Gate Decision: {decision_icons[decision]} "
                f"<span style='color:{decision_colors[decision]};font-size:2rem'>{decision}</span>",
                unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("MIGRATE Assets", audit["migrate_count"])
    c2.metric("HYBRID Assets",  audit["hybrid_count"])
    c3.metric("MONITOR Assets", audit["monitor_count"])
    c4.metric("DEFER Assets",   audit["defer_count"])

    if audit["findings"]:
        st.markdown("### Violations Detected")
        for f in audit["findings"]:
            with st.expander(f"[{f['policy']}] {f['asset_name']} — QRS: {f['qrs_score']}"):
                for v in f["violations"]:
                    st.error(v)
    else:
        st.success("No violations detected — all assets compliant.")

    st.markdown("---")
    st.subheader("Audit Artifact — audit_gate.json")
    st.code(json.dumps(audit, indent=2), language="json")
    st.caption("This immutable audit artifact corresponds to Table 9 (paper p.33547). "
               "Each enforcement decision is timestamped and includes asset ID, QRS score, policy flag, and violation details.")

    # Save artifact
    os.makedirs("evidence", exist_ok=True)
    audit_path = "evidence/audit_gate.json"
    with open(audit_path, "w") as f:
        json.dump(audit, f, indent=2)
    st.download_button("⬇️ Download audit_gate.json", json.dumps(audit, indent=2),
                       file_name="audit_gate.json", mime="application/json")


# ═══════════════════════════════════════════════════════════
# PAGE: EVIDENCE & AUDIT LOG
# ═══════════════════════════════════════════════════════════
elif page == "📋 Evidence & Audit Log":
    st.title("📋 Evidence & Audit Log")
    st.caption("Evidence bundle — Table 10 (Birgin & Celiktas, 2026, p.33547)")

    # Generate and show QRS artifact
    paper_results   = evaluate_assets(PAPER_ASSETS)
    extended_results = evaluate_assets(EXTENDED_ASSETS)

    os.makedirs("evidence", exist_ok=True)
    artifact = generate_qrs_json(paper_results + extended_results, "evidence/qrs_results.json")

    st.markdown("### qrs_results.json (Phase P3 artifact)")
    st.code(json.dumps(artifact, indent=2)[:2000] + "\n  ... [truncated] ...", language="json")
    st.download_button("⬇️ Download qrs_results.json",
                       json.dumps(artifact, indent=2),
                       file_name="qrs_results.json", mime="application/json")

    st.markdown("---")
    st.markdown("### Evidence Taxonomy (Table 10, paper p.33547)")
    evidence_table = pd.DataFrame([
        ["P1", "cmdb_snapshot.json", "Asset inventory with tags", "Schema validation + checksum"],
        ["P3", "qrs_results.json",   "QRS scores with policy flags", "Determinism check"],
        ["P5", "audit_gate.json",    "CI/CD ALLOW/RESTRICT/BLOCK decision", "Pipeline log + hash"],
        ["P6", "cryptolyzer_report.txt", "TLS config visibility", "Re-run against endpoint"],
    ], columns=["Phase","Artifact","Description","Verification"])
    st.dataframe(evidence_table, use_container_width=True)

    st.markdown("---")
    st.markdown("### AHP Weight Verification")
    ahp_df = pd.DataFrame({
        "Factor": ["Data Longevity","Algorithm Vulnerability","Key Exposure","System Dependence"],
        "Weight": [0.30, 0.25, 0.25, 0.20],
        "Rationale": [
            "Long-lived data faces highest HNDL exposure risk",
            "Classical-only (RSA/ECC) = maximum vulnerability",
            "Distributed keys = broad attack surface",
            "Mission-critical systems = highest operational impact"
        ]
    })
    st.dataframe(ahp_df, use_container_width=True)
    st.caption("AHP Consistency Ratio CR ≈ 0.022 < 0.10 — acceptable per Saaty (1987), Table 7 of paper.")
