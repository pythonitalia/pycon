/** @jsx jsx */
import { graphql, useStaticQuery } from "gatsby";
import { jsx } from "theme-ui";

export const MapWithLink = () => {
  const {
    backend: { conference },
  } = useStaticQuery(graphql`
    query MapWithLink {
      backend {
        conference {
          map {
            image(width: 1280, height: 400, zoom: 15)
            link
          }
        }
      }
    }
  `);

  return (
    <a
      target="_blank"
      rel="noopener noreferrer"
      href={conference.map!.link!}
      sx={{
        width: "100%",
        height: 350,

        display: "block",

        mt: [3, 3, 0],

        gridColumnStart: [null, null, 3],

        border: "3px solid #000",

        backgroundImage: `url("${conference.map!.image}")`,
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
        backgroundPosition: "center",
      }}
    />
  );
};
