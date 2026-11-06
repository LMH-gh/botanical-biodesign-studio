# Hark Botanical Biodesign Studio · 植物仿生时装设计参考库

**从植物解剖学、微观孢粉到四维时装工程的中英双语 Biodesign 开源参考工作台**

**A Bilingual Reference Studio Translating Botanical Morphology into Haute Couture, Ready-to-Wear, Intimate Structure & Resort Wear**

> **视觉资产严正声明（Non-Commercial & No-AI-Training Notice）**
>
> 本仓库的前端代码采用 **MIT License** 开源；但仓库及关联图库中的所有**植物仿生服装图像资产**受独立的专有许可条款保护：**仅供个人学习、生物设计（Biodesign）学术研究与审美参考，严禁任何形式的商业使用，且严禁用于训练、微调（LoRA / DreamBooth / Fine-tuning）任何人工智能或机器学习模型，严禁纳入任何数据集或自动化爬虫抓取。**

## 1. 项目概览与植物学资产规模

本项目源自系统化的植物形态学与时装结构转译实验，从逾 16,000 张原始生成图像中严格按植物分类学白名单（被子植物、裸子植物、蕨类与石松、苔藓植物、藻类植物）清洗筛选，剔除一切非植物主题（矿物、建筑、器物、真菌与动物）及过程废稿，最终收录 **761 个植物仿生主题单元、4,569 张标准规格视觉参考图**：

| 服装工程模块 | 收录主题数 | 图片总数 | 核心视图与规格构成 | 植物学覆盖范围与转译特征 | 
| ----- | ----- | ----- | ----- | ----- | 
| **高定雕塑礼服 (Haute Couture)** | 331 组 | 2,317 张 | 每组含 `D1`–`D6` 六个设计方向 (`768×1376`) + `Sheet` 六宫格总览图 (`1840×2180`) | 201 种直属植物 + 显微花粉与硅藻 (`S1`)、食虫植物捕虫笼 (`S2`)、果实与种子空气动力学 (`S3`)、传粉花冠机关 (`S5`)、银杏二十四节气物候 (`S6`)、蕨类与苔藓 (`S7`)、荒漠旱生植物 (`S14`) | 
| **日常休闲矩阵 (BioCasual Matrix)** | 74 组 | 444 张 | 每组含 `D1`–`D6` 六种版型与转译梯度 (`768×1376`) + 精选街拍 `VIBE` 图 | 涵盖银杏、巨藻、苏铁、问荆、百岁兰、龟背竹、捕蝇草、王莲、满江红等，探索 T 恤 + 短裙/短裤的 L0–L3 实穿转译 | 
| **植物实景同框成衣 (Habitat First-Frame)** | 121 组 | 370 张 | 定稿全身正视图 `_final` + 服装细节与真实植物生境同框微距首帧 `seg1`–`seg3` | 单一 Hero Detail 克制转译（如银杏二叉分叉百褶、水稻梯田阶梯下摆、鹿角蕨分叉贴袋） | 
| **植物结构内衣 (Botanical Intimate)** | 40 组 | 268 张 | `Front` / `Back` / `Left` / `Right` 四向秀场图 + `Product` 无头透明人台静物图 + `Board` 1:1 妆发设定板 | 将花瓣翻折、叶脉开窗、笼唇滚边转化为钢圈通道、定型纱罩杯分割与骨线结构（置于「显示扩展分类」开关下） | 
| **花卉度假泳装与外搭 (Botanical Resort)** | 195 组 | 1,170 张 | 每组含 `D1`–`D5` 五种泳装剪裁 + `D6` 同主题植物刺绣欧根纱防晒外搭衬衫 (`768×1376`) | 与高定礼服 `L05`–`L205` 物种 1:1 对应（从迎春花、铃兰到短尾铁线莲），展示同一植物在轻薄泳装与刺绣外搭中的形态映射 | 
| **全库合计 (Pure Botanical Total)** | **761 组** | **4,569 张** | WebP 降采样总体积 **\~480 MB**（单 GitHub 仓库直接托管） | **跨品类同物种关联逾 190 种植物**（支持一键横向对比同一植物在 4 类服装中的结构转译） | 

## 2. 核心功能与 Biodesign 三轴检索设计

1. **同源植物跨品类联动（Cross-Category Taxon Mapping）**：

   * 通过拉丁学名与中文正名锚点（`taxonKey`），将分布在不同服装模块的同一植物自动串联。例如点击 **「银杏 (*Ginkgo biloba*)」**，即可在同一抽屉内横向对比其 **二十四节气高定礼服（24 组）**、**二叉叶脉分叉褶日常短裙（D1–D6）** 与 **金扇二裂透明人台内衣（Product View）**。

2. **植物学三轴过滤系统**：

   * **按演化门纲筛选（Botanical Clade）**：被子植物、裸子植物、蕨类与石松、苔藓植物、藻类与硅藻。

   * **按仿生器官筛选（Morphological Organ）**：花冠与传粉机关、叶脉分叉与叶片开窗、捕虫笼与特化陷阱、果实与种子空气动力学、微米级花粉与藻壳。

   * **按服装品类与转译层级筛选（Garment Line）**：高定雕塑礼服、日常休闲矩阵、植物实景同框、仿生结构内衣（含透明人台纯服装图）、花卉度假泳装与刺绣外搭。

3. **卡片内多维视图丝滑切换**：

   * 列表卡片内置 `D1`–`D6`、`Sheet 六宫格`、`Product 透明人台`、`Board 妆发设定板` 独立切换圆点，悬停或点击小标签即可切换当前卡片视图。

## 3. 快速构建与本地运行

本仓库提供全自动 Python 清洗与索引构建脚本 `build_biodesign_assets.py`：

```
# 1. 安装依赖并运行纯植物白名单提取、WebP 降采样与防 AI 训练 EXIF 注入
pip3 install Pillow
python3 build_biodesign_assets.py --source-root ./drive_sources --out-dir ./public

# 2. 启动静态预览（或直接双击打开 hark_biodesign_studio.html）
npx vite --port 5199

```

## 4. 视觉资产专用许可协议（LICENSE-ASSETS.md）

本仓库采用**代码与视觉资产双轨许可（Dual Licensing）**：

* **前端与构建脚本代码（MIT License）**：仓库中的 `.html`、`.ts`、`.tsx`、`.py`、`.css` 源代码遵循 MIT 许可证开放使用。

* **服装视觉图像资产（Strict Non-Commercial & No-AI-Training License）**：

  1. **非商业使用限制（Non-Commercial Only）**：`public/assets/` 目录及在线画廊展示的所有植物仿生服装图像（含预览图、缩略图、人台图、六宫格拼图及妆发设定板）仅授权用于个人学习、教学演示与非商业学术研究。严禁用于任何商业服装生产、电商展示、商业广告、付费素材包打包转售或商业衍生品。

  2. **严禁 AI 模型训练与数据集抓取（No AI/ML Training, No LoRA, No Scraping）**：未经著作权人事先书面授权，**严禁将本项目的任何图像用于训练、微调（包括但不限于 LoRA、DreamBooth、ControlNet、Textual Inversion）、蒸馏、评估任何生成式人工智能或计算机视觉模型**；严禁通过爬虫、脚本批量下载本库图像用于构建公开或私有数据集。

  3. **技术保护措施声明（TDM Reservation）**：所有发布图像均已移除 4K 原始母图，并注入 W3C TDMRep (`Reservation=1`) 元数据及 `X-Robots-Tag: noai, noimageai` 响应头，任何移除水印或规避 `robots.txt` 的抓取行为均构成违约与侵权。