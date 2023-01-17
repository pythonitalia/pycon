import React from "react";

import { useCurrentLanguage } from "~/locale/context";
import { useKeynotesSectionQuery } from "~/types";

export const KeynotersSection = () => {
  const language = useCurrentLanguage();
  const { data } = useKeynotesSectionQuery({
    variables: {
      code: process.env.conferenceCode,
      language,
    },
  });

  if (!data) {
    return null;
  }

  const {
    conference: { keynotes },
  } = data;

  if (keynotes.length === 0) {
    return null;
  }

  return null;
};
