/** @jsxRuntime classic */

/** @jsx jsx */
import { Box, Flex, Heading, jsx, Text } from "theme-ui";

import Image from "next/image";

import { Link } from "~/components/link";
import { Keynote, useKeynotesSectionQuery } from "~/types";

import { GridSlider } from "../grid-slider";
import { KeynoteSlide } from "./keynote-slide";

export const KeynotersSection = () => {
  const { data } = useKeynotesSectionQuery({
    variables: {
      code: process.env.conferenceCode,
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
