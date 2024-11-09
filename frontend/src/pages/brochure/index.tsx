import { Brochure } from "~/components/brochure";
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

const stats = {
  attendees: "1000+",
  speakers: "100+",
  talks: "100+",
  uniqueOnlineVisitors: "10000+",
  sponsorsAndPartners: "50+",
  grantsGiven: "15+",
  coffees: "10000+",
};

const introduction = `
**PyCon Italia** is the official Italian event about Python, but nowadays it’s one of the most important pythonic events in all of Europe. More than 1000 people gather from all over the world to attend, learn, code, speak, support, and meet other fellow pythonistas in Bologna.

Our care for the quality of every aspect of PyCon Italia results in a wonderful gathering for growing together.

This year, PyCon Italia is at its 14th edition, and we'll try to make it an unforgettable and even more great experience for everyone.
`.trim();

const tags = `
BEGINNERS’ & DJANGOGIRLS — WORKSHOPS
NETWORKING — RECRUITING SESSION SOCIAL
DINNER & EVENTS SPEAKERS & ATTENDEES
FROM ALL OVER THE WORLD CARE FOR
DIVERSITY AND INCLUSION PRIZES AND
CHALLENGES SPRINTS — CHILDCARE — GREEN
`.trim();

const location = {
  city: "Bologna",
  cityDescription: `
Bologna is one of the most charming cities of Italy, and we love it. Many of our attendees enjoy coming here in autumn, for experiencing the rich history and culinary culture that will forever be an essential part of this place.

Included in the UNESCO Creative Cities Network as a City of Music, the historic center of Bologna is a treasure trove of art and architecture.

The PyCon Italia venue is located close to the city center (~25’ walk) and many initiatives will be announced for sharing this treasure with our attendees.
`.trim(),

  country: "Italy",
  countryDescription:
    'Last but not least, Italy is famous in all the world for its food and our attendees never felt disappointed on how we want this tradition to be honored. Bologna, known as "La Grassa" (The Fat One), is especially renowned for its culinary excellence.',
  imageUrl:
    "https://images.unsplash.com/photo-1671794646570-cba0e7dc162b?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
};
const community = `
PyCon Italia is aimed at everyone in the Python community, of all skill levels, both users and programmers. It is a great meeting event: ~1000attendees are expected from all over the world. Professionals, companies and students will meet for learning, collaborate and grow together. The delegates are a mix of Python users and developers (~60%), students (~20%), PMs (~8%), researchers (~7%), CTOs (~5%) as well as individuals whose businesses rely on the use of Python.
`.trim();

const whySponsor = {
  introduction:
    "The very first reason is to help the community around this environment to grow. Sponsors are what make this conference possible. From low ticket prices to financial aid, to video recording, the organizations who step forward to support PyCon Italia, in turn, support the entire Python community.",
  text: `
Advertising your brand in a very targeted audience like this gives back a high increase of its awareness.

Moreover, many of our sponsoring services have turned towards the increased recruiting requests we got in the last years, that's why you can find several ways of engage potential candidates for the position you are looking for in our event.
`.trim(),
};

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
      content={{ stats, introduction, tags, location, community, whySponsor }}
    />
  );
}
