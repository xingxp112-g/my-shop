# 美妆内部销售系统 — 设计系统 v1.0

> 设计方向：轻奢美妆品牌，参考 Glossier / SK-II 官网质感
> 关键词：克制、细腻、留白、温润

---

## 1. 色彩体系

### 主色（Rose Gold）

| Token | Hex | RGB | 用途 |
|-------|-----|-----|------|
| `--color-primary` | `#C4845A` | 196, 132, 90 | 主按钮背景、关键操作、价格高亮、active 状态 |
| `--color-primary-light` | `#D9A882` | 217, 168, 130 | 主按钮 hover 态、渐变终点 |
| `--color-primary-dark` | `#A8694A` | 168, 105, 74 | 主按钮 active/pressed 态 |
| `--color-primary-muted` | `#F0D5C5` | 240, 213, 197 | 标签底色、轻度强调背景 |

### 辅色（Pearl White + Champagne）

| Token | Hex | RGB | 用途 |
|-------|-----|-----|------|
| `--color-accent` | `#E8C9A8` | 232, 201, 168 | 装饰线、卡片内分割线、次要强调 |
| `--color-gold` | `#BFA080` | 191, 160, 128 | 品牌名称、Logo 配色、高光细节 |

### 背景色

| Token | Hex | 用途 |
|-------|-----|------|
| `--color-bg-base` | `#FDFAF8` | 全局页面底色（带微暖调的近白） |
| `--color-bg-warm` | `#F5EDE8` | 内容区块背景、卡片悬浮背景、Hero 区 |
| `--color-bg-section` | `#FAF6F3` | 区块间分隔背景（alternating section） |
| `--color-bg-overlay` | `rgba(196,132,90,0.06)` | 鼠标 hover 时卡片背景叠加层 |

### 文字色

| Token | Hex | 用途 |
|-------|-----|------|
| `--color-text-primary` | `#2C2320` | 标题、商品名、重要信息（极深暖棕，非纯黑） |
| `--color-text-secondary` | `#6B5E58` | 副标题、品牌名称、描述文字 |
| `--color-text-muted` | `#A89690` | 占位符、时间戳、辅助说明 |
| `--color-text-on-primary` | `#FDFAF8` | 主色背景上的文字 |
| `--color-text-link` | `#C4845A` | 链接、可点击文字 |

### 边框色

| Token | Hex | 用途 |
|-------|-----|------|
| `--color-border-light` | `#EDE3DC` | 卡片边框、输入框默认边框 |
| `--color-border-medium` | `#D9CBBE` | 分割线、表格边框 |
| `--color-border-focus` | `#C4845A` | 输入框 focus 边框 |

### 状态色

| Token | Hex | 用途 |
|-------|-----|------|
| `--color-success` | `#7BAF8A` | 成功提示、已完成状态（柔和绿） |
| `--color-success-bg` | `#EEF5F0` | 成功状态背景 |
| `--color-warning` | `#C9935A` | 待处理状态（与主色同色调的橙） |
| `--color-warning-bg` | `#FBF2EA` | 待处理状态背景 |
| `--color-danger` | `#B86A6A` | 错误、已取消状态（柔和红） |
| `--color-danger-bg` | `#F7EDED` | 错误状态背景 |
| `--color-info` | `#7A9BB5` | 已确认状态（柔和蓝） |
| `--color-info-bg` | `#EEF3F8` | 已确认状态背景 |

### 阴影

| Token | 值 | 用途 |
|-------|-----|------|
| `--shadow-xs` | `0 1px 2px rgba(44,35,32,0.05)` | 极细微投影，输入框 |
| `--shadow-sm` | `0 2px 8px rgba(44,35,32,0.07)` | 卡片默认阴影 |
| `--shadow-md` | `0 4px 16px rgba(44,35,32,0.10)` | 卡片 hover 阴影 |
| `--shadow-lg` | `0 8px 32px rgba(44,35,32,0.12)` | 弹窗、抽屉 |
| `--shadow-nav` | `0 1px 0 #EDE3DC` | 导航栏底部线条阴影 |

---

## 2. 字体系统

### 字体选择

```css
/* Google Fonts 引入（头部 <link> 标签） */
/* 标题字体：Cormorant Garamond — 衬线字体，来自奢侈品排版传统，细腻优雅 */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

:root {
  --font-display: 'Cormorant Garamond', 'SimSun', serif;   /* 标题、品牌名、数字金额 */
  --font-body: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif; /* 正文、UI文字 */
}
```

**选型说明：**
- `Cormorant Garamond`：纤细衬线，极具轻奢感，用于大标题、价格展示、品牌名，对标 Glossier / Chanel 官网字体风格
- `Noto Sans SC`：中文无衬线，清晰易读，中文界面正文首选

### 字号阶梯

| Token | 值 | 对应 Tailwind | 用途 |
|-------|-----|---------------|------|
| `--text-xs` | `11px` | `text-xs` | 时间戳、状态角标、法律说明 |
| `--text-sm` | `13px` | `text-sm` | 辅助说明、标签文字、表格内容 |
| `--text-base` | `15px` | `text-base` | 正文段落、表单标签、卡片描述 |
| `--text-lg` | `17px` | `text-lg` | 商品名称、卡片主标题 |
| `--text-xl` | `20px` | `text-xl` | 页面区块标题、弹窗标题 |
| `--text-2xl` | `26px` | `text-2xl` | 页面大标题、统计数字 |
| `--text-3xl` | `34px` | `text-3xl` | Hero 标题（display 字体） |

### 字重

| Token | 值 | 用途 |
|-------|-----|------|
| `--weight-light` | `300` | 大标题装饰用（display 字体搭配） |
| `--weight-regular` | `400` | 正文默认 |
| `--weight-medium` | `500` | 强调文字、按钮、标签 |
| `--weight-bold` | `700` | 价格金额、关键指标数字 |

### 行高与字间距

```css
:root {
  /* 行高 */
  --leading-tight: 1.25;    /* 标题，避免行间过宽 */
  --leading-normal: 1.6;    /* 正文，舒适阅读 */
  --leading-relaxed: 1.8;   /* 长描述文字 */

  /* 字间距 */
  --tracking-tight: -0.02em;   /* 大号标题，视觉收紧 */
  --tracking-normal: 0;         /* 正文 */
  --tracking-wide: 0.08em;      /* 全大写标签、按钮文字（中文不建议使用） */
  --tracking-widest: 0.15em;    /* 导航品牌名、装饰性英文 */
}
```

---

## 3. 间距系统

基础单位：`4px`

| Token | 值 | Tailwind | 用途 |
|-------|-----|----------|------|
| `--space-1` | `4px` | `p-1 / m-1` | 图标内边距、微间距 |
| `--space-2` | `8px` | `p-2 / m-2` | 标签内边距、相邻元素间距 |
| `--space-3` | `12px` | `p-3 / m-3` | 小卡片内边距、输入框竖向padding |
| `--space-4` | `16px` | `p-4 / m-4` | 标准内边距、卡片内部水平间距 |
| `--space-6` | `24px` | `p-6 / m-6` | 卡片内边距（主要使用值）、区块内小间距 |
| `--space-8` | `32px` | `p-8 / m-8` | 区块间距、导航高度padding |
| `--space-12` | `48px` | `p-12 / m-12` | 页面大区块间距 |
| `--space-16` | `64px` | `p-16 / m-16` | Hero 区垂直padding、页面顶部留白 |

**使用原则：**
- 卡片内边距统一用 `24px`（移动端降为 `16px`）
- 相邻卡片 gap 用 `16px`（移动端）/ `24px`（PC端）
- 页面横向 padding：移动端 `16px`，PC端 `32px`，最大宽度容器内自动居中

---

## 4. 组件规范

### 4.1 按钮

#### 主按钮（Primary Button）
```
背景色：#C4845A
文字色：#FDFAF8
字体：Noto Sans SC, 500, 14px
字间距：0.06em
内边距：12px 28px（高度约 44px）
圆角：4px（克制，不做胶囊形）
边框：none
阴影：0 2px 8px rgba(196,132,90,0.30)

hover：background → #D9A882，阴影加深 → 0 4px 12px rgba(196,132,90,0.40)，translateY(-1px)
active/pressed：background → #A8694A，translateY(0)，scale(0.98)
disabled：opacity: 0.45，cursor: not-allowed
transition：all 200ms cubic-bezier(0.4, 0, 0.2, 1)
```

#### 次按钮（Secondary Button）
```
背景色：transparent
文字色：#C4845A
字体：Noto Sans SC, 500, 14px
内边距：11px 28px
圆角：4px
边框：1.5px solid #C4845A
阴影：none

hover：background → #F0D5C5，border-color 保持
active：background → #E8C9A8
disabled：opacity: 0.45
transition：all 200ms cubic-bezier(0.4, 0, 0.2, 1)
```

#### 文字按钮（Text Button / Ghost）
```
背景色：transparent
文字色：#C4845A
字体：Noto Sans SC, 400, 14px
内边距：8px 4px
边框：none
下划线：none（默认），hover 时出现 underline

hover：color → #A8694A，underline
active：color → #A8694A
transition：color 150ms ease
```

#### 危险按钮（Danger Button）
```
背景色：#B86A6A
文字色：#FDFAF8
其余同主按钮规范，阴影用 rgba(184,106,106,0.30)
```

#### 尺寸变体
```
sm：padding 8px 18px，font-size 12px，height ~36px
md：padding 12px 28px，font-size 14px，height ~44px（默认）
lg：padding 16px 36px，font-size 16px，height ~52px
```

---

### 4.2 卡片（Card）

#### 商品卡片（H5 前台）
```
背景色：#FFFFFF
边框：1px solid #EDE3DC
圆角：8px
阴影：0 2px 8px rgba(44,35,32,0.07)
内边距：0（图片无边距） + 内容区 16px

hover：
  - translateY(-4px)
  - 阴影 → 0 8px 24px rgba(44,35,32,0.12)
  - border-color → #D9CBBE
  - transition：all 250ms cubic-bezier(0.4, 0, 0.2, 1)

图片区：
  - aspect-ratio: 1 / 1（正方形）
  - object-fit: cover
  - border-radius: 8px 8px 0 0
  - overflow: hidden

内容区：padding 12px 16px 16px
```

#### 管理后台卡片（统计数据、表单容器）
```
背景色：#FFFFFF
边框：1px solid #EDE3DC
圆角：6px
阴影：0 1px 4px rgba(44,35,32,0.06)
内边距：24px
```

---

### 4.3 标签（Tag / Badge）

#### 商品标签（筛选/展示用）
```
背景色：#F0D5C5
文字色：#A8694A
字体：12px，500
内边距：4px 10px
圆角：3px
边框：none

选中态：background → #C4845A，color → #FDFAF8
hover：background → #E8C9A8
```

#### 订单状态徽章（Status Badge）
```
字体：11px，500
内边距：3px 8px
圆角：3px
border：1px solid（同色系，透明度20%）

待处理：bg #FBF2EA，color #C9935A，border rgba(201,147,90,0.25)
已确认：bg #EEF3F8，color #7A9BB5，border rgba(122,155,181,0.25)
已完成：bg #EEF5F0，color #7BAF8A，border rgba(123,175,138,0.25)
已取消：bg #F7EDED，color #B86A6A，border rgba(184,106,106,0.25)
```

---

### 4.4 输入框（Input）

```
高度：44px（移动端）/ 40px（PC后台）
背景色：#FFFFFF
边框：1.5px solid #EDE3DC
圆角：4px
字体：15px，Noto Sans SC，color #2C2320
内边距：0 14px
阴影：0 1px 2px rgba(44,35,32,0.04)

placeholder：color #A89690

focus：
  - border-color → #C4845A
  - box-shadow → 0 0 0 3px rgba(196,132,90,0.12)
  - outline: none

error：
  - border-color → #B86A6A
  - box-shadow → 0 0 0 3px rgba(184,106,106,0.10)

disabled：
  - background → #F5EDE8
  - color → #A89690
  - cursor: not-allowed

transition：border-color 200ms ease, box-shadow 200ms ease

select 同上，追加：
  - appearance: none
  - background-image：自定义下拉箭头（玫瑰金色 SVG）
  - padding-right: 36px

textarea：
  - min-height: 100px
  - resize: vertical
  - line-height: 1.6
```

---

### 4.5 导航栏（Navbar）

#### H5 前台导航
```
高度：56px（含 safe-area-inset-top）
背景色：rgba(253,250,248,0.92)
backdrop-filter：blur(12px) saturate(180%)
底部边框：1px solid #EDE3DC
阴影：0 1px 0 #EDE3DC
position：sticky top-0
z-index：100

Logo/品牌名：
  - 字体：Cormorant Garamond，24px，400
  - 颜色：#2C2320
  - letter-spacing: 0.1em

购物车图标区：
  - 徽章背景：#C4845A，文字 #FDFAF8，圆形，最小宽 18px，字号 11px
```

#### 后台管理侧边栏
```
宽度：220px（展开）/ 64px（收起）
背景色：#2C2320
文字色：rgba(253,250,248,0.75)
分割线：rgba(253,250,248,0.08)

active 菜单项：
  - background：rgba(196,132,90,0.18)
  - color：#F0D5C5
  - left border：3px solid #C4845A

hover 菜单项：
  - background：rgba(253,250,248,0.06)
  - color：#FDFAF8

Logo 区高度：64px
```

#### 后台顶部 Topbar
```
高度：56px
背景色：#FFFFFF
底部边框：1px solid #EDE3DC
阴影：0 1px 0 #EDE3DC
```

---

### 4.6 表格（Table，后台管理用）

```
表头：
  - background：#FAF6F3
  - color：#6B5E58
  - font-size：12px，500
  - padding：12px 16px
  - border-bottom：1.5px solid #EDE3DC

表格行：
  - background：#FFFFFF
  - padding：14px 16px
  - border-bottom：1px solid #F2EAE5

  hover：background → #FAF6F3

  transition：background 150ms ease

文字截断：商品名最多显示2行（-webkit-line-clamp: 2）
```

---

### 4.7 弹窗/确认框（Modal）

```
Overlay：background rgba(44,35,32,0.40)，backdrop-filter blur(2px)
容器：
  - background：#FFFFFF
  - border-radius：8px
  - padding：32px
  - box-shadow：0 16px 48px rgba(44,35,32,0.18)
  - max-width：480px（确认框）/ 640px（表单弹窗）

标题：text-xl，font-display，color #2C2320
副标题/描述：text-sm，color #6B5E58
底部按钮区：margin-top 28px，flex，gap 12px，justify-end

动效：
  - 进场：opacity 0→1 + scale 0.95→1，200ms ease-out
  - 出场：opacity 1→0 + scale 1→0.95，150ms ease-in
```

---

## 5. 动效规范

### 过渡时间

| Token | 值 | 用途 |
|-------|-----|------|
| `--duration-fast` | `150ms` | 颜色变化、hover 色彩过渡、文字按钮 |
| `--duration-normal` | `250ms` | 卡片 hover 上浮、输入框 focus、按钮状态切换 |
| `--duration-slow` | `400ms` | 页面元素入场、侧边栏展开收起、弹窗动画 |

### 缓动函数

```css
:root {
  --ease-out: cubic-bezier(0.4, 0, 0.2, 1);      /* 标准 Material ease，通用 */
  --ease-in-out: cubic-bezier(0.4, 0, 0.6, 1);   /* 侧边栏、弹窗等大范围位移 */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1); /* 轻弹簧感，卡片上浮、按钮点击反馈 */
  --ease-linear: linear;                          /* 进度条、loading 动画 */
}
```

### 具体动效定义

#### 页面加载 — 卡片交错淡入（Staggered Fade-Up）
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 每张卡片延迟 = index * 60ms，最多10张后不再增加延迟 */
.card-item {
  animation: fadeInUp 400ms var(--ease-out) both;
  animation-delay: calc(var(--card-index, 0) * 60ms);
}
```

#### Hover — 卡片上浮
```css
.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(44, 35, 32, 0.12);
  transition: transform 250ms var(--ease-spring),
              box-shadow 250ms var(--ease-out);
}
```

#### 按钮点击 — 轻微缩放反馈
```css
.btn:active {
  transform: scale(0.97);
  transition: transform 100ms var(--ease-out);
}
```

#### 图片懒加载 — 模糊渐入
```css
@keyframes imgReveal {
  from { opacity: 0; filter: blur(8px); transform: scale(1.03); }
  to   { opacity: 1; filter: blur(0);   transform: scale(1); }
}

.product-img.loaded {
  animation: imgReveal 400ms var(--ease-out) both;
}
```

#### 页面切换（H5 多页）
```css
/* 新页面进场 */
@keyframes pageEnter {
  from { opacity: 0; transform: translateX(16px); }
  to   { opacity: 1; transform: translateX(0); }
}

body {
  animation: pageEnter 300ms var(--ease-out) both;
}
```

#### 购物车角标弹动
```css
@keyframes badgePop {
  0%   { transform: scale(1); }
  40%  { transform: scale(1.4); }
  70%  { transform: scale(0.9); }
  100% { transform: scale(1); }
}

.cart-badge.updated {
  animation: badgePop 300ms var(--ease-spring);
}
```

#### Skeleton 骨架屏（加载占位）
```css
@keyframes shimmer {
  0%   { background-position: -400px 0; }
  100% { background-position: 400px 0; }
}

.skeleton {
  background: linear-gradient(90deg, #F0E8E3 25%, #FAF6F3 50%, #F0E8E3 75%);
  background-size: 800px 100%;
  animation: shimmer 1.4s var(--ease-linear) infinite;
  border-radius: 4px;
}
```

---

## 6. 布局规范

### 最大宽度

| 场景 | 值 | 说明 |
|------|-----|------|
| H5 前台 | `max-width: 480px` | 手机端居中，超出截断 |
| 后台管理 | `max-width: 1440px` | 宽屏限制，居中显示 |
| 后台内容区（去掉侧边栏后）| 自然撑满 | 侧边栏 220px，内容区 `calc(100vw - 220px)` |

### 响应式断点

```css
/* 遵循 Tailwind 默认断点 */
/* sm */  @media (min-width: 640px)  { ... }
/* md */  @media (min-width: 768px)  { ... }
/* lg */  @media (min-width: 1024px) { ... }
/* xl */  @media (min-width: 1280px) { ... }
```

### H5 前台列数

| 断点 | 商品列表列数 | gap |
|------|-------------|-----|
| `< 640px`（手机） | 2 列 | 12px |
| `>= 640px`（平板竖屏） | 3 列 | 16px |
| `>= 768px`（平板横屏）| 4 列 | 20px |

### 后台管理列数

| 页面 | 布局描述 |
|------|----------|
| 统计首页 | 4列统计卡片（lg:4，md:2，sm:1） |
| 商品列表 | 全宽表格 |
| 品牌/标签列表 | 全宽表格 |
| 订单列表 | 全宽表格 |
| 商品表单 | 单列，最大宽 720px，居中 |

### 页面内边距

```
H5 前台：
  - 页面横向 padding：px-4（16px，移动端）
  - 内容区顶部 padding：pt-4（navbar 高度 56px，需 padding-top 补偿）

后台管理内容区：
  - 内边距：p-6（24px，标准页面）
  - 紧凑页面（表格）：p-0（外容器无padding，表格自带内边距）
  - 区块间 margin-bottom：24px
```

### 后台管理页面结构

```
┌────────────────────────────────────────────────┐
│  Topbar（56px，全宽，sticky）                    │
├──────────┬─────────────────────────────────────┤
│          │                                     │
│ Sidebar  │  Content Area                       │
│ 220px    │  padding: 24px                      │
│ sticky   │  max-height: calc(100vh - 56px)     │
│          │  overflow-y: auto                   │
│          │                                     │
└──────────┴─────────────────────────────────────┘
```

---

## 附录 A：CSS 自定义属性汇总

将以下变量放入 `frontend/h5/css/custom.css` 和 `frontend/admin/css/custom.css` 的 `:root`：

```css
:root {
  /* ── 主色 ── */
  --color-primary:        #C4845A;
  --color-primary-light:  #D9A882;
  --color-primary-dark:   #A8694A;
  --color-primary-muted:  #F0D5C5;
  --color-accent:         #E8C9A8;
  --color-gold:           #BFA080;

  /* ── 背景 ── */
  --color-bg-base:        #FDFAF8;
  --color-bg-warm:        #F5EDE8;
  --color-bg-section:     #FAF6F3;
  --color-bg-overlay:     rgba(196,132,90,0.06);

  /* ── 文字 ── */
  --color-text-primary:   #2C2320;
  --color-text-secondary: #6B5E58;
  --color-text-muted:     #A89690;
  --color-text-on-primary:#FDFAF8;
  --color-text-link:      #C4845A;

  /* ── 边框 ── */
  --color-border-light:   #EDE3DC;
  --color-border-medium:  #D9CBBE;
  --color-border-focus:   #C4845A;

  /* ── 状态 ── */
  --color-success:        #7BAF8A;
  --color-success-bg:     #EEF5F0;
  --color-warning:        #C9935A;
  --color-warning-bg:     #FBF2EA;
  --color-danger:         #B86A6A;
  --color-danger-bg:      #F7EDED;
  --color-info:           #7A9BB5;
  --color-info-bg:        #EEF3F8;

  /* ── 阴影 ── */
  --shadow-xs:  0 1px 2px rgba(44,35,32,0.05);
  --shadow-sm:  0 2px 8px rgba(44,35,32,0.07);
  --shadow-md:  0 4px 16px rgba(44,35,32,0.10);
  --shadow-lg:  0 8px 32px rgba(44,35,32,0.12);
  --shadow-nav: 0 1px 0 #EDE3DC;

  /* ── 字体 ── */
  --font-display: 'Cormorant Garamond', 'SimSun', serif;
  --font-body:    'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;

  /* ── 过渡 ── */
  --duration-fast:   150ms;
  --duration-normal: 250ms;
  --duration-slow:   400ms;
  --ease-out:        cubic-bezier(0.4, 0, 0.2, 1);
  --ease-in-out:     cubic-bezier(0.4, 0, 0.6, 1);
  --ease-spring:     cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

---

## 附录 B：Google Fonts 引入代码

```html
<!-- 放在所有 HTML 页面的 <head> 顶部（link rel=preconnect 先） -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
```

---

*设计系统版本：v1.0 | 创建日期：2026-03-04 | 项目：美妆内部销售系统*
