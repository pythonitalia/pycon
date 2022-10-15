/** @jsxRuntime classic */

/** @jsx jsx */
import { Carousel, SpeakerSquare } from "@python-italia/pycon-styleguide";
import { jsx } from "theme-ui";

import { useCurrentLanguage } from "~/locale/context";
import { useKeynotesSectionQuery } from "~/types";

import { Link } from "../link";

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

  return (
    <Carousel title="Keynoters">
      {keynotes.map((keynote, index) => (
        <SpeakerSquare
          key={index}
          name={keynote.speakers[0].name}
          subtitle={keynote.title}
          portraitUrl={keynote.speakers[0].photo}
          linkWrapper={<Link path={`/keynotes/${keynote.slug}/`} />}
        />
      ))}
    </Carousel>
  );
};
