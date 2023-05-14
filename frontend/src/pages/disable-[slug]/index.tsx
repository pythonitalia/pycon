// import { Page as BasePage } from "@python-italia/pycon-styleguide";
// import React, { Fragment } from "react";

// import { GetStaticPaths, GetStaticProps } from "next";
// import { useRouter } from "next/router";

// import { addApolloState, getApolloClient } from "~/apollo/client";
// import {
//   BlocksRenderer,
//   blocksDataFetching,
// } from "~/components/blocks-renderer";
// import { MetaTags } from "~/components/meta-tags";
// import { prefetchSharedQueries } from "~/helpers/prefetch";
// import { useCurrentLanguage } from "~/locale/context";
// import { GenericPage, queryAllPages, queryPage, usePageQuery } from "~/types";

// export const Page = () => {
//   const router = useRouter();
//   const slug = router.query.slug as string;
//   const language = useCurrentLanguage();

//   const { data } = usePageQuery({
//     variables: {
//       code: process.env.conferenceCode,
//       language,
//       slug,
//     },
//   });

//   const { cmsPage } = data;
//   const page = cmsPage as GenericPage;

//   return (
//     <Fragment>
//       <MetaTags title={page.title} description={page.searchDescription} />

//       <BasePage endSeparator={false}>
//         <BlocksRenderer blocks={page.body} />
//       </BasePage>
//     </Fragment>
//   );
// };

// export const getStaticProps: GetStaticProps = async ({ params, locale }) => {
//   const language = locale;
//   const slug = params.slug as string;
//   const client = getApolloClient();

//   const [_, pageQuery] = await Promise.all([
//     prefetchSharedQueries(client, language),
//     queryPage(client, {
//       code: process.env.conferenceCode,
//       language,
//       slug,
//     }),
//   ]);

//   if (pageQuery.data.cmsPage?.__typename !== "GenericPage") {
//     return {
//       notFound: true,
//     };
//   }

//   await blocksDataFetching(client, pageQuery.data.cmsPage.body, locale);

//   return addApolloState(client, {
//     props: {},
//   });
// };

// export const getStaticPaths: GetStaticPaths = async () => {
//   const client = getApolloClient();

//   const {
//     data: { cmsPages: italianPages },
//   } = await queryAllPages(client, {
//     code: process.env.conferenceCode,
//     language: "it",
//   });
//   const {
//     data: { cmsPages: englishPages },
//   } = await queryAllPages(client, {
//     code: process.env.conferenceCode,
//     language: "en",
//   });

//   const paths = [
//     ...italianPages.map((page) => ({
//       params: {
//         slug: page.slug,
//       },
//       locale: "it",
//     })),
//     ...englishPages.map((page) => ({
//       params: {
//         slug: page.slug,
//       },
//       locale: "en",
//     })),
//   ];

//   return {
//     paths,
//     fallback: "blocking",
//   };
// };

// export default Page;
