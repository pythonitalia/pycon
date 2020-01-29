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

const createPageWithSocialCards = (
  createPage,
  socialCardComponent,
  args,
  createOnlySocialCard = false,
  cardTypes = ["social", "social-square", "social-twitter"],
) => {
  cardTypes.forEach(type => {
    createPage({
      ...args,
      path: `${args.path}/${type}`,
      component: socialCardComponent,
      context: {
        ...args.context,
        cardType: type,
      },
    });
  });

  if (!createOnlySocialCard) {
    const cards = {};

    if (cardTypes.includes("social")) {
      cards.socialCard = `${args.path}/social/social.png`;
    } else if (cardTypes.includes("social-twitter")) {
      cards.socialCard = `${args.path}/social/social-twitter.png`;
    }

    if (cardTypes.includes("social-twitter")) {
      cards.socialCardTwitter = `${args.path}/social/social-twitter.png`;
    }

    createPage({
      ...args,
      context: {
        ...args.context,
        ...cards,
      },
    });
  }
};

exports.createPages = async ({ graphql, actions, reporter }) => {
  const { createPage, createRedirect } = actions;

  const result = await graphql(
    `
      query Pages {
        backend {
          blogPosts {
            slugEn: slug(language: "en")
            slugIt: slug(language: "it")
          }
          pages {
            slugEn: slug(language: "en")
            slugIt: slug(language: "it")
          }
          conference {
            keynotes {
              slug
            }
          }
          submissions {
            id
          }
        }
      }
    `,
  );

  if (result.errors) {
    console.log(result.errors);

    reporter.panicOnBuild(`Error while running GraphQL query.`);
    return;
  }

  const blogTemplate = path.resolve(`src/templates/blog/index.tsx`);
  const blogPostTemplate = path.resolve(`src/templates/blog/post.tsx`);
  const blogPostSocialTemplate = path.resolve(
    `src/templates/blog/social-card.tsx`,
  );
  const submissionTemplate = path.resolve(`src/templates/submission/index.tsx`);
  const submissionSocialTemplate = path.resolve(
    `src/templates/submission/social-card.tsx`,
  );
  const pageTemplate = path.resolve(`src/templates/page.tsx`);
  const homeTemplate = path.resolve(`src/templates/home.tsx`);
  const appTemplate = path.resolve(`src/templates/app.tsx`);
  const talkTemplate = path.resolve(`src/templates/talk/talk.tsx`);
  const talkSocialTemplate = path.resolve(`src/templates/talk/social-card.tsx`);

  createRedirect({
    fromPath: `/`,
    redirectInBrowser: true,
    toPath: `/en`,
  });

  const pages = [
    { template: homeTemplate, path: "" },
    { template: blogTemplate, path: "/blog" },
    { template: appTemplate, path: "/login", matchPath: "/login/*" },
    { template: appTemplate, path: "/signup", matchPath: "/signup/*" },
    { template: appTemplate, path: "/grants", matchPath: "/grants/*" },
    {
      template: appTemplate,
      path: "/unsubscribe",
      matchPath: "/unsubscribe/*",
    },
    { template: appTemplate, path: "/profile", matchPath: "/profile/*" },
    { template: appTemplate, path: "/cfp", matchPath: "/cfp/*" },
    { template: appTemplate, path: "/orders", matchPath: "/orders/*" },
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
      path: "/submission/edit",
      matchPath: "/submission/*/edit",
    },
    {
      template: appTemplate,
      path: "/reset-password",
      matchPath: "/reset-password/*",
    },
    { template: appTemplate, path: "/tickets", matchPath: "/tickets/*" },
    {
      template: appTemplate,
      path: "/voting",
      matchPath: "/voting/*",
    },
    {
      template: appTemplate,
      path: "/ranking",
      matchPath: "/ranking/*",
    },
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
          alternateLinks: {
            en: `/en${page.path}`,
            it: `/it${page.path}`,
          },
          conferenceCode: process.env.CONFERENCE_CODE || "pycon-demo",
        },
      }),
    );
  });

  result.data.backend.blogPosts.forEach(({ slugEn, slugIt }) => {
    createPageWithSocialCards(createPage, blogPostSocialTemplate, {
      path: `/en/blog/${slugEn}`,
      component: blogPostTemplate,
      context: {
        slug: slugEn,
        language: "en",
        alternateLinks: {
          en: `/en/blog/${slugEn}`,
          it: `/it/blog/${slugIt}`,
        },
      },
    });

    createPageWithSocialCards(createPage, blogPostSocialTemplate, {
      path: `/it/blog/${slugIt}`,
      component: blogPostTemplate,
      context: {
        slug: slugIt,
        language: "it",
        alternateLinks: {
          en: `/en/blog/${slugEn}`,
          it: `/it/blog/${slugIt}`,
        },
      },
    });
  });

  result.data.backend.conference.keynotes.forEach(({ slug }) => {
    createPageWithSocialCards(createPage, talkSocialTemplate, {
      path: `/en/keynote/${slug}`,
      component: talkTemplate,
      context: {
        slug,
        language: "en",
        type: "keynote",
        alternateLinks: {
          en: `/en/keynote/${slug}`,
          it: `/it/keynote/${slug}`,
        },
      },
    });

    createPageWithSocialCards(createPage, talkSocialTemplate, {
      path: `/it/keynote/${slug}`,
      component: talkTemplate,
      context: {
        slug,
        language: "it",
        type: "keynote",
        alternateLinks: {
          en: `/en/keynote/${slug}`,
          it: `/it/keynote/${slug}`,
        },
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
        alternateLinks: {
          en: `/en/${slugEn}`,
          it: `/it/${slugIt}`,
        },
      },
    });

    createPage({
      path: `/en/${slugEn}`,
      component: pageTemplate,
      context: {
        language: "en",
        slug: slugEn,
        alternateLinks: {
          en: `/en/${slugEn}`,
          it: `/it/${slugIt}`,
        },
      },
    });
  });

  result.data.backend.submissions.forEach(({ id }) => {
    createPage({
      component: submissionTemplate,
      path: `/en/submission/${id}`,
      context: {
        id,
        language: "en",
        alternateLinks: {
          en: `/en/submission/${id}`,
          it: `/it/submission/${id}`,
        },
      },
    });

    createPage({
      component: submissionTemplate,
      path: `/it/submission/${id}`,
      context: {
        id,
        language: "it",
        alternateLinks: {
          en: `/en/submission/${id}`,
          it: `/it/submission/${id}`,
        },
      },
    });
  });

  // generic social card
  const genericSocialCardTemplate = path.resolve(
    `src/templates/social-card.tsx`,
  );

  createPageWithSocialCards(
    createPage,
    genericSocialCardTemplate,
    {
      path: "",
    },
    true,
  );
};

exports.onCreatePage = async ({ page, actions }) => {
  const { createPage, deletePage } = actions;

  if (page.path.match(/^\/[a-z]{2}\/404\/$/)) {
    const oldPage = { ...page };

    const language = page.path.split(`/`)[1];
    page.matchPath = `/${language}/*`;

    deletePage(oldPage);
    createPage({
      ...page,
      context: {
        language,
        alternateLinks: {
          en: `/en/404`,
          it: `/it/404`,
        },
      },
    });
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
