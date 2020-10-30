/** @jsx jsx */
import { jsx } from "theme-ui";

import { useMapWithLinkQuery } from "~/types";

export const MapWithLink = ({ ...props }) => {
  const { data } = useMapWithLinkQuery({
    variables: {
      code: process.env.conferenceCode,
    },
  });

  if (!data) {
    return null;
  }

  return (
    <a
      target="_blank"
      rel="noopener noreferrer"
      href={data.conference.map!.link!}
      sx={{
        width: "100%",
        height: 350,

        display: "block",

        my: 3,

        border: "3px solid #000",

        backgroundImage: `url("${data.conference.map!.image}")`,
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
        backgroundPosition: "center",
      }}
      {...props}
    />
  );
};
