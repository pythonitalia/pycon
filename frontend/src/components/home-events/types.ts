import { GatsbyImageProps } from "gatsby-image";

export type PyConEvent = {
  title: string;
  locationName: string | null;
  start: string;
  imageFile: {
    childImageSharp: GatsbyImageProps | null;
  } | null;
};
