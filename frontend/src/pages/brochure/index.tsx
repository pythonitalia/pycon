import { Brochure, Benefit, Package } from "~/components/brochure";
import { useGetBrochureDataQuery } from "~/types";

const testimonials = [
  {
    text: "The conference locations were great, the Organizers went above and beyond to make things run smoothly.",
    author: "Brian Fitzpatrick, Google Inc.",
  },
  {
    text: "PyCon Italia is the conference closest and dearest to my heart out of the many I regularly attend.",
    author: "Alex Martelli, Google Inc.",
  },
  {
    text: "PyCon italia is a great way to meet  the top coders in Italy, talk with major vendors, and either recruit or be recruited.",
    author: "Raymond Hettinger, Python's Core Developer",
  },
];

export default function BrochurePage() {
  const { loading, data } = useGetBrochureDataQuery({
    variables: { conferenceCode: process.env.conferenceCode },
  });

  if (loading || !data) {
    return null;
  }

  return (
    <Brochure
      conference={data.conference}
      testimonials={testimonials}
    />
  );
}
