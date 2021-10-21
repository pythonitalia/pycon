import { queryFooter, queryHeader } from "~/types";

export const prefetchSharedQueries = async (language: string) => {
  await queryHeader({
    code: process.env.conferenceCode,
    language,
  });

  await queryFooter({
    code: process.env.conferenceCode,
  });
};
