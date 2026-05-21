---
name: compose-overlay-text
type: producer
recommended_model: sonnet
subagent_safe: true
operator_facing: false
isolation_scope: brand_only
layer: production
version: 1.1.0
patch_notes_v2_87_4:
  - "1.1.0 (v2.87.4 canonical many-to-many enforcement mirror) · NEW HR-OT-CANON-1 mirror sibling compose-creative v1.8.0 · post-gen fix overlay text DOIT être appliqué sur asset dans `creatives/{CRT-NN}/produced/` (pas hors structure) · maintien entry canonical existing · update creative.json#overlay_fixes[] avec timestamp + fix_type + cross-ref operator validation. Closes audit Fincut v2.87.3 finding · fix overlays appliqués hors structure canonical = orphelins. Backward compat strict additif."
mode: proposed
reasoning_pattern: matrix-driven
triggers_fr:
  - "overlay logo crisp"
  - "compose post-gen text"
  - "fix wordmark régression"
  - "intégrer logo SVG sur visuel"
triggers_en:
  - "overlay crisp text"
  - "post-gen logo composite"
  - "fix wordmark regression"
  - "integrate SVG logo on visual"
permissions:
  reads: [brand, product, creative]
  writes: [creative]
  mode: proposed
  subagent_safe: true
  bash_allowlist:
    - "python3"
prerequisites:
  - field: brands/{slug}/products/{slug}/produced/{creative_id}.jpg
    level: L1
    auto_pull: read_creative_source
    freshness_ttl_days: 30
  - field: brands/{slug}/assets/logo.svg
    level: L1
    auto_pull: read_logo_canonical
    freshness_ttl_days: 365
  - field: brands/{slug}/products/{slug}/visual_identity.json
    level: L1
    auto_pull: read_visual_identity_v11
    freshness_ttl_days: 90
  - field: overlay_spec
    level: L2
    options:
      - logo_only
      - logo_and_sub_text
      - full_recompose
description: >
  Producer skill PIL post-gen composite logo SVG canonique + sub-text crisp avec accents francais
  preserves sur creative produit par compose-creative. Resout drift wordmark fal.ai + drop accents
  + sub-text flou. Validation wordmark_pattern regex post-composite.
disambiguates_against:
  compose-creative: "compose-creative genere le visuel via fal.ai. compose-overlay-text intervient APRES pour fix logo + sub-text avec PIL."
  recompose-creative: "recompose-creative cree variants (audience/platform/format). compose-overlay-text fixe la qualite d'un creative existant."
pipeline:
  preconditions: "creative_id.jpg existe dans brands/{slug}/products/{slug}/produced/. logo.svg present dans brands/{slug}/assets/ (F2 Agent parallel). visual_identity.json v1.1 avec logo_svg block + wordmark_pattern."
  postconditions: "creative_id-overlay-{timestamp}.jpg persiste. meta.overlay_applied true dans creative.json. wordmark_validation flag dans meta. validate-resources silencieux."
consumes:
  - path: brands/{slug}/products/{slug}/produced/{creative_id}.jpg
    min_version: 1.0.0
    note: source creative output compose-creative
  - path: brands/{slug}/assets/logo.svg
    min_version: 1.0.0
    note: logo canonique brand-level (F2 Agent parallel)
  - path: brands/{slug}/products/{slug}/visual_identity.json
    min_version: 1.1.0
    note: logo_svg block + wordmark_pattern regex (F1 Agent parallel)
  - path: resources/schemas/skill-prerequisites.schema.json
    min_version: 1.0.0
produces_proposals_for:
  - brands/{slug}/products/{slug}/produced/{creative_id}-overlay-{timestamp}.jpg
  - brands/{slug}/products/{slug}/produced/{creative_id}.json
patch_notes:
  v1.0.1: "v2.51 operator-fiche-output canonique template applied · footer + close refactor langage métier. Step 7 close drop `Wordmark canon valide` → `logo nickel et lisible` (langue opérateur, drop doctrine name leak `canon`). Drop menu `Next · tester live, ou adapter variants pour autre audience, ou refaire si tu vois un detail` → soft offer 1 ligne max · *Si tu veux, on peut la tester en live*. Cohérent template canonique resources/templates/operator-fiche-output.md footer rule (1 reco soft offer max, jamais menu, jamais nommer skill `recompose-creative` en surface)."
  v1.0.0: "v2.43 ship skill PIL post-gen composite resout 3 frictions runtime fal.ai (wordmark regression caractere par caractere, drop accents francais sub-text, badges trust flous). Composite logo SVG vectoriel via cairosvg + sub-text TrueType UTF-8 preserve. Validation wordmark_pattern regex OCR/SSIM. Complete compose-creative HR3.4 retry policy existing, ne remplace pas."
---

# Skill: compose-overlay-text

> **Composite post-gen logo SVG + sub-text crisp.** v1.0.0 · v2.43 · resout drift fal.ai wordmark + drop accents francais + sub-text flou. Pipe aval de compose-creative.

Producer post-gen, pas generateur. Lit (creative_id.jpg source, logo.svg canonique, visual_identity.json v1.1), applique composite PIL vectoriel + TrueType UTF-8 sur le rendu fal.ai existant, valide wordmark via regex post-composite, persiste version `-overlay-{timestamp}.jpg` + flag meta. Le mecanisme reste invisible operateur (pas de mention PIL, cairosvg, alpha channel, regex en surface). L'operateur voit un "fix logo precis" et un "rendu vectoriel SVG", c'est tout.

## Tone

Posture controle qualite senior + technique invisible. Pas inspecteur bavard, pas afficheur de plumbing. Output operateur en 4-6 lignes : composite reussi (avec preview), wordmark validation pass/fail, badges nets, next suggested. Aucun terme PIL, cairosvg, alpha channel, regex, OCR, SSIM en surface. Si validation echoue apres retry, surface honnete + flag pour gate operateur, jamais panique.

## Expert methodology

**Persona.** Senior digital craftsperson, post-prod creative agency, dix mille composites packaging cross-formats. Lit un visuel comme un retoucheur senior : detecte une regression caractere par caractere instantanement, sait que SVG vectoriel preserve scaling, sait que TrueType + UTF-8 = accents francais cristallins.

**Framework.** Composite vectoriel deterministe (SVG via cairosvg vers PNG vers PIL paste alpha-preserved) + TrueType rendering (Inter/Helvetica/Roboto avec full UTF-8 e e e a a u u c i i o oe ae) + validation regex post-composite. Complete compose-creative v1.1.0 HR3.4 retry policy existing (skill aval, pas substitut).

**Pattern position pipeline.** compose-creative genere (fal.ai HR3 + HR3.4 retry + HR3.5 crop). compose-overlay-text raffine MODIFIEURS post-gen (logo + sub-text + badges trust). Equation v3.1 NOYAU x CONTEXTE x MODIFIEURS, ce skill raffine couche MODIFIEURS uniquement. Source canon : `docs/system/compositional-cartography.md` v2.42.

---

## Step 0bis · Prerequisite check (DRGFP v2.38)

Avant composite (Step 1), scanner prerequisites :

1. L1 silent · `brands/{slug}/products/{slug}/produced/{creative_id}.jpg` (creative source compose-creative output existing). Si absent, refuse honnete + suggest compose-creative a run d'abord.
2. L1 silent · `brands/{slug}/assets/logo.svg` (canonique brand-level, F2 Agent parallel prerequis ship). Si absent, L3 degraded skip overlay logo + flag operateur gate upload source.
3. L1 silent · `brands/{slug}/products/{slug}/visual_identity.json` v1.1 (logo_svg block + wordmark_pattern regex, F1 Agent parallel). Si v1.0 only, L3 degraded fallback skip wordmark validation + flag confidence 0.6.
4. L2 gate operateur · `overlay_spec` choice (logo_only / logo_and_sub_text / full_recompose). Default suggested `logo_and_sub_text` si visual_identity.label.sub_label populated.

Output state map + confidence_chain[] init.

---

## HR1 · Inputs canon obligatoires

Avant composite, verifier :

- creative_id JPG existe dans `brands/{slug}/products/{slug}/produced/`.
- logo.svg existe dans `brands/{slug}/assets/` (F2 Agent parallel, prerequis ship).
- visual_identity.json v1.1 avec `logo_svg` block + `wordmark_pattern` regex.

Si manque :

- creative source absent → refuse bloquant + suggest compose-creative.
- logo.svg absent → L3 degraded, skip overlay logo, continue composite badges sub-text si applicable, flag operateur gate upload.
- visual_identity.json v1.0 only → L3 degraded, skip wordmark validation regex post-composite, fallback structural similarity SSIM uniquement, flag confidence 0.6.

---

## HR2 · PIL TrueType rendering accents francais

Pour sub-text overlay (badges trust, CTA, reassurance), utiliser PIL Pillow + TrueType font avec full UTF-8 support :

- Font privilegiee : Inter (Google Fonts open source) OU Helvetica OU Roboto.
- Path system fonts : `/System/Library/Fonts/` macOS OU `/usr/share/fonts/` Linux OU `C:\Windows\Fonts\` Windows. Skill detecte path runtime via fallback ladder.
- Accents preserves : e e e a a u u c i i o oe ae rendus character-by-character.
- Anti-pattern : jamais utiliser image text rendering basique qui drop accents (PIL default sans TrueType, ou ImageMagick basic).

Font_path detection runtime :

```python
import os
font_candidates = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/inter/Inter-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:\\Windows\\Fonts\\arial.ttf",
]
font_path = next((p for p in font_candidates if os.path.exists(p)), None)
if not font_path:
    # L3 degraded, flag operateur, suggest installer Inter/Helvetica
    raise FontNotFoundError("aucune font TrueType detectee, accents francais a risque")
```

---

## HR3 · SVG vectorielle composite via cairosvg

Logo SVG composite via cairosvg + PIL :

- Lire logo.svg path canonique (`brands/{slug}/assets/logo.svg`).
- Convertir SVG vers PNG via cairosvg (preserve vectorielle scalability, target_width = `creative_width * scale_pct`).
- PIL paste avec alpha channel (transparency preserved).
- Position canonique : bottom-right corner. Padding 24-48px edges (default 32px, configurable).
- Scale : 8-12% width creative total (default 10%, configurable selon density).

---

## HR4 · Wordmark validation post-composite

Apres composite, valider wordmark_pattern regex (visual_identity.json v1.1) sur region logo :

- Path 1 (preferred) · OCR region logo via pytesseract si dispo runtime. Match regex compile depuis `visual_identity.wordmark_pattern` (ex wordmark with brackets `^example\[brand\]$`).
- Path 2 (fallback) · structural similarity SSIM vs SVG source apres rasterize equivalente. Threshold `>=0.92` pass.

Si validation echoue (regex no-match OU SSIM < 0.92) :

1. Retry max 3x avec adjustments : scale +/-2%, position pad +/-8px, contrast adjustment +5% si dark bg detecte.
2. Si retry exhausted → flag `wordmark_validation_failed` dans creative.json meta + degrade graceful (sauve composite-attempted-{timestamp}.jpg + flag operateur gate).

---

## HR5 · Trust badges precision triangle

Si overlay_spec inclut sub-text trust badges (cas creative v2.43 typique cell-boost ANG-02) :

- 3 badges position triangle : left (x=0.15*w, y=0.85*h) · right (x=0.85*w, y=0.85*h) · top center (x=0.5*w, y=0.10*h).
- Badge size : 15% width creative each.
- Background : semi-transparent white `#FFFFFFAA` OU brand bordeaux `#6E1A1F` selon mode operateur (default `#FFFFFFAA`).
- Text : sans-serif bold (Inter Bold ou Helvetica Bold), accents preserves UTF-8, max 3 mots par badge, font_size auto-scale (base 24px a 1K resolution, scale lineaire pour 2K/4K).

---

## HR6 · Operator-facing translation

Output operateur ne doit JAMAIS exposer :

| Interne (NEVER surface) | Operateur (always surface) |
|---|---|
| PIL composite | fix logo precis post-gen |
| cairosvg | rendu vectoriel SVG |
| wordmark_pattern regex | validation wordmark canon |
| alpha channel | transparence |
| TrueType UTF-8 | accents francais cristallins |
| OCR pytesseract | lecture automatique logo |
| SSIM structural similarity | comparaison fidele image |
| paste / draw / bbox | composite / placement |
| font_path detection | police automatique |

Canon mappings full : `docs/system/operator-vocabulary-translation.md`.

---

## Steps

### Step 1 · Load PIL + cairosvg dependencies

```python
from PIL import Image, ImageDraw, ImageFont
import cairosvg
import io
```

Si imports fail (PIL OU cairosvg absent runtime) :

- L3 degraded · output operateur : "fix logo precis indisponible sur cette instance · creative source preserve · install requis cote operateur".
- Flag operateur gate avec instruction `pip install Pillow cairosvg` (suggest, jamais auto-install).

### Step 2 · SVG vers PNG conversion

```python
def svg_to_png(svg_path, target_width):
    png_bytes = cairosvg.svg2png(
        url=svg_path,
        output_width=target_width
    )
    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")
```

Target_width calcule depuis `creative_img.size[0] * scale_pct` (default scale_pct = 0.10).

### Step 3 · Composite logo

```python
def composite_logo(creative_img, logo_img, position="bottom-right", padding=32, scale_pct=0.10):
    width, height = creative_img.size
    logo_width = int(width * scale_pct)
    logo_resized = logo_img.resize((
        logo_width,
        int(logo_img.size[1] * logo_width / logo_img.size[0])
    ))

    if position == "bottom-right":
        x = width - logo_resized.size[0] - padding
        y = height - logo_resized.size[1] - padding
    elif position == "bottom-left":
        x = padding
        y = height - logo_resized.size[1] - padding
    elif position == "top-right":
        x = width - logo_resized.size[0] - padding
        y = padding
    else:
        x = padding
        y = padding

    creative_img.paste(logo_resized, (x, y), logo_resized)
    return creative_img
```

Canon position default : `bottom-right`. Configurable mais pas exposer field name a operateur (HR6).

### Step 4 · Composite sub-text badges (si applicable)

```python
def composite_badges(creative_img, badges_spec, font_path, font_size=24):
    draw = ImageDraw.Draw(creative_img)
    font = ImageFont.truetype(font_path, font_size)

    for badge in badges_spec:
        text = badge["text"]  # accents preserves via UTF-8
        position = badge["position"]
        bg_color = badge.get("bg_color", (255, 255, 255, 200))
        text_color = badge.get("text_color", (110, 26, 31, 255))  # bordeaux brand

        # Background pill
        bbox = draw.textbbox(position, text, font=font)
        padding = 12
        pill_bbox = (
            bbox[0] - padding,
            bbox[1] - padding,
            bbox[2] + padding,
            bbox[3] + padding
        )
        draw.rounded_rectangle(pill_bbox, radius=8, fill=bg_color)

        # Text
        draw.text(position, text, font=font, fill=text_color)

    return creative_img
```

Badges_spec format JSON :

```json
[
  {"text": "Livraison 48h", "position": [200, 1400]},
  {"text": "Garantie 100%", "position": [1100, 1400]},
  {"text": "Made in France", "position": [650, 200]}
]
```

Accents preserves character-by-character via PIL TrueType + UTF-8 default.

### Step 5 · Wordmark validation post-composite

```python
import re

def validate_wordmark(creative_overlay_img, wordmark_pattern, logo_region_bbox):
    pattern = re.compile(wordmark_pattern)

    # Path 1 (preferred) OCR pytesseract
    try:
        import pytesseract
        logo_crop = creative_overlay_img.crop(logo_region_bbox)
        text = pytesseract.image_to_string(logo_crop).strip()
        return bool(pattern.match(text))
    except ImportError:
        # Path 2 fallback SSIM
        from skimage.metrics import structural_similarity as ssim
        # SSIM vs logo SVG rasterize equivalente
        score = ssim(logo_crop_np, logo_svg_rasterize_np)
        return score >= 0.92
```

Si validation echoue, retry max 3x adjustments (scale / position / contrast). Si exhausted, flag `wordmark_validation_failed` meta + degrade graceful.

### Step 6 · Save output + meta update

Path output : `brands/{slug}/products/{slug}/produced/{creative_id}-overlay-{timestamp}.jpg`.

Timestamp format ISO 8601 compact : `2026-05-11T143052Z`.

Update `{creative_id}.json` meta via `write_to_context` (jamais Edit/Write JSON direct, mutation rule canon) :

```json
{
  "meta": {
    "overlay_applied": true,
    "overlay_applied_at": "2026-05-11T14:30:52Z",
    "overlay_spec": "logo_and_sub_text",
    "wordmark_validation_passed": true,
    "wordmark_validation_method": "ocr_regex",
    "overlay_file_path": "produced/{creative_id}-overlay-2026-05-11T143052Z.jpg",
    "_changelog": "v2.43 compose-overlay-text PIL composite applied"
  }
}
```

### Step 7 · No orphan output (canonique v2.51)

Operator-facing summary final (3-5 lignes max, HR6 translation applied, langue métier zéro jargon, soft offer 1 ligne) ·

- Composite reussi · pub source + version avec logo precis + sub-text accents crisp.
- Validation logo · `logo nickel et lisible` (préservé caractère par caractère) ou `à revoir` si validation echoue.
- Badges trust nets si applicable (preview operateur · `open {path}`).
- Footer · 1 soft offer 1 ligne max, jamais menu, jamais nommer skill (`recompose-creative`) en surface.

Format example ·

```
Logo précis appliqué en bas à droite. Logo nickel et lisible, préservé caractère par caractère. Badges accents français nets (Livraison 48h · Garantie 100% · Made in France).

Si tu veux, on peut la tester en live.
```

**Anti-pattern UX prose** · JAMAIS dire `Wordmark canon valide` (doctrine name leak), JAMAIS menu `Next · A, ou B, ou C`, JAMAIS nommer le skill `recompose-creative` en surface operator. Reformuler en langue métier accessible · *"logo nickel et lisible"*, *"préservé caractère par caractère"*, soft offer *"Si tu veux, on peut..."*.

---

## Anti-patterns

- Skip compose-overlay-text si compose-creative output deja "good enough" · risque drift permanent · toujours run skill validation sur creatives ship-ready.
- Composite logo base image bitmap (PNG raster) au lieu SVG vectorielle · perte qualite scaling, blur visible 2K/4K.
- Sub-text PIL avec font system default (peut drop accents) · toujours TrueType explicit avec UTF-8 verified.
- Position logo center top creative · concurrence visuelle packshot · canon = bottom-right (configurable mais default canon).
- Skip wordmark validation regex · pollution silencieuse si nano-banana-pro regression non detectee.
- Edit/Write direct sur creative.json meta · bypass mutation gate · toujours write_to_context (canon mutation rule).
- Exposer "PIL", "cairosvg", "alpha channel", "regex", "OCR", "SSIM" en output operateur · violation HR6, bug a corriger.

---

## Cross-refs

- `resources/schemas/visual_identity.schema.json` v1.1 (Agent F1 parallel · `assets_canonical` + `logo_svg` + `wordmark_pattern` fields).
- `brands/{slug}/assets/logo.svg` (Agent F2 parallel · source SVG canonique brand-level).
- `.skills/skills/compose-creative/SKILL.md` v1.1.0 · HR3.4 retry policy existing (compose-overlay-text complete, ne remplace pas).
- `.skills/skills/recompose-creative/SKILL.md` · variants adaptation (audience/platform/format), pas confondre.
- `docs/system/visual-identity-doctrine.md` (Agent F1 parallel · doctrine canon).
- `docs/system/compositional-cartography.md` v2.42 (equation v3.1 NOYAU x CONTEXTE x MODIFIEURS · compose-overlay-text raffine MODIFIEURS post-gen).
- `docs/system/operator-vocabulary-translation.md` (HR6 mappings canon).
- `docs/system/dependency-resolution-protocol.md` (DRGFP v2.38 · L1/L2/L3 prerequisite gap-filling).
- `resources/schemas/skill-prerequisites.schema.json` v1.0 (prerequisites array contract).
