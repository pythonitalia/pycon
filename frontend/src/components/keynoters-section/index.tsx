/** @jsxRuntime classic */

/** @jsx jsx */
import { jsx } from "theme-ui";

import { useCurrentLanguage } from "~/locale/context";
import { useKeynotesSectionQuery } from "~/types";

import { GridSlider } from "../grid-slider";
import { KeynoteSlide } from "./keynote-slide";

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

  return (
    <GridSlider title="Keynoters" items={keynotes} Component={KeynoteSlide} />
  );
};
