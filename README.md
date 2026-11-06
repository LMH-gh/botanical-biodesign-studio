# Hark Botanical Biodesign Studio · 植物仿生时装设计参考库

**植物形态与服装工程的中英双语参考工作台。当前页面载入 251 个主题、1,010 个可切换视图；仓库包含 1,899 个 WebP 文件。**

**A bilingual reference studio for botanical morphology and garment engineering. The current page loads 251 themes and 1,010 selectable views; the repository contains 1,899 WebP files.**

> **视觉资产严正声明（Non-Commercial & No-AI-Training Notice）**
>
> 本仓库的前端代码采用 **MIT License** 开源；但仓库及关联图库中的所有**植物仿生服装图像资产**受独立的专有许可条款保护：**仅供个人学习、生物设计（Biodesign）学术研究与审美参考，严禁任何形式的商业使用，且严禁用于训练、微调（LoRA / DreamBooth / Fine-tuning）任何人工智能或机器学习模型，严禁纳入任何数据集或自动化爬虫抓取。**

## 当前仓库内容 | Current Repository Snapshot

下表来自当前 `public/data/catalog.json`、页面内嵌条目与实际文件清单，不代表尚未收录的完整规划库。JSON 目录有 250 条记录；页面使用 11 个内嵌条目，再补入 ID 不重复的 JSON 记录，最终显示 251 个主题。10 个同 ID 条目以页面内嵌版本为准，另有内嵌条目 `LG-B008`。

The table below reflects the checked-in `public/data/catalog.json`, embedded entries, and files, not the larger planned collection. The JSON catalog has 250 records. The page starts with 11 embedded entries and appends JSON records with new IDs, resulting in 251 themes. Embedded versions take precedence for 10 matching IDs; `LG-B008` is an additional embedded entry.

| 类别 / Category | 主题 / Themes | 可切换视图 / Views |
| ----- | -----: | -----: |
| 高定礼服 / Haute Couture | 20 | 105 |
| 日常矩阵 / Casual Matrix | 9 | 45 |
| 生境成衣 / Habitat Study | 91 | 91 |
| 结构内衣 / Intimate Structure | 4 | 8 |
| 度假泳装 / Resortwear | 127 | 761 |
| **运行时合计 / Runtime total** | **251** | **1,010** |

当前页面共 239 个不同 `taxonKey`。`public/assets/` 含 1,899 个 WebP 文件，约 94.4 MiB：目录关联 1,007 张预览图，另有 892 张缩略图。页面内嵌视图使用 data URI，不计入 WebP 文件数。原始 PNG 未提交到仓库。

The current page contains 239 distinct `taxonKey` values. `public/assets/` contains 1,899 WebP files (about 94.4 MiB): 1,007 catalog-linked previews and 892 thumbnails. Embedded views use data URIs and are not included in the WebP file count. Raw PNG sources are not committed.

## 功能 | Features

- 中英文界面切换；按类别、植物演化类群、形态器官、关键词和编号筛选。
- Switch the full interface between Chinese and English; filter by garment category, botanical clade, morphology, keywords, or ID.
- 在卡片与详情窗口中切换可用视图；支持收藏和双列对比。
- Switch available views in cards and detail dialogs; save favorites and compare two entries side by side.
- 当前数据类别包括高定礼服、日常矩阵、生境成衣、结构内衣与度假泳装；数据量随目录文件更新。
- Current categories are couture, casual matrix, habitat study, intimate structure, and resortwear. Counts follow the checked-in catalog.

## 本地预览 | Local Preview

页面通过 `fetch()` 加载目录，请使用本地 HTTP 服务，不要直接以 `file://` 打开：

The page loads its catalog with `fetch()`. Serve it over HTTP instead of opening it with `file://`:

```powershell
py -m http.server 5199
```

然后访问 `http://localhost:5199/`。构建脚本 `build_biodesign_assets.py` 可从你自己的源图目录生成 WebP 与目录文件；原始源图不包含在本仓库中。

Then open `http://localhost:5199/`. The `build_biodesign_assets.py` script can generate WebP files and a catalog from your own source-image directory; those source images are not included here.

## 许可与发布说明 | Licensing and Publishing

代码按 MIT License 发布；视觉资产受 [LICENSE-ASSETS.md](LICENSE-ASSETS.md) 中的非商业与禁止 AI 训练条款约束。

Code is released under the MIT License. Visual assets are subject to the non-commercial and no-AI-training terms in [LICENSE-ASSETS.md](LICENSE-ASSETS.md).

GitHub Pages 由 `.github/workflows/deploy.yml` 构建和发布。`robots.txt` 表达爬虫访问请求；GitHub Pages 不会把 `_headers` 文件解释为 HTTP 响应头配置，因此不能据此保证 `X-Robots-Tag` 响应头已生效。

GitHub Pages is built and deployed by `.github/workflows/deploy.yml`. `robots.txt` states crawler preferences. GitHub Pages does not interpret `_headers` as HTTP response-header configuration, so the file alone does not guarantee that an `X-Robots-Tag` header is served.