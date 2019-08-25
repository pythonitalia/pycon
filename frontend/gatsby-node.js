/* eslint-disable @typescript-eslint/no-var-requires */

const path = require("path");
const {
    createFilePath,
    createRemoteFileNode,
} = require("gatsby-source-filesystem");

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
    const { createNode } = actions;
    createResolvers({
        BACKEND_Post: {
            imageFile: {
                type: `File`,
                resolve(source, args, context, info) {
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
                },
            },
        },
    });
};

exports.createPages = async ({ graphql, actions, reporter }) => {
    const { createPage } = actions;
    // Query for markdown nodes to use in creating pages.
    const result = await graphql(
        `
            query {
                backend {
                    blogPosts {
                        slug
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

    result.data.backend.blogPosts.forEach(({ slug }) => {
        createPage({
            path: `/blog/${slug}`,
            component: blogPostTemplate,
            context: {
                slug,
            },
        });
    });
};
