# Botanical Biodesign Reference Studio · 植物仿生时装参考库

**植物形态与服装工程的中英双语参考工作台。当前目录收录 89 个主题、410 个可切换视图，包含 645 个 WebP 文件（约 26.1 MiB）。**

**A bilingual reference studio for botanical morphology and garment engineering. The current catalog contains 89 themes and 410 selectable views, with 645 WebP files (about 26.1 MiB).**

## 当前目录 | Current Catalog

以下数量来自当前目录文件。未收录的已下载原图保留在本地临时目录，不计入网站。

Counts below come from the checked-in catalog. Downloaded images that were not selected remain outside the website.

| 类别 / Category | 主题 / Themes | 可切换视图 / Views |
| ----- | -----: | -----: |
| 高定礼服 / Haute Couture | 20 | 105 |
| 日常矩阵 / Casual Matrix | 9 | 45 |
| 生境成衣 / Habitat Study | 20 | 20 |
| 结构内衣 / Intimate Structure | 20 | 120 |
| 度假泳装 / Resortwear | 20 | 120 |
| **合计 / Total** | **89** | **410** |

图片资产均来自植物灵感主题。原始 PNG 不包含在仓库中；页面底部有图片来源说明与邀请链接。

All catalog entries use botanical inspiration. Original PNG files are not included in the repository. The page footer contains the image-source note and invitation link.

## 网站 | Website

[打开植物仿生时装参考库](https://lmh-gh.github.io/botanical-biodesign-studio/)

## 功能 | Features

- 中英文界面切换；按类别、植物类群、形态结构、关键词和编号筛选。
- Switch between Chinese and English; filter by garment category, botanical clade, morphology, keyword, or ID.
- 在卡片和详情窗口中切换视图；支持收藏和双列对比。
- Switch views in cards and detail dialogs; save favorites and compare entries side by side.
- 当前数据类别包括高定礼服、日常矩阵、生境成衣、结构内衣与度假泳装。
- Current categories are haute couture, casual matrix, habitat study, intimate structure, and resortwear.

## 本地预览 | Local Preview

页面通过 `fetch()` 加载目录，请通过本地 HTTP 服务打开：

The page loads its catalog with `fetch()`. Serve it over local HTTP:

```powershell
py -m http.server 5199
```

然后访问 `http://localhost:5199/`。构建脚本 `build_biodesign_assets.py` 可从源图目录生成 WebP 与目录文件。

Then open `http://localhost:5199/`. The `build_biodesign_assets.py` script generates WebP assets and the catalog from a source-image directory.

## 许可与发布 | Licensing and Publishing

代码按 MIT License 发布；图片受 [LICENSE-ASSETS.md](LICENSE-ASSETS.md) 中的非商业和禁止 AI 训练条款约束。

Code is released under the MIT License. Images are subject to the non-commercial and no-AI-training terms in [LICENSE-ASSETS.md](LICENSE-ASSETS.md).

GitHub Pages 由 `.github/workflows/deploy.yml` 构建与发布。GitHub Pages 不会把 `_headers` 用作 HTTP 响应头配置，因此不能据此保证 `X-Robots-Tag` 已生效。

GitHub Pages is built and published by `.github/workflows/deploy.yml`. GitHub Pages does not apply `_headers` as HTTP response-header configuration, so this file alone does not guarantee an `X-Robots-Tag` header.
