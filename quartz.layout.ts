import type { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({ links: { Quartz: "https://quartz.jzhao.xyz/" } }),
}

const navigation = [
  Component.PageTitle(),
  Component.MobileOnly(Component.Spacer()),
  Component.Flex({
    components: [
      { Component: Component.Search(), grow: true },
      { Component: Component.Darkmode() },
      { Component: Component.ReaderMode() },
    ],
  }),
  Component.Explorer({ title: "花园目录", folderClickBehavior: "collapse" }),
]

const graphAndContext = [
  Component.Graph({
    localGraph: {
      depth: 2,
      scale: 1.15,
      repelForce: 0.8,
      centerForce: 0.35,
      linkDistance: 42,
      fontSize: 0.8,
      opacityScale: 1.25,
      showTags: true,
    },
    globalGraph: {
      scale: 0.9,
      repelForce: 0.75,
      centerForce: 0.35,
      linkDistance: 48,
      fontSize: 0.72,
      opacityScale: 1.2,
      showTags: true,
      enableRadial: true,
    },
  }),
  Component.DesktopOnly(Component.TableOfContents()),
  Component.Backlinks(),
  Component.RecentNotes({ title: "最近更新", limit: 5, showTags: true }),
]

export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
  ],
  left: navigation,
  right: graphAndContext,
}

export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: navigation,
  right: [Component.RecentNotes({ title: "最近更新", limit: 8, showTags: true })],
}
