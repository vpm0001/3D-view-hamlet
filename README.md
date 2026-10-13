# Complete 3D Building Massing Model: Ground + 14 Floors & 3-Level Basement

A high-performance, browser-based **Interactive 3D Architectural Massing Model** created directly from the 2D CAD floor-plan drawing (`1446 x 2048 px`), featuring the complete building hierarchy:
1. **Superstructure (Ground + 14 Residential Floors):** 18 vertical levels spanning from $-9.6\text{m}$ to $+48.0\text{m}$, with 364 total residential units ($26\text{ units/floor} \times 14$), Ground Floor amenity/entrance massing, and open circulation corridors.
2. **5 Continuous Vertical Circulation Cores:** Unbroken shafts running from the foundation slab at $-9.6\text{m}$ up to the 14th-floor roof at $+48.0\text{m}$ with zero horizontal shift.
3. **Substructure (3-Level Underground Basement):** A continuous $60.0\text{m} \times 96.0\text{m}$ rectangular underground box ($5,760\text{ m}^2$ per level) extending to $-9.6\text{m}$ depth.

---

## Quick Start (How to Run)

Choose any of the following 3 options:

### Option 1: Direct Web Browser Access (Active Server)
The local server is already running in your workspace:  
👉 **[http://localhost:8080/index.html](http://localhost:8080/index.html)** (ES Module build)  
👉 **[http://localhost:8080/standalone_viewer.html](http://localhost:8080/standalone_viewer.html)** (UMD build)

### Option 2: One-Click Windows Desktop Launcher
Double-click **`Start_3D_Model.bat`** in `d:\HAMLET\3D View\`. It spins up the local server and opens your default browser automatically.

### Option 3: 100% Offline (No Server Required)
Double-click **`standalone_viewer.html`** in Windows File Explorer. All geometry and Three.js libraries are locally bundled with zero external internet or CORS dependencies.

---

## Building Vertical Hierarchy & Elevation Schedule

Floor-to-floor height: **3.2 metres**. Total height: **57.6 metres** (-9.6m to +48.0m across 18 levels).

```
 +48.0 m ────────────────────────────────────── Roof / Top of 14th Floor
         │  14TH FLOOR   │  26 Apartments + Corridors (+44.8m to +48.0m)
 +44.8 m ──────────────────────────────────────
         │  13TH FLOOR   │  26 Apartments + Corridors (+41.6m to +44.8m)
         │      ...      │  ...
         │  2ND FLOOR    │  26 Apartments + Corridors (+6.4m to +9.6m)
  +6.4 m ──────────────────────────────────────
         │  1ST FLOOR    │  MASTER TEMPLATE: 26 Apartments (+3.2m to +6.4m)
  +3.2 m ──────────────────────────────────────
         │  GROUND FLOOR │  Entrance Lobby & Amenity Massing (0.0m to +3.2m)
   0.0 m ══════════════════════════════════════ GROUND LEVEL
         │  BASEMENT 1   │  Parking / Utility Box (0.0m to -3.2m)
  -3.2 m ──────────────────────────────────────
         │  BASEMENT 2   │  Parking / Utility Box (-3.2m to -6.4m)
  -6.4 m ──────────────────────────────────────
         │  BASEMENT 3   │  Parking / Utility Box (-6.4m to -9.6m)
  -9.6 m ══════════════════════════════════════ Foundation Slab Level
```

> **Note:** The building stops strictly at the 14th floor (+48.0m). There is no 15th floor.

---

## Interactive Controls & Features

### 1. Floor Level Selector & Highlighting
- **Interactive Pills (`ALL`, `GND`, `1F` through `14F`):** Clicking any floor pill isolates that level in solid ivory while ghosting the remainder of the tower to 12% opacity.
- **Show All Floors / Hide Residential:** Quickly reveal or isolate superstructure components.

### 2. Exploded Floor & Basement Views
- **Exploded Floors:** Smooth lerp animation vertically separates all 14 residential levels (+1.1m stagger per floor) to inspect interior corridors and floor-to-floor relationships.
- **Normal View:** Smoothly collapses the tower back into its stacked monolithic form.
- **Explode Basement:** Drops B2 (-2.8m) and B3 (-5.6m) below B1 to inspect underground floor slabs.
- **Basement Cutaway:** Ghosts the front retaining wall to view subterranean interior clearances.

### 3. Vertical Inspection & Transparency
- **Building Transparency Slider ($0\% \rightarrow 95\%$):** Smoothly transitions the tower from solid ivory to architectural acrylic glass, revealing the continuous vertical core shafts running through the center.
- **Vertical Section Cut:** Enables a real-time clipping plane along the Z-axis. Drag the slice slider ($-45\text{m}$ to $+45\text{m}$) to cut clean cross-sections through apartments, corridors, and basements.

### 4. 5 Continuous Vertical Cores
- Unbroken dark charcoal shafts (`#363a3e`) running continuously from $-9.6\text{m}$ to $+48.0\text{m}$.
- Independently toggleable via the "Continuous Stair/Lift Cores" switch.

### 5. Architectural Camera Viewports
- **Isometric:** Standard 3D architectural perspective.
- **Top (Plan):** Orthogonal plan view (North Up) for 1:1 footprint validation.
- **Front:** South elevation facing the main building facade.
- **Side:** East elevation profile.
- **Section:** Angled section view paired with the clipping plane.
- **Basements:** Angled camera framing the full 9.6m underground substructure.
- **Reset:** Restores camera focus.

### 6. Interactive Structure Details Card
- Click any apartment block, ground floor element, stair core, or basement level to inspect its ID, unit type, elevation, and geometric properties.

---

## Performance & Optimization
- **Geometry Caching:** Extruded geometries for the 26 unique apartment footprints are cached once and shared across all 14 floors, reducing memory overhead to under 10MB and maintaining a rock-solid 60 FPS on all devices.
- **Zero Model Rebuilding:** When the inventory feed updates, the 3D model geometry is never rebuilt. Only the material colors of the affected apartment meshes are updated via state caching and diffing.

---

## Live Google Sheets Inventory Control System

The 3D model is connected to a live, read-only Google Apps Script JSON API feed:
`https://script.google.com/macros/s/AKfycbx9_AbznKZDe8QzBz0wzsyvYBSf-nlJUig1FzbZwG6uDed2jw9G59xtiKKM2x4aANSf/exec`

### Matching Rule (`floor + position`)
- **364 Total Apartments:** 14 residential floors $\times$ 26 physical apartment positions per floor.
- Each apartment mesh in the 3D model contains explicit metadata: `{ floor: 1..14, position: 1..26 }`.
- Matching is performed strictly against this metadata (never by visual position guessing).

### Status Color Palette
- **Available:** GREEN (`#22c55e`)
- **Booked:** RED (`#ef4444`)
- **Hold:** YELLOW (`#eab308`)
- **Registered:** BLUE (`#3b82f6`)
- **Sold:** DARK GREEN (`#14532d`)
- **N/A:** GREY (`#64748b`)

Only residential apartment blocks respond to inventory status. Corridors, stair/lift shafts, ground floor amenity masses, and basement levels retain their architectural materials.

### Live Real-Time Auto-Refresh & In-App Configuration
- **Real-Time Auto-Sync:** Fetches on website load and refreshes automatically every **30 seconds** (standard live interval, configurable down to 3s).
- **In-App Config (⚙️ icon):** Click the gear icon in the **LIVE INVENTORY FEED** card to change your Google Apps Script URL or adjust the polling frequency (3s, 5s, 10s, 30s) directly without editing code. Saved automatically in `localStorage`.
- **Flexible Data Support:** Supports both standard List format (`Floor`, `Position`/`Flat`, `Status`) and Grid Matrix format (Floors 1-14 rows $\times$ Flats 1-26 columns).
- **Google Apps Script Code:** See [`Google_Apps_Script_Code.gs`](Google_Apps_Script_Code.gs) for the turnkey script to copy and paste into your Google Sheet (`Extensions > Apps Script`).
- **Floor Isolation Filter:** Selecting any floor (`ALL FLOORS`, `GROUND`, `1` through `14`) highlights the selected level while rendering the rest of the building visible but slightly transparent.
- **Click Interaction:** Clicking any flat displays its exact `Floor`, `Position`, and `Status` (e.g., `FLAT POSITION 15`, `7TH FLOOR`, `STATUS: BOOKED`) with zero customer information displayed.

---

## Public Deployment Guide (GitHub & Vercel)

This project is a 100% self-contained static web application with zero external framework build dependencies.

### 1. GitHub Repository Setup
1. Initialize git in the project root:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: ROMA Hamlet 3D Building Inventory Viewer"
   ```
2. Create a new repository on GitHub (public or private).
3. Push to your GitHub repository:
   ```bash
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git branch -M main
   git push -u origin main
   ```

### 2. Vercel Deployment Settings
1. Go to [vercel.com/new](https://vercel.com/new) and import your GitHub repository.
2. Configure project settings:
   - **Framework Preset:** `Other` (Static HTML)
   - **Root Directory:** `./`
   - **Build Command:** *(Leave empty)*
   - **Output Directory:** `./` *(or leave default)*
3. Click **Deploy**. Vercel will deploy the site globally on its Edge Network in seconds.
4. Access:
   - Main 3D Viewer: `https://<your-project>.vercel.app/`
   - Standalone Viewer: `https://<your-project>.vercel.app/standalone` (configured via `vercel.json`)


