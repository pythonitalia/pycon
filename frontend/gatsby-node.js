/* eslint-disable @typescript-eslint/no-var-requires */

const path = require("path");
const {
  createFilePath,
  createRemoteFileNode,
} = require("gatsby-source-filesystem");

require("dotenv").config({
  path: `.env`,
});

exports.onCreateNode = ({ node, actions, getNode, getNodes }) => {
  const { createNodeField } = actions;

  if (node.internal.type === `MarkdownRemark`) {
    const value = createFilePath({ node, getNode });
    createNodeField({
      name: `slug`,
      node,
      value,
    });
  }
};

exports.createResolvers = ({
  actions,
  cache,
  createNodeId,
  createResolvers,
  store,
  reporter,
}) => {
  const imageFileResolver = (source, args, context, info) => {
    if (!source.image) {
      return null;
    }

    return createRemoteFileNode({
      url: source.image,
      store,
      cache,
      createNode,
      createNodeId,
      reporter,
    });
  };

  const { createNode } = actions;

  const typesWithImages = [
    "BACKEND_Post",
    "BACKEND_Page",
    "BACKEND_Sponsor",
    "BACKEND_Event",
    "BACKEND_ScheduleItem",
  ];

  const resolvers = {};

  typesWithImages.forEach(type => {
    resolvers[type] = {
      imageFile: {
        type: `File`,
        resolve: imageFileResolver,
      },
    };
  });

  createResolvers(resolvers);
};

exports.createPages = async ({ graphql, actions, reporter }) => {
  const { createPage, createRedirect } = actions;

  const result = await graphql(
    `
      query {
        backend {
          blogPosts {
            slug
          }
          pages {
            slugEn: slug(language: "en")
            slugIt: slug(language: "it")
          }
        }
      }
    `,
  );

  if (result.errors) {
    reporter.panicOnBuild(`Error while running GraphQL query.`);
    return;
  }

  const blogPostTemplate = path.resolve(`src/templates/blog-post.tsx`);
  const pageTemplate = path.resolve(`src/templates/page.tsx`);
  const homeTemplate = path.resolve(`src/templates/home.tsx`);
  const appTemplate = path.resolve(`src/templates/app.tsx`);

  createRedirect({
    fromPath: `/`,
    redirectInBrowser: true,
    toPath: `/en`,
  });

  const pages = [
    { template: homeTemplate, path: "" },
    { template: appTemplate, path: "/login", matchPath: "/login/*" },
    { template: appTemplate, path: "/signup", matchPath: "/signup/*" },
    { template: appTemplate, path: "/profile", matchPath: "/profile/*" },
    { template: appTemplate, path: "/cfp", matchPath: "/cfp/*" },
    {
      template: appTemplate,
      path: "/submission",
      matchPath: "/submission/*",
    },
    {
      template: appTemplate,
      path: "/profile/edit",
      matchPath: "/profile/edit/*",
    },
    {
      template: appTemplate,
      path: "/submission",
      matchPath: "/submission/*",
    },
    {
      template: appTemplate,
      path: "/reset-password",
      matchPath: "/reset-password/*",
    },
    { template: appTemplate, path: "/tickets", matchPath: "/tickets/*" },
  ];
  const languages = ["en", "it"];

  pages.forEach(page => {
    languages.forEach(language =>
      createPage({
        path: `/${language}${page.path}`,
        component: page.template,
        matchPath: page.matchPath ? `/${language}${page.matchPath}` : null,
        context: {
          language,
          conferenceCode: process.env.CONFERENCE_CODE || "pycon-demo",
        },
      }),
    );
  });

  result.data.backend.blogPosts.forEach(({ slug }) => {
    // TODO: translate blog
    createPage({
      path: `/en/blog/${slug}`,
      component: blogPostTemplate,
      context: {
        slug,
      },
    });

    createPage({
      path: `/it/blog/${slug}`,
      component: blogPostTemplate,
      context: {
        slug,
      },
    });
  });

  result.data.backend.pages.forEach(({ slugEn, slugIt }) => {
    createPage({
      path: `/it/${slugIt}`,
      component: pageTemplate,
      context: {
        language: "it",
        slug: slugIt,
      },
    });

    createPage({
      path: `/en/${slugEn}`,
      component: pageTemplate,
      context: {
        language: "en",
        slug: slugEn,
      },
    });
  });

  // generic social card
  const genericSocialCardTemplate = path.resolve(
    `src/templates/social-card.tsx`,
  );

  createPage({
    path: `/social`,
    component: genericSocialCardTemplate,
  });
};

exports.onCreatePage = async ({ page, actions }) => {
  const { createPage, deletePage } = actions;

  if (page.path.match(/^\/[a-z]{2}\/404\/$/)) {
    const oldPage = { ...page };

    const language = page.path.split(`/`)[1];
    page.matchPath = `/${language}/*`;

    deletePage(oldPage);
    createPage({ ...page, context: { language } });
  }
};

exports.onCreateWebpackConfig = ({
  stage,
  rules,
  loaders,
  plugins,
  actions,
}) => {
  actions.setWebpackConfig({
    module: {
      rules: [
        {
          test: /\.graphql$/,
          exclude: /node_modules/,
          loader: "graphql-tag/loader",
        },
      ],
    },
  });
};
