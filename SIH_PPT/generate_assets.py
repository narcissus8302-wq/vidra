import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont

# Directory setup
BASE_DIR = "SIH_PPT/assets"
os.makedirs(f"{BASE_DIR}/satellite", exist_ok=True)
os.makedirs(f"{BASE_DIR}/diagrams", exist_ok=True)
os.makedirs(f"{BASE_DIR}/charts", exist_ok=True)
os.makedirs(f"{BASE_DIR}/ui", exist_ok=True)

# Styling palette - Vivid Azure & Dark Navy Theme
BG_DARK = "#0B1120"
BG_CARD = "#0F172A"
AZURE_MAIN = "#007AFF"
AZURE_BRIGHT = "#00D2FF"
AZURE_ACCENT = "#0B84FE"
TEXT_WHITE = "#FFFFFF"
TEXT_MUTED = "#94A3B8"
ALERT_RED = "#FF3B30"
SUCCESS_GREEN = "#34C759"
BORDER_COLOR = "#1E293B"

# Set matplotlib dark style
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.facecolor'] = BG_DARK
plt.rcParams['axes.facecolor'] = BG_CARD

def create_satellite_imagery():
    """Generates realistic simulated Sentinel-2 satellite scene before, after, and change mask."""
    np.random.seed(42)
    h, w = 500, 500

    # Base terrain: background field (dark olive/green)
    base = np.zeros((h, w, 3), dtype=np.uint8)
    base[:, :] = [30, 45, 30] # Vegetation background

    # Add river winding through (blue/azure)
    y_coords = np.arange(h)
    x_river = (200 + 40 * np.sin(y_coords / 50)).astype(int)
    for y in range(h):
        rw = 35 + int(10 * np.cos(y / 30))
        base[y, max(0, x_river[y]-rw):min(w, x_river[y]+rw)] = [15, 85, 140]

    # Baseline Before 2021: sparse greenery, open soil
    before = base.copy()
    # Soil patches
    before[100:250, 260:420] = [60, 50, 40]
    # Add noise / texture
    noise = np.random.randint(-10, 10, (h, w, 3))
    before = np.clip(before.astype(int) + noise, 0, 255).astype(np.uint8)

    # Save Before
    img_before = Image.fromarray(before)
    draw = ImageDraw.Draw(img_before)
    draw.rectangle([10, 10, 240, 40], fill=(11, 17, 32, 200))
    draw.text((20, 15), "SENTINEL-2 | 2021-04-12 | T43QKB", fill=AZURE_BRIGHT)
    img_before.save(f"{BASE_DIR}/satellite/scene_before_2021.png")

    # After 2024: New industrial structure built in soil patch
    after = before.copy()
    # Industrial buildings (bright grey/white high reflectiveness)
    after[120:200, 280:360] = [210, 215, 225]
    after[140:180, 375:410] = [190, 195, 205]
    # Paved access road connecting to river bank
    after[160:175, 200:280] = [120, 125, 130]

    img_after = Image.fromarray(after)
    draw = ImageDraw.Draw(img_after)
    draw.rectangle([10, 10, 240, 40], fill=(11, 17, 32, 200))
    draw.text((20, 15), "SENTINEL-2 | 2024-04-15 | T43QKB", fill=AZURE_BRIGHT)
    img_after.save(f"{BASE_DIR}/satellite/scene_after_2024.png")

    # Change Mask (Azure highlight on persistent change)
    mask = np.zeros((h, w, 4), dtype=np.uint8)
    # Industrial site changed area highlighted
    mask[115:205, 275:415, 0:3] = [0, 210, 255] # Azure color
    mask[115:205, 275:415, 3] = 160 # Semi transparent
    mask[155:180, 200:280, 0:3] = [0, 210, 255]
    mask[155:180, 200:280, 3] = 160

    change_overlay = Image.fromarray(after).convert("RGBA")
    mask_img = Image.fromarray(mask, mode="RGBA")
    combined = Image.alpha_composite(change_overlay, mask_img)

    draw_c = ImageDraw.Draw(combined)
    draw_c.rectangle([110, 110, 420, 210], outline="#00D2FF", width=3)
    draw_c.rectangle([10, 10, 320, 40], fill=(11, 17, 32, 220))
    draw_c.text((20, 15), "PERSISTENT CHANGE CONFIDENCE: 96.4%", fill="#00D2FF")
    combined.convert("RGB").save(f"{BASE_DIR}/satellite/change_mask.png")

def create_temporal_chart():
    """Generates spectral temporal trajectory curve chart over multi-year satellite history."""
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=200)

    years = np.array([2020.0, 2020.5, 2021.0, 2021.5, 2022.0, 2022.5, 2023.0, 2023.5, 2024.0, 2024.5, 2025.0])

    # Seasonal vegetation fluctuation (NDVI) - cyclic
    ndvi = 0.5 + 0.25 * np.sin(2 * np.pi * years) + np.random.normal(0, 0.02, len(years))

    # NDBI (Normalized Difference Built-up Index) - sharp persistent elevation starting late 2022
    ndbi = 0.15 + 0.05 * np.sin(2 * np.pi * years)
    ndbi[years >= 2022.5] += 0.45 # Structural shift
    ndbi += np.random.normal(0, 0.015, len(years))

    ax.plot(years, ndvi, label="NDVI (Vegetation Index - Seasonal)", color="#34C759", linewidth=2, linestyle="--", marker="o")
    ax.plot(years, ndbi, label="NDBI (Built-up Index - Persistent Onset)", color=AZURE_BRIGHT, linewidth=3, marker="s")

    # Highlight change onset
    ax.axvline(x=2022.5, color=ALERT_RED, linestyle=":", linewidth=2, label="Detected Change Onset (Q3 2022)")
    ax.axvspan(2022.5, 2025.0, color=AZURE_MAIN, alpha=0.15)

    ax.set_title("Multi-Temporal Spectral Trajectory Analysis (2020-2025)", fontsize=12, fontweight="bold", color="white", pad=12)
    ax.set_xlabel("Acquisition Timeline (Years)", color=TEXT_MUTED, fontsize=10)
    ax.set_ylabel("Spectral Index Value", color=TEXT_MUTED, fontsize=10)
    ax.grid(True, color="#1E293B", linestyle="-", alpha=0.7)
    ax.legend(facecolor=BG_CARD, edgecolor=BORDER_COLOR, labelcolor="white", loc="upper left")

    plt.tight_layout()
    plt.savefig(f"{BASE_DIR}/charts/temporal_trajectory.png", dpi=200, bbox_inches="tight")
    plt.close()

def create_retrieval_benchmark_chart():
    """Generates validation and retrieval performance bar chart."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=200)

    # Semantic Retrieval Metrics
    metrics = ['Recall@1', 'Recall@5', 'Precision@5', 'MRR', 'nDCG@5']
    scores = [78.4, 92.1, 89.5, 85.3, 90.8]

    bars1 = ax1.bar(metrics, scores, color=AZURE_MAIN, edgecolor=AZURE_BRIGHT, width=0.5)
    ax1.set_ylim(0, 100)
    ax1.set_title("Semantic Retrieval Accuracy (%)", fontweight="bold", fontsize=11, color="white", pad=10)
    ax1.grid(axis='y', color="#1E293B", linestyle="--")
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, f"{yval:.1f}%", ha='center', va='bottom', color="white", fontsize=9, fontweight="bold")

    # False Alarm Suppression Metrics
    categories = ['Naive Difference', 'Quality Masked', '+ Seasonal Filter', '+ Temporal Engine']
    false_alarm_rate = [48.2, 28.5, 12.1, 3.4] # Percentage false alarms

    bars2 = ax2.bar(categories, false_alarm_rate, color=['#FF3B30', '#FF9500', '#007AFF', '#34C759'], width=0.5)
    ax2.set_ylim(0, 60)
    ax2.set_title("False Alarm Suppression Rate (%)", fontweight="bold", fontsize=11, color="white", pad=10)
    ax2.grid(axis='y', color="#1E293B", linestyle="--")
    ax2.tick_params(axis='x', rotation=15)
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, f"{yval:.1f}%", ha='center', va='bottom', color="white", fontsize=9, fontweight="bold")

    plt.tight_layout()
    plt.savefig(f"{BASE_DIR}/charts/retrieval_benchmark.png", dpi=200, bbox_inches="tight")
    plt.close()

def create_architecture_diagram():
    """Generates visual 3-plane architecture diagram."""
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
    ax.axis('off')

    # Planes setup
    planes = [
        {"title": "ANALYST PLANE", "desc": "Interactive GIS Map • Temporal Timeline • Evidence Dossier Export • Audit Log", "y": 0.75, "color": AZURE_BRIGHT},
        {"title": "INTELLIGENCE PLANE", "desc": "Multimodal Embeddings • Spatial Indexing • Temporal Trajectory • False-Alarm Suppression", "y": 0.45, "color": AZURE_MAIN},
        {"title": "DATA PLANE", "desc": "Sentinel-2 / EO Imagery • GeoTIFF Ingestion • Cloud Masking • STAC Catalog & Postgres", "y": 0.15, "color": "#0B84FE"}
    ]

    for p in planes:
        # Draw plane card box
        rect = patches.FancyBboxPatch((0.05, p["y"] - 0.1), 0.9, 0.2, boxstyle="round,pad=0.03",
                                     facecolor=BG_CARD, edgecolor=p["color"], linewidth=2)
        ax.add_patch(rect)

        # Text inside plane box
        ax.text(0.08, p["y"] + 0.04, p["title"], color=p["color"], fontsize=12, fontweight="bold", va="center")
        ax.text(0.08, p["y"] - 0.03, p["desc"], color=TEXT_WHITE, fontsize=10, va="center")

    # Arrows between planes
    ax.annotate("", xy=(0.5, 0.65), xytext=(0.5, 0.55), arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=AZURE_BRIGHT, lw=2.5))
    ax.annotate("", xy=(0.5, 0.35), xytext=(0.5, 0.25), arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=AZURE_BRIGHT, lw=2.5))

    ax.text(0.53, 0.60, "Bi-directional Intelligence Flow", color=TEXT_MUTED, fontsize=9, va="center")
    ax.text(0.53, 0.30, "Normalized Ingestion & Feature Extraction", color=TEXT_MUTED, fontsize=9, va="center")

    plt.tight_layout()
    plt.savefig(f"{BASE_DIR}/diagrams/3_plane_architecture.png", dpi=200, bbox_inches="tight")
    plt.close()

def create_false_alarm_funnel():
    """Generates false alarm suppression pipeline diagram."""
    fig, ax = plt.subplots(figsize=(9, 5), dpi=200)
    ax.axis('off')

    stages = [
        ("Raw Pixel Differences", "100% Signal candidate noise", "#FF3B30", 0.85),
        ("Cloud & Quality Masking", "Filters cloud cover & shadows", "#FF9500", 0.70),
        ("Spatial Alignment & Ortho", "Sub-pixel geometric co-registration", "#007AFF", 0.55),
        ("Seasonal / Phenology Filter", "Eliminates agricultural & cyclic variation", "#0B84FE", 0.40),
        ("Temporal Persistence Engine", "Confirms multi-observation structural shift", "#34C759", 0.25)
    ]

    y = 0.82
    for title, desc, color, width in stages:
        x_left = 0.5 - width/2
        rect = patches.FancyBboxPatch((x_left, y - 0.06), width, 0.12, boxstyle="round,pad=0.02",
                                     facecolor=BG_CARD, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(0.5, y + 0.01, title, color="white", fontsize=10, fontweight="bold", ha="center")
        ax.text(0.5, y - 0.03, desc, color=TEXT_MUTED, fontsize=8.5, ha="center")

        # Arrow down if not last
        if y > 0.3:
            ax.annotate("", xy=(0.5, y - 0.08), xytext=(0.5, y - 0.06),
                        arrowprops=dict(arrowstyle="->", color=AZURE_BRIGHT, lw=2))
        y -= 0.16

    ax.text(0.5, 0.04, "VERIFIED HIGH-CONFIDENCE GEOSPATIAL INTELLIGENCE EVENT",
            color=AZURE_BRIGHT, fontsize=10, fontweight="bold", ha="center",
            bbox=dict(boxstyle="round,pad=0.5", facecolor=BG_CARD, edgecolor=AZURE_BRIGHT, lw=2))

    plt.tight_layout()
    plt.savefig(f"{BASE_DIR}/diagrams/false_alarm_funnel.png", dpi=200, bbox_inches="tight")
    plt.close()

def create_ui_mock():
    """Generates mock UI screenshot of the Analyst Workstation."""
    w, h = 1000, 600
    img = Image.new("RGB", (w, h), color="#0B1120")
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([0, 0, w, 50], fill="#0F172A", outline="#1E293B")
    draw.text((20, 15), "SIH 26227 | OFF-GRID SATELLITE INTELLIGENCE WORKSTATION", fill="#00D2FF")
    draw.rectangle([780, 10, 980, 40], fill="#007AFF")
    draw.text((795, 20), "EXPORT EVIDENCE DOSSIER", fill="#FFFFFF")

    # Left Panel - Search & Filters
    draw.rectangle([10, 60, 280, 580], fill="#0F172A", outline="#1E293B")
    draw.text((25, 75), "NATURAL LANGUAGE SEARCH", fill="#94A3B8")
    draw.rectangle([20, 100, 270, 140], fill="#1E293B", outline="#007AFF")
    draw.text((30, 112), '"New construction near river"', fill="#FFFFFF")

    draw.text((25, 160), "RETRIEVED CANDIDATES", fill="#94A3B8")

    # Candidate items
    candidates = [
        ("AOI-43QKB Sector 7", "Confidence: 96.4%", "Onset: Sep 2022"),
        ("AOI-43QKB Sector 12", "Confidence: 88.2%", "Onset: Nov 2023"),
        ("AOI-42RND Sector 3", "Confidence: 84.0%", "Onset: Jan 2024")
    ]
    y_c = 190
    for title, conf, onset in candidates:
        draw.rectangle([20, y_c, 270, y_c + 60], fill="#1E293B", outline="#007AFF" if "96.4" in conf else "#334155")
        draw.text((30, y_c + 8), title, fill="#FFFFFF")
        draw.text((30, y_c + 32), f"{conf} | {onset}", fill="#00D2FF" if "96.4" in conf else "#94A3B8")
        y_c += 70

    # Main Center - Map / Satellite View
    draw.rectangle([290, 60, 710, 420], fill="#152033", outline="#007AFF", width=2)

    # Insert mini satellite preview if available
    try:
        sat_img = Image.open(f"{BASE_DIR}/satellite/change_mask.png").resize((416, 356))
        img.paste(sat_img, (292, 62))
    except Exception as e:
        draw.text((320, 220), "[ MAPLIBRE GL SATELLITE CANVAS ]", fill="#00D2FF")

    # Bottom Panel - Temporal Timeline
    draw.rectangle([290, 430, 710, 580], fill="#0F172A", outline="#1E293B")
    draw.text((305, 440), "MULTI-TEMPORAL SPECTRAL TRAJECTORY (2020 - 2025)", fill="#94A3B8")
    try:
        chart_img = Image.open(f"{BASE_DIR}/charts/temporal_trajectory.png").resize((410, 115))
        img.paste(chart_img, (295, 460))
    except Exception:
        pass

    # Right Panel - Intelligence Dossier & Provenance
    draw.rectangle([720, 60, 990, 580], fill="#0F172A", outline="#1E293B")
    draw.text((735, 75), "EVIDENCE PROVENANCE", fill="#00D2FF")

    prov_text = [
        "Satellite: Sentinel-2A/B",
        "Tile ID: T43QKB_20240415",
        "Spatial Res: 10m Ground",
        "Bands: B02, B03, B04, B08",
        "Processing: Ortho + Mask",
        "Confidence: 96.4% High",
        "Change Type: Industrial",
        "False Alarm: Suppressed",
        "Audit Hash: 8f9a2d...e41",
        "Air-Gap Status: Local"
    ]
    y_p = 105
    for line in prov_text:
        draw.text((735, y_p), f"• {line}", fill="#FFFFFF" if "Confidence" in line or "Air-Gap" in line else "#94A3B8")
        y_p += 22

    img.save(f"{BASE_DIR}/ui/analyst_workstation_mock.png")

if __name__ == "__main__":
    print("Generating presentation visual assets...")
    create_satellite_imagery()
    create_temporal_chart()
    create_retrieval_benchmark_chart()
    create_architecture_diagram()
    create_false_alarm_funnel()
    create_ui_mock()
    print("All visual assets successfully generated in SIH_PPT/assets!")
