#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hark Botanical Biodesign Studio — Asset ETL, WebP Transcoder & Catalog Builder
==============================================================================
功能说明：
1. 纯植物白名单清洗：遍历 5 个源目录（自动跳过非植物文件夹 hark-bikini2），
   严格剔除所有视频 (.mp4/.mov)、技能规范文档 (.md/.json/.txt)、压缩包 (.zip)、
   4K 超分母图 (_FINAL_)、废稿 (_弃用/_R1/_R2) 以及真菌/地衣/动物/矿物/器物目录。
2. 同源植物跨品类关联（Taxon ID Mapping）：自动将同一植物物种（如银杏、龟背竹、
   百岁兰、捕蝇草、迎春花等）在高定礼服、日常成衣、仿生内衣与花卉泳装四个维度的资产关联。
3. WebP 降采样与反训练元数据注入：将原图批量转换为高质量 WebP 预览图与列表缩略图，
   并在图片 EXIF/XMP 中写入 Non-Commercial & No-AI-Training 版权声明。
4. 自动生成前端检索索引 `public/data/catalog.json`、防 AI 爬虫 `public/robots.txt`
   与 `public/_headers`。

运行方式：
  python3 build_biodesign_assets.py --source-root ./drive_sources --out-dir ./public
"""

from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

try:
    from PIL import Image, ImageDraw
except ImportError:
    raise SystemExit("请先安装 Pillow: pip3 install Pillow")

# ==============================================================================
# 1. 植物学白名单与非植物剔除规则 (761 个纯植物/藻类主题)
# ==============================================================================

GOWN_ALLOWED_L_NUMBERS: Set[int] = (
    set(range(5, 206))          # L05 - L205 (201 个直属植物)
    | set(range(206, 224))      # S1 花粉与硅藻 (18 个)
    | set(range(230, 236))      # S1 显微植物种子 (6 个)
    | set(range(236, 256))      # S2 食虫植物 (20 个)
    | set(range(256, 280))      # S3 种子传播机制 (24 个)
    | set(range(302, 325, 2))   # S5 花与传粉者中的植物花部 (12 个偶数编号)
    | set(range(326, 350))      # S6 银杏二十四节气物候 (24 个)
    | set(range(350, 368))      # S7 蕨类、石松与苔藓 (18 个)
    | set(range(726, 732))      # S14 荒漠植物前段 (仙人掌/生石花/龙舌兰/沙漠玫瑰花/仙人球/百岁兰)
    | set(range(738, 744))      # S14 荒漠植物后段 (胡杨/骆驼刺/复苏草/椰枣棕榈/梭梭/麻黄)
)

GOWN_PINYIN_NAME_MAP: Dict[int, Tuple[str, str]] = {
    738: ("胡杨", "Populus euphratica"),
    739: ("骆驼刺", "Alhagi camelorum"),
    740: ("复苏草", "Selaginella lepidophylla"),
    741: ("椰枣棕榈", "Phoenix dactylifera"),
    742: ("梭梭", "Haloxylon ammodendron"),
    743: ("麻黄", "Ephedra sinica"),
}

CASUAL_MATRIX_EXCLUDED_FUNGI_NUMS: Set[int] = {
    3, 4, 11, 18, 21, 24, 29, 39, 47, 49, 52,
}

EXCLUDED_NON_PLANT_KEYWORDS: Tuple[str, ...] = (
    "石蕊", "松萝", "肉杯菌", "马勃", "鹅膏", "毒蝇", "小菇", "地星",
    "云芝", "猴头菇", "银耳", "木耳", "绣球菌", "竹荪", "鬼笔", "笼头菌",
    "灵芝", "鸡油菌", "鬼伞", "乳菇", "枝瑚菌", "地衣", "梅衣", "地图衣",
    "发网菌", "粉瘤菌", "绒泡菌", "羊肚菌", "毛杯菌", "扇菇", "蜜环菌",
    "裂褶菌", "腊蘑", "侧耳", "珠与纱", "F77", "翡翠夜宴",
    "衣内千年", "器物有灵", "园林六境",
    "usnea", "lichen", "sarcoscypha", "calvatia", "amanita", "mycena",
    "geastrum", "trametes", "hericium", "tremella", "auricularia", "sparassis",
    "morchella", "cookeina", "coprinus", "panellus", "omphalotus", "schizophyllum",
    "ganoderma", "lactarius", "laccaria", "cantharellus", "cladonia", "pleurotus",
)

GYMNOSPERM_KEYWORDS = ("银杏", "苏铁", "百岁兰", "南洋杉", "松", "柏", "杉", "麻黄", "ginkgo", "cycas", "welwitschia", "araucaria", "ephedra", "taxodium", "pinus", "cedrus", "abies", "juniperus", "sequoiadendron")
PTERIDOPHYTE_KEYWORDS = ("蕨", "桫椤", "满江红", "问荆", "石松", "卷柏", "复活草", "复苏草", "蘋", "紫萁", "贯众", "equisetum", "azolla", "selaginella", "adiantum", "platycerium", "cyathea", "alsophila")
BRYOPHYTE_KEYWORDS = ("藓", "地钱", "角苔", "sphagnum", "polytrichum", "funaria")
ALGAE_KEYWORDS = ("藻", "角叉菜", "kelp", "macrocystis", "chondrus", "volvox", "acetabularia", "fucus", "codium", "padina", "caulerpa", "chara")

COPYRIGHT_NOTICE = (
    "Copyright (c) 2026 Hark Botanical Biodesign Studio. "
    "Non-Commercial Research & Reference Use Only. "
    "NO AI/ML MODEL TRAINING, NO LORA FINE-TUNING, NO DATASET SCRAPING ALLOWED. "
    "TDMRep: Reservation=1."
)


def classify_botanical_clade(name_zh: str, latin_hint: str = "") -> str:
    text = f"{name_zh} {latin_hint}".lower()
    if any(k in text for k in ALGAE_KEYWORDS):
        return "algae"
    if any(k in text for k in BRYOPHYTE_KEYWORDS):
        return "bryophyte"
    if any(k in text for k in PTERIDOPHYTE_KEYWORDS):
        return "pteridophyte"
    if any(k in text for k in GYMNOSPERM_KEYWORDS):
        return "gymnosperm"
    return "angiosperm"


def classify_morphological_organ(name_zh: str, series_code: str = "") -> str:
    if "花粉" in name_zh or "硅藻" in name_zh or "藻" in name_zh or series_code == "S1":
        return "micro_pollen"
    if any(k in name_zh for k in ("猪笼草", "瓶子草", "茅膏菜", "捕蝇草", "捕虫堇", "狸藻", "挖耳草", "土瓶草", "貉藻")) or series_code == "S2":
        return "carnivorous"
    if any(k in name_zh for k in ("种子", "翅果", "榆钱", "冠毛", "杨絮", "钩刺", "苍耳", "浆果", "蒴果", "喷瓜", "莲蓬", "椰子", "果", "稻", "菱", "酸浆")) or series_code == "S3":
        return "seed_dispersal"
    if any(k in name_zh for k in ("龟背", "银杏", "百岁兰", "苏铁", "问荆", "蕨", "满江红", "生石花", "仙人", "龙舌兰", "胡杨", "梭梭", "麻黄", "叶", "竹", "杉", "松", "柏")) or series_code in ("S6", "S7", "S14"):
        return "foliage_venation"
    return "floral_corolla"


def normalize_taxon_key(name_zh: str) -> str:
    cleaned = re.sub(r"^[A-Z]+\d+[-_\s]*", "", name_zh.strip())
    cleaned = re.sub(r"_时装片$", "", cleaned)
    cleaned = cleaned.split()[0]
    synonyms = {
        "亚马孙王莲": "王莲",
        "美洲龙舌兰": "龙舌兰",
        "大花卡特兰": "卡特兰",
        "罗氏兜兰": "兜兰",
        "白花蝴蝶兰": "蝴蝶兰",
        "蓝花西番莲": "西番莲",
        "广玉兰": "荷花玉兰",
        "锯叶班克木": "锯叶佛塔树",
        "细叶满江红": "满江红",
        "茉莉花": "茉莉",
        "立春冬芽": "银杏",
        "立秋": "银杏",
        "霜降": "银杏",
        "捕蝇草张开": "捕蝇草",
    }
    return synonyms.get(cleaned, cleaned)


def transcode_webp_with_protection(
    src_path: Path,
    preview_out: Path,
    thumb_out: Optional[Path] = None,
    add_subtle_watermark: bool = True,
) -> None:
    preview_out.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src_path) as im:
        im_rgb = im.convert("RGB")
        w, h = im_rgb.size
        if max(w, h) > 1376:
            scale = 1376.0 / max(w, h)
            im_rgb = im_rgb.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)

        if add_subtle_watermark and im_rgb.width >= 320:
            draw = ImageDraw.Draw(im_rgb)
            wm_text = "© Hark Biodesign · Non-Commercial · No AI Training"
            draw.text((12, im_rgb.height - 20), wm_text, fill=(220, 225, 220))

        exif = im_rgb.getexif()
        exif[0x010E] = "Hark Botanical Biodesign Reference Studio (Pure Plant Series)"
        exif[0x8298] = COPYRIGHT_NOTICE
        im_rgb.save(preview_out, format="WEBP", quality=82, method=6, exif=exif.tobytes())

        if thumb_out is not None:
            thumb_out.parent.mkdir(parents=True, exist_ok=True)
            tw = min(384, im_rgb.width)
            th = int(im_rgb.height * (tw / im_rgb.width))
            thumb_im = im_rgb.resize((tw, th), Image.Resampling.LANCZOS)
            thumb_im.save(thumb_out, format="WEBP", quality=76, method=6, exif=exif.tobytes())


def is_valid_image_file(path: Path) -> bool:
    if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        return False
    stem = path.stem
    excluded_tokens = ("_FINAL_", "_弃用", "_R1_", "_R2_", "抖音封面", "_record")
    return not any(tok in stem for tok in excluded_tokens)


def write_anti_scraping_configs(out_dir: Path) -> None:
    robots_txt = """# Hark Botanical Biodesign Studio — Anti-AI-Training & Anti-Scraping Policy
# All visual assets are strictly Non-Commercial and PROHIBITED from AI/ML model training.

User-agent: GPTBot
Disallow: /

User-agent: ChatGPT-User
Disallow: /

User-agent: OAI-SearchBot
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: anthropic-ai
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Claude-Web
Disallow: /

User-agent: Bytespider
Disallow: /

User-agent: ImagesiftBot
Disallow: /

User-agent: FacebookBot
Disallow: /

User-agent: Meta-ExternalAgent
Disallow: /

User-agent: Diffbot
Disallow: /

User-agent: omgili
Disallow: /

User-agent: PerplexityBot
Disallow: /

User-agent: Amazonbot
Disallow: /

User-agent: Applebot-Extended
Disallow: /

User-agent: *
Disallow: /assets/
"""
    headers_txt = """/*
  X-Robots-Tag: noai, noimageai
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin

/assets/*
  X-Robots-Tag: noindex, noai, noimageai
  Cache-Control: public, max-age=31536000, immutable
"""
    (out_dir / "robots.txt").write_text(robots_txt, encoding="utf-8")
    (out_dir / "_headers").write_text(headers_txt, encoding="utf-8")


def build_catalog(source_root: Path, out_dir: Path, dry_run: bool = False) -> Dict:
    entries: List[Dict] = []
    taxon_index: Dict[str, List[str]] = {}
    total_images_count = 0

    # 1. 高定礼服 (hark-礼服设计)
    gown_root = source_root / "hark-礼服设计"
    if gown_root.exists():
        for folder in sorted(gown_root.rglob("L*_*")):
            if not folder.is_dir():
                continue
            m = re.match(r"^L0*(\d+)_(.+)$", folder.name)
            if not m:
                continue
            l_num = int(m.group(1))
            if l_num not in GOWN_ALLOWED_L_NUMBERS:
                continue
            raw_name = m.group(2)
            name_zh, latin_name = GOWN_PINYIN_NAME_MAP.get(l_num, (raw_name, ""))
            series_code = folder.parent.name.split("_")[0] if folder.parent != gown_root else "L_SPECIES"
            item_id = f"HC-L{l_num:03d}"
            taxon_key = normalize_taxon_key(name_zh)

            views = []
            for img_path in sorted(folder.iterdir()):
                if not is_valid_image_file(img_path):
                    continue
                if re.match(r"^L0*\d+_(D[1-6]|sheet)\.(png|jpg)$", img_path.name, re.I):
                    view_key = "SHEET" if "sheet" in img_path.stem.lower() else img_path.stem.split("_")[-1].upper()
                    rel_webp = f"/assets/gown/{item_id}_{view_key}.webp"
                    rel_thumb = f"/assets/gown/thumbs/{item_id}_{view_key}.webp"
                    if not dry_run:
                        transcode_webp_with_protection(
                            img_path,
                            out_dir / rel_webp.lstrip("/"),
                            out_dir / rel_thumb.lstrip("/") if view_key in ("D1", "SHEET") else None,
                        )
                    views.append({"key": view_key, "preview": rel_webp, "thumb": rel_thumb})
                    total_images_count += 1

            if views:
                entries.append({
                    "id": item_id,
                    "code": f"L{l_num:03d}",
                    "taxonKey": taxon_key,
                    "name": {"zh": name_zh, "en": latin_name or f"Botanical Specimen L{l_num:03d}"},
                    "garmentLine": "gown",
                    "clade": classify_botanical_clade(name_zh, latin_name),
                    "organ": classify_morphological_organ(name_zh, series_code),
                    "series": series_code,
                    "extended": False,
                    "views": views,
                })
                taxon_index.setdefault(taxon_key, []).append(item_id)

    # 2. 日常休闲矩阵 (hark-休闲服设计)
    casual_root = source_root / "hark-休闲服设计"
    if casual_root.exists():
        for folder in sorted(casual_root.glob("C*-*")):
            if not folder.is_dir():
                continue
            m = re.match(r"^C0*(\d+)-(.+)$", folder.name)
            if not m:
                continue
            c_num = int(m.group(1))
            name_zh = m.group(2)
            if c_num in CASUAL_MATRIX_EXCLUDED_FUNGI_NUMS or any(k in name_zh for k in EXCLUDED_NON_PLANT_KEYWORDS):
                continue
            item_id = f"BC-M{c_num:03d}"
            taxon_key = normalize_taxon_key(name_zh)
            views = []
            latin_genus = ""
            for img_path in sorted(folder.iterdir()):
                if not is_valid_image_file(img_path):
                    continue
                dm = re.match(r"^C0*\d+_(D[1-6])(?:_VIBE)?_([a-zA-Z]+)\.png$", img_path.name)
                if dm:
                    v_key = "VIBE" if "_VIBE_" in img_path.name else dm.group(1)
                    latin_genus = dm.group(2).capitalize()
                    rel_webp = f"/assets/casual/{item_id}_{v_key}.webp"
                    rel_thumb = f"/assets/casual/thumbs/{item_id}_{v_key}.webp"
                    if not dry_run:
                        transcode_webp_with_protection(
                            img_path,
                            out_dir / rel_webp.lstrip("/"),
                            out_dir / rel_thumb.lstrip("/") if v_key in ("D1", "VIBE") else None,
                        )
                    views.append({"key": v_key, "preview": rel_webp, "thumb": rel_thumb})
                    total_images_count += 1
            if views:
                entries.append({
                    "id": item_id,
                    "code": f"C{c_num:02d}",
                    "taxonKey": taxon_key,
                    "name": {"zh": name_zh, "en": f"{latin_genus} BioCasual" if latin_genus else f"BioCasual C{c_num:02d}"},
                    "garmentLine": "casual_matrix",
                    "clade": classify_botanical_clade(name_zh, latin_genus),
                    "organ": classify_morphological_organ(name_zh),
                    "series": "OSC_3.0_BioCasual",
                    "extended": False,
                    "views": views,
                })
                taxon_index.setdefault(taxon_key, []).append(item_id)

    # 3. 植物实景同框成衣 (hark-设计)
    hab_root = source_root / "hark-设计"
    if hab_root.exists():
        for img_path in sorted(hab_root.glob("C*_final.png")):
            if not is_valid_image_file(img_path):
                continue
            m = re.match(r"^C0*(\d+)_([a-z_]+)_(.+)_final\.png$", img_path.name, re.I)
            if not m:
                continue
            c_num = int(m.group(1))
            genus = m.group(2)
            name_zh = m.group(3)
            if any(k in f"{name_zh} {genus}".lower() for k in EXCLUDED_NON_PLANT_KEYWORDS):
                continue
            item_id = f"BC-S{c_num:03d}"
            taxon_key = normalize_taxon_key(name_zh)
            rel_webp = f"/assets/habitat/{item_id}_FINAL.webp"
            rel_thumb = f"/assets/habitat/thumbs/{item_id}_FINAL.webp"
            if not dry_run:
                transcode_webp_with_protection(img_path, out_dir / rel_webp.lstrip("/"), out_dir / rel_thumb.lstrip("/"))
            total_images_count += 1
            entries.append({
                "id": item_id,
                "code": f"BC-S{c_num:03d}",
                "taxonKey": taxon_key,
                "name": {"zh": name_zh, "en": f"{genus.capitalize()} Habitat RTW"},
                "garmentLine": "casual_habitat",
                "clade": classify_botanical_clade(name_zh, genus),
                "organ": classify_morphological_organ(name_zh),
                "series": "Habitat_Hero_Detail",
                "extended": False,
                "views": [{"key": "FINAL", "preview": rel_webp, "thumb": rel_thumb}],
            })
            taxon_index.setdefault(taxon_key, []).append(item_id)

    # 4. 仿生内衣 (Hark-内衣)
    intimate_root = source_root / "Hark-内衣"
    if intimate_root.exists():
        idx = 1
        for folder in sorted(intimate_root.iterdir()):
            if not folder.is_dir() or any(k in folder.name for k in EXCLUDED_NON_PLANT_KEYWORDS):
                continue
            name_zh = folder.name
            taxon_key = normalize_taxon_key(name_zh)
            item_id = f"LG-B{idx:03d}"
            idx += 1
            views = []
            for img_path in sorted(folder.glob("*.png")):
                if not is_valid_image_file(img_path):
                    continue
                for suffix, label in (
                    ("_front.png", "FRONT"),
                    ("_back.png", "BACK"),
                    ("_left.png", "LEFT"),
                    ("_right.png", "RIGHT"),
                    ("_product.png", "PRODUCT"),
                    ("_hair_makeup_board.png", "BOARD"),
                ):
                    if img_path.name.endswith(suffix):
                        rel_webp = f"/assets/intimate/{item_id}_{label}.webp"
                        rel_thumb = f"/assets/intimate/thumbs/{item_id}_{label}.webp"
                        if not dry_run:
                            transcode_webp_with_protection(
                                img_path,
                                out_dir / rel_webp.lstrip("/"),
                                out_dir / rel_thumb.lstrip("/") if label in ("FRONT", "PRODUCT", "BOARD") else None,
                            )
                        views.append({"key": label, "preview": rel_webp, "thumb": rel_thumb})
                        total_images_count += 1
            if views:
                entries.append({
                    "id": item_id,
                    "code": item_id,
                    "taxonKey": taxon_key,
                    "name": {"zh": name_zh, "en": f"Botanical Intimate · {taxon_key}"},
                    "garmentLine": "intimate",
                    "clade": classify_botanical_clade(name_zh),
                    "organ": classify_morphological_organ(name_zh),
                    "series": "Botanical_Intimate",
                    "extended": True,
                    "views": views,
                })
                taxon_index.setdefault(taxon_key, []).append(item_id)

    # 5. 花卉泳装与外搭 (hark-bikini)
    resort_root = source_root / "hark-bikini"
    if resort_root.exists():
        for folder in sorted(resort_root.glob("BK*_*")):
            if not folder.is_dir():
                continue
            m = re.match(r"^BK0*(\d+)_(.+)$", folder.name)
            if not m:
                continue
            bk_num = int(m.group(1))
            name_zh = m.group(2)
            item_id = f"BK-FL{bk_num:03d}"
            taxon_key = normalize_taxon_key(name_zh)
            views = []
            for img_path in sorted(folder.glob("BK*_D[1-6].png")):
                v_key = img_path.stem.split("_")[-1].upper()
                rel_webp = f"/assets/resort/{item_id}_{v_key}.webp"
                rel_thumb = f"/assets/resort/thumbs/{item_id}_{v_key}.webp"
                if not dry_run:
                    transcode_webp_with_protection(
                        img_path,
                        out_dir / rel_webp.lstrip("/"),
                        out_dir / rel_thumb.lstrip("/") if v_key == "D1" else None,
                    )
                views.append({"key": v_key, "preview": rel_webp, "thumb": rel_thumb})
                total_images_count += 1
            if views:
                entries.append({
                    "id": item_id,
                    "code": f"BK{bk_num:03d}",
                    "taxonKey": taxon_key,
                    "name": {"zh": name_zh, "en": f"Botanical Resort BK{bk_num:03d}"},
                    "garmentLine": "resort",
                    "clade": classify_botanical_clade(name_zh),
                    "organ": classify_morphological_organ(name_zh),
                    "series": "Botanical_Resort_Bikini",
                    "extended": True,
                    "views": views,
                })
                taxon_index.setdefault(taxon_key, []).append(item_id)

    for entry in entries:
        siblings = [sid for sid in taxon_index.get(entry["taxonKey"], []) if sid != entry["id"]]
        entry["relatedIds"] = siblings

    catalog_payload = {
        "project": "Hark Botanical Biodesign Studio",
        "version": "1.0.0",
        "updatedAt": "2026-11-05",
        "license": {
            "code": "MIT",
            "assets": "Non-Commercial & No-AI-Training (Strict Prohibition on ML/LoRA Training & Scraping)",
            "tdmReservation": 1,
        },
        "counts": {
            "totalThemes": len(entries),
            "totalImages": total_images_count,
            "uniqueTaxa": len(taxon_index),
        },
        "items": entries,
    }
    data_dir = out_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "catalog.json").write_text(
        json.dumps(catalog_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_anti_scraping_configs(out_dir)
    return catalog_payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Hark Botanical Biodesign Studio assets and catalog.json")
    parser.add_argument("--source-root", type=Path, default=Path("./drive_sources"), help="Path containing the Google Drive folders")
    parser.add_argument("--out-dir", type=Path, default=Path("./public"), help="Output public directory for Vite/GitHub Pages")
    parser.add_argument("--dry-run", action="store_true", help="Only build catalog.json without WebP transcoding")
    args = parser.parse_args()

    result = build_catalog(args.source_root, args.out_dir, dry_run=args.dry_run)
    print(f"[DONE] Built Botanical Biodesign catalog: {result['counts']['totalThemes']} plant themes ({result['counts']['totalImages']} WebP images) across {result['counts']['uniqueTaxa']} unique taxa.")
    print(f"[DONE] Anti-AI-Training robots.txt, _headers, and EXIF policies generated in: {args.out_dir}")
