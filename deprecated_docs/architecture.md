# 架构设计文档: 凿壁

## 1. 引言
本文档基于 `docs/prd.md` (版本 1.2+) 中定义的产品需求，为“凿壁”项目设计系统架构，并提供技术选型和实施建议。目标是构建一个高性能、可维护、**以 Markdown 内容为核心** 的静态网站。

## 2. 架构目标
*   **高性能:** 快速的页面加载速度，优秀的 Core Web Vitals 指标。
*   **可维护性:** 清晰的代码结构，易于更新内容和迭代功能。
*   **可扩展性:** 能够方便地添加新文章和潜在的新功能模块。
*   **安全性:** 最大程度减少攻击面，因为主要交付的是静态文件。
*   **开发效率:** 利用现代工具链提高开发和内容管理效率。
*   **成本效益:** 优先考虑免费或低成本的托管和工具方案。

## 3. 架构模式选择
### 3.1 备选模式
1.  **静态网站生成器 (SSG) 模式:** 使用 Hugo, Astro, Eleventy 等工具，从Markdown等内容源文件构建纯静态HTML、CSS、JS文件。
2.  **带静态内容的单页应用 (SPA) 模式:** 使用 Vue/React 等框架构建应用外壳，客户端加载和渲染静态内容（如Markdown文件）。
3.  **纯静态 HTML/CSS/JS 手动编写模式:** 为每个页面手动创建HTML文件（当前项目似乎部分采用此方式）。

### 3.2 模式评估
*   **SSG模式:**
    *   **优点:** 性能极佳、SEO友好、安全性高、内容管理（Markdown）方便、与CDN结合良好。
    *   **缺点:** 需要构建步骤、纯静态限制了部分动态交互（需JS实现）。
    *   **适用性:** 非常适合内容驱动、对性能要求高的网站，与本项目需求高度契合。
*   **SPA模式:**
    *   **优点:** 可能提供更丰富的应用级交互、组件化开发。
    *   **缺点:** 初始加载可能较慢、SEO处理相对复杂、对于本项目可能引入不必要的复杂度。
    *   **适用性:** 更适合交互复杂的Web应用，而非内容展示为主的网站。
*   **纯静态手动模式:**
    *   **优点:** 初期简单，无构建依赖。
    *   **缺点:** 内容增长后极难维护、重复代码多、易出错、无法有效利用模板。
    *   **适用性:** 只适合极简单的微型网站，不适合本项目规模。

### 3.3 推荐模式
**静态网站生成器 (SSG) 模式** 是本项目的最佳选择。它完美契合了PRD中对性能、可维护性、内容管理和现代Web实践的要求。

## 4. 系统架构图 (高层)

```mermaid
graph LR
    subgraph "开发环境 (本地/CI)"
        A[Markdown 内容 (.md) <br> + YAML Frontmatter] --> B{SSG 引擎 (Astro)};
        C[布局/组件 (.astro)] --> B;
        D[样式 (Tailwind CSS)] --> B;
        E[客户端 JS (.js)] --> B;
        B --> F[构建过程 (npm run build)];
        F --> G[静态文件 (HTML, CSS, JS)];
    end

    subgraph "部署与访问"
        G --> H{静态 Web 托管 (GitHub Pages)};
        I[用户浏览器] --> H;
        J[CDN (外部库)] --> I;
        H -.-> I;
    end

    style B fill:#f9f,stroke:#333,stroke-width:2px
    style H fill:#ccf,stroke:#333,stroke-width:2px
```

**说明:**
1.  开发者在本地或使用工具（如LLM）编写/生成 **带有 YAML Frontmatter 的 Markdown 内容文件**，并与 Astro 组件/布局一起存储在项目中。
2.  使用 Astro 引擎（通过`npm run build`）读取 Markdown 内容集合，结合模板，生成最终的纯静态网站文件。
3.  静态文件部署到 GitHub Pages 或其他静态托管平台。
4.  用户浏览器直接访问托管平台上的静态文件。
5.  浏览器按需从 CDN 加载外部库（Tailwind, FontAwesome, Mermaid 等）。

## 5. 技术选型
*   **静态网站生成器 (SSG):** **Astro**
    *   *理由:* 现代、性能卓越（默认零JS）、组件模型灵活（支持多种UI框架或自带组件）、与Tailwind集成良好、社区活跃。相比Eleventy更面向未来组件化趋势。
*   **内容格式:** **Markdown (.md)** + **YAML Frontmatter** + **Astro Content Collections**
    *   *理由:* 简单易学、专注于内容编写、易于版本控制、被广泛的SSG支持。Frontmatter 用于存储元数据。**Astro Content Collections 提供类型安全和 Schema 验证，确保元数据一致性。**
*   **样式:** **Tailwind CSS**
    *   *理由:* 项目规则要求，现代化的Utility-First CSS框架，开发效率高，易于维护一致性。
*   **客户端交互:** **Vanilla JavaScript**
    *   *理由:* 对于主题切换、移动菜单、Mermaid初始化等简单交互，无需引入大型JS框架，保持轻量。Astro的架构也鼓励尽可能少的客户端JS。
*   **版本控制:** **Git**
    *   *理由:* 行业标准，项目已在使用。
*   **托管:** **GitHub Pages**
    *   *理由:* 免费、与GitHub仓库无缝集成、可通过GitHub Actions实现CI/CD自动化部署。

## 6. 核心组件职责
*   **内容集合 (`src/content/`):**
    *   存放所有 Markdown 格式的文章和页面内容。
    *   **使用 Astro Content Collections (`src/content/config.ts`) 定义 Schema 并进行类型安全的内容管理和查询。**
    *   Markdown 文件包含符合预定义 Schema 的 YAML Frontmatter 元数据。
*   **布局 (`src/layouts/`):**
    *   `Layout.astro`: 基础HTML骨架，包含`<head>`（引入CSS、JS、字体、元数据）、header、footer、以及内容插入槽 (`<slot/>`)。
    *   `ArticleLayout.astro`: 文章页面的特定布局，可能包含标题、日期显示、作者信息等结构。
*   **组件 (`src/components/`):**
    *   `Header.astro`: 网站头部，包含Logo、导航链接、主题切换按钮。处理响应式导航（移动端菜单）。
    *   `Footer.astro`: 网站页脚，包含版权和作者信息。
    *   `Card.astro`: 可重用的文章卡片组件，用于在首页或分类页展示文章摘要。接收文章数据作为`props`。
    *   `ThemeToggle.astro` / `ThemeToggle.js`: 主题切换按钮及其客户端逻辑。
    *   `MobileMenu.astro` / `MobileMenu.js`: 移动端菜单按钮及其客户端逻辑。
    *   `Mermaid.astro` (可选): 用于封装Mermaid图表渲染逻辑的组件。
*   **页面 (`src/pages/`):**
    *   `index.astro`: 网站首页，负责获取并展示各分类的文章列表（使用`Card`组件），包含Hero、关于我们等静态区域。实现分类切换逻辑。
    *   `articles/[...slug].astro`: 动态路由页面，用于根据slug渲染单个文章Markdown内容，使用`ArticleLayout`。
    *   (可能需要的其他静态页面，如独立的"关于我们"页等)
*   **样式 (`src/styles/`):**
    *   `global.css`: 全局样式，Tailwind CSS的引入和基础配置，自定义CSS变量（颜色、字体等）。
*   **工具配置:**
    *   `astro.config.mjs`: Astro配置文件（集成Tailwind、站点元数据等）。
    *   `tailwind.config.cjs`: Tailwind CSS配置文件（主题颜色、字体定义等）。
    *   `package.json`: 项目依赖管理。

## 7. 数据管理
*   **核心内容数据以 Markdown 文件形式存储在 `src/content/` 目录，并通过 Git 进行版本控制。**
*   **Astro Content Collections API (`getCollection`, `getEntryBySlug` 等) 在构建时读取和处理这些内容文件。**
*   无传统数据库。
*   用户偏好（如主题选择）存储在客户端浏览器的`localStorage`中。

## 8. 跨领域关注点
*   **安全性:** 主要风险在于前端依赖库的安全性（需定期更新）和部署流程的访问控制。静态文件本身风险较低。
*   **性能:** Astro默认的零JS和选择性加载（Islands）机制有利于性能。需遵循图片优化、代码压缩（Astro build默认执行）等最佳实践。
*   **可访问性 (A11y):** 遵循HTML语义化、提供`alt`文本、确保键盘导航、颜色对比度符合WCAG标准。
*   **SEO:** Astro提供良好的SEO支持（元数据管理、站点地图生成等）。Markdown frontmatter用于定义页面`title`和`description`。

## 9. 部署策略
*   **持续集成/持续部署 (CI/CD):** 使用 **GitHub Actions**。
    *   **触发器:** 推送 (push) 到 `main` 分支。
    *   **流程:**
        1.  检出代码 (Checkout code)。
        2.  设置 Node.js 环境。
        3.  安装依赖 (`npm install`)。
        4.  构建静态文件 (`npm run build`)。
        5.  部署到 GitHub Pages。
*   **托管平台:** **GitHub Pages**。

## 10. 风险与缓解
*   **风险:** **确保 LLM 生成的 Markdown 和 Frontmatter 符合预定义的 Schema。**
    *   **缓解:** **提供清晰的 Schema 定义 (`src/content/config.ts`)，在内容创建流程中加入校验步骤（或依赖 Astro 构建时的错误提示），对 LLM 输出进行必要的后处理。**
*   **风险:** 从现有 `index.html` 迁移内容到 Markdown 耗时且易错。
    *   **缓解:** 分阶段迁移，编写简单脚本辅助，仔细校对。
*   **风险:** Astro 或 Tailwind CSS 的学习曲线。
    *   **缓解:** 参考官方文档，从小功能开始实践，预留学习时间。
*   **风险:** 跨浏览器/设备的样式和JS兼容性问题。
    *   **缓解:** 使用现代Web标准，进行充分测试，利用Tailwind规避大部分CSS兼容问题。
*   **风险:** 保持Mermaid图表渲染的健壮性。
    *   **缓解:** 使用最新稳定版Mermaid，在多种环境下测试，对复杂图表考虑替代方案或截图。

## 11. 未来扩展性考量
*   **搜索:** 可通过集成Algolia DocSearch（前端方案）或构建简单的索引文件（小型站点）实现。
*   **评论系统:** 可集成第三方服务如Disqus, Giscus（基于GitHub Discussions）等。
*   **国际化 (i18n):** Astro 支持国际化路由和内容管理。
*   **更多动态功能:** 如果需要更复杂的后端交互，可将Astro作为前端，与独立的API服务集成。