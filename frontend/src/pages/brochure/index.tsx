import { Brochure, Benefit, Package } from "~/components/brochure";
import { useGetBrochureDataQuery } from "~/types";

const sponsorshipOptions: Array<{
  name: string;
  description: string;
}> = [
  {
    name: "Booth in Exhibit Hall",
    description:
      "There will be a dedicated space for sponsors in the hotel hall where all the attendees will have coffee breaks and lunch.",
  },
  {
    name: "Booth in Front of Conference Rooms",
    description:
      "Only a few sponsors can have the chance to book another booth just in front of the conference rooms (limited places available) - this option may not be available for safety reasons.",
  },
  {
    name: "Small Table in Front of Conference Rooms",
    description:
      "Only a few sponsors can have the chance to book a small round high table in front of the conference rooms (limited places available) - this option may not be available for safety reasons.",
  },
  {
    name: "Social Event Named After Sponsor",
    description:
      "The sponsors will see its name and logo shown during the social event and linked with that in all the related communication and official material.",
  },
  {
    name: "Logo on PyCon Italia Speaker Desks",
    description:
      "These sponsors will have their logo shown on the speakers podiums during all the conference talks.",
  },
  {
    name: "Logo on PyCon Italia Video Titles",
    description:
      "These sponsors will have their logo shown in all the official videos recorded and published online of the event.",
  },
  {
    name: "Logo on PyCon Italia Banners",
    description:
      "These sponsors will have their logo shown on the information banners placed in the congress center during the event.",
  },
  {
    name: "Logo on PyCon Italia Website",
    description:
      "These sponsors will have their logo shown on the official PyCon Italia website for the whole duration of the event.",
  },
  {
    name: "Recruiting Session Participation",
    description:
      "The recruiting sessions will be held between the keynote session of every conference day. Those special session will give the chance to the sponsors to give a small pitch (5-7') to advertise their company and job opportunities during the most crowded moments of the event.",
  },
  {
    name: "Job Positions in the Job Board on the Website",
    description:
      "PyCon Italia website has a job board advertising the job offers of our sponsors. This board will be online until the next PyCon is organized (usually October of the next year). This board will be promoted to the event attendees and Python Italia channels subscribers (~7.5k contacts).",
  },
  {
    name: "One Recruiting Email to Attendees (Opt-in)",
    description:
      "These sponsors will have the chance to send a dedicated email (through our systems, we don't give away any personal details) to the event attendees who will have opted-in to receive this kind of communications (usually about 1/4 of the total attendees).",
  },
  {
    name: "Sponsored Keynote (1H)",
    description:
      "This sponsor will have the chance to give a keynote to the whole audience of the conference. The keynote content has to be arranged with the event organization and has to be something of interest and value for the community.",
  },
  {
    name: "Sponsored Talk (30MIN)",
    description:
      "These sponsors will have the chance to have a talk in the conference schedule. The talk content has to be arranged with the event organization and should have a technical relevance.",
  },
  {
    name: "Arranged Newsletter Content Highlighting the Sponsor",
    description:
      "This sponsor will have one special dedicated content in the official newsletter. The content will be arranged with the organization.",
  },
  {
    name: "Blog Posts Highlighting the Sponsor",
    description:
      "These sponsors will have one special thank post on the event blog.",
  },
  {
    name: "Questions in the Conference Feedback Form",
    description:
      "These sponsors will have the chance to suggest up to 2 questions in the feedback form sent to all the attendees after the event closing.",
  },
  {
    name: "One Tweet to All @pyconit Subscribers (Sponsored Content)",
    description:
      "These sponsors will have the chance to have one sponsored content tweeted directly on our Twitter account.",
  },
  {
    name: 'One Post on All the Official @pyconit Social Channels (Standard "Thank You" Post)',
    description:
      'These sponsors will have a "thank you" post on our social channels.',
  },
  {
    name: "Participation in the Gamification",
    description:
      "Every year the PyCon Italia organization prepares a special game for the attendees. This sponsor have the chance to be included in this special initiative with a mention or more (details depends on the kind of game/riddle).",
  },
  {
    name: "Shared Meeting Room",
    description:
      "These sponsors will have the chance to book a quiet meeting room just in front of the conference rooms. This room will have a shared calendar.",
  },
];

const specialOptions: Array<{
  name: string;
  description: string;
  price: number;
}> = [
  {
    name: "Advertising in the PyCon Italia Digital Signage",
    description:
      "Your advertisement will be shown on the program/information displays in the venue during the conference. (additional ADs cost is €500 each) ADs may be still images or short videos, the content must be provided by the sponsor company and will be shown on the conference location during all the conference time.",
    price: 1000,
  },
  {
    name: "Sponsored Selfie / Pic Background",
    description:
      "The sponsor will have its logo shown on the big selfie / pic background (4.1mt * 2mt), that will be put just near to the registration/information desk for the whole event.",
    price: 2000,
  },
  {
    name: "Beginners' Workshop Sponsor",
    description:
      "The sponsor will have its name and logo shown along all the communication and during this initiative (~120 people).",
    price: 1000,
  },
  {
    name: "Network Area Sponsor (Logo and Name of the Network Area)",
    description:
      "The sponsor will have its name and logo shown on the communication and in this area where people can stay, relax, chat and network together.",
    price: 2000,
  },
  {
    name: "Logo on Lanyard (Lanyard Included)",
    description:
      "The sponsor will have its logo printed on all the lanyards of the attendees.",
    price: 1500,
  },
  {
    name: "Workshop Sponsor (Logo in Training Rooms)",
    description:
      "The sponsor logo will be shown in the training room for the whole event duration.",
    price: 1500,
  },
  {
    name: "Optional Booth in Front of Conference Rooms",
    description:
      "The sponsor can have an extra desk in front of the conference rooms - this option may not be available for safety reasons.",
    price: 2000,
  },
  {
    name: "Optional Small Table in Front of Conference Rooms",
    description:
      "The sponsor can have an extra small round (80cm diameter) high table in front of the conference rooms - this option may not be available for safety reasons.",
    price: 800,
  },
  {
    name: "More Job Positions in the Job Board",
    description:
      "The sponsor can have more slots available to be published in the Job Board.",
    price: 200,
  },
];

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

const packages: Package[] = [
  {
    name: "Keystone",
    price: 10_000,
    availability: 1,
    benefits: [
      { id: "sponsored-keynote", value: true },
      { id: "booth", value: true },
      { id: "booth-front-conference-rooms", value: true },
      { id: "small-table-conference-rooms", value: true },
      { id: "complimentary-passes", value: 6 },
      { id: "discounted-passes", value: 10 },
      { id: "social-event-naming", value: true },
      { id: "logo-video-titles", value: true },
      { id: "logo-speaker-desks", value: true },
      { id: "logo-banners", value: true },
      { id: "logo-website", value: true },
      { id: "recruiting-session", value: true },
      { id: "job-board-positions", value: 3 },
      { id: "recruiting-email", value: true },
      { id: "branded-newsletter", value: true },
      { id: "blog-post", value: true },
      { id: "feedback-form-questions", value: true },
      { id: "tweet-to-subscribers", value: true },
      { id: "social-channels-post", value: true },
      { id: "gamification-participation", value: true },
      { id: "shared-meeting-room", value: true },
    ],
  },
  {
    name: "Gold",
    price: 7_000,
    availability: 2,
    benefits: [
      { id: "sponsored-talk", value: true },
      { id: "booth", value: true },
      { id: "booth-front-conference-rooms", value: true },
      { id: "small-table-conference-rooms", value: true },
      { id: "complimentary-passes", value: 4 },
      { id: "discounted-passes", value: 8 },
      { id: "logo-video-titles", value: true },
      { id: "logo-speaker-desks", value: true },
      { id: "logo-banners", value: true },
      { id: "logo-website", value: true },
      { id: "recruiting-session", value: true },
      { id: "job-board-positions", value: 2 },
      { id: "recruiting-email", value: true },
      { id: "blog-post", value: true },
      { id: "feedback-form-questions", value: true },
      { id: "tweet-to-subscribers", value: true },
      { id: "social-channels-post", value: true },
      { id: "shared-meeting-room", value: true },
    ],
  },
  {
    name: "Silver",
    price: 4_500,
    availability: 4,
    benefits: [
      { id: "booth", value: true },
      { id: "small-table-conference-rooms", value: true },
      { id: "complimentary-passes", value: 2 },
      { id: "discounted-passes", value: 4 },
      { id: "logo-video-titles", value: true },
      { id: "logo-speaker-desks", value: true },
      { id: "logo-banners", value: true },
      { id: "logo-website", value: true },
      { id: "recruiting-session", value: true },
      { id: "job-board-positions", value: 2 },
      { id: "recruiting-email", value: true },
      { id: "feedback-form-questions", value: true },
      { id: "tweet-to-subscribers", value: true },
      { id: "social-channels-post", value: true },
      { id: "shared-meeting-room", value: true },
    ],
  },
  {
    name: "Bronze",
    price: 3_000,
    availability: "unlimited",
    benefits: [
      { id: "small-table-conference-rooms", value: true },
      { id: "complimentary-passes", value: 2 },
      { id: "discounted-passes", value: 4 },
      { id: "logo-video-titles", value: true },
      { id: "logo-speaker-desks", value: true },
      { id: "logo-banners", value: true },
      { id: "logo-website", value: true },
      { id: "job-board-positions", value: 2 },
      { id: "tweet-to-subscribers", value: true },
      { id: "social-channels-post", value: true },
    ],
  },
  {
    name: "Patron",
    price: 1_000,
    availability: "unlimited",
    benefits: [
      { id: "complimentary-passes", value: 2 },
      { id: "discounted-passes", value: 2 },
      { id: "logo-speaker-desks", value: true },
      { id: "logo-banners", value: true },
      { id: "logo-website", value: true },
      { id: "social-channels-post", value: true },
    ],
  },
  {
    name: "Startup",
    price: 500,
    availability: "unlimited",
    benefits: [
      { id: "complimentary-passes", value: 1 },
      { id: "discounted-passes", value: 2 },
      { id: "logo-website", value: true },
      { id: "job-board-positions", value: 1 },
      { id: "recruiting-email", value: true },
    ],
  },
  {
    name: "Diversity",
    price: 1_000,
    availability: "unlimited",
    benefits: [
      { id: "logo-video-titles", value: "special thanks" },
      { id: "logo-speaker-desks", value: "special thanks" },
      { id: "logo-banners", value: "special thanks" },
      { id: "logo-website", value: true },
      { id: "social-channels-post", value: true },
    ],
  },
];

const benefits: Benefit[] = [
  {
    name: "Sponsored Keynote (1h)",
    id: "sponsored-keynote",
    group: "Sponsored Content",
  },
  {
    name: "Sponsored talk (30min)",
    id: "sponsored-talk",
    group: "Sponsored Content",
  },
  {
    name: "Booth in exhibit hall",
    id: "booth",
    group: "Booth",
  },
  {
    name: "Option for booth in front of conference rooms",
    id: "booth-front-conference-rooms",
    group: "Booth",
  },
  {
    name: "Option for small table in front of conference rooms",
    id: "small-table-conference-rooms",
    group: "Booth",
  },
  {
    name: "Complimentary conference session passes",
    id: "complimentary-passes",
    group: "Session Passes",
  },
  {
    name: "Conference session passes with discount (30%)",
    id: "discounted-passes",
    group: "Session Passes",
  },
  {
    name: "Social Event named after sponsor",
    id: "social-event-naming",
    group: "Brand Visibility",
  },
  {
    name: "Logo on video titles",
    id: "logo-video-titles",
    group: "Brand Visibility",
  },
  {
    name: "Logo on speaker desks",
    id: "logo-speaker-desks",
    group: "Brand Visibility",
  },
  {
    name: "Logo on banners",
    id: "logo-banners",
    group: "Brand Visibility",
  },
  {
    name: "Logo on website",
    id: "logo-website",
    group: "Brand Visibility",
  },
  {
    name: "Recruiting session participation",
    id: "recruiting-session",
    group: "Recruiting",
  },
  {
    name: "Job positions in the Job Board on the website",
    id: "job-board-positions",
    group: "Recruiting",
  },
  {
    name: "One recruiting email to attendees (opt-in)",
    id: "recruiting-email",
    group: "Recruiting",
  },
  {
    name: "Branded newsletter content highlighting the sponsor",
    id: "branded-newsletter",
    group: "Communication",
  },
  {
    name: "Blog posts highlighting the sponsor",
    id: "blog-post",
    group: "Communication",
  },
  {
    name: "Questions in the conference feedback form",
    id: "feedback-form-questions",
    group: "Communication",
  },
  {
    name: "One tweet to all @PyConIT subscribers",
    id: "tweet-to-subscribers",
    group: "Communication",
  },
  {
    name: "One post on all the official @PyConIT social channels",
    id: "social-channels-post",
    group: "Communication",
  },
  {
    name: "Participation in the gamification",
    id: "gamification-participation",
    group: "Sponsor / Attendee Interaction",
  },
  {
    name: "Shared meeting room",
    id: "shared-meeting-room",
    group: "Sponsor / Attendee Interaction",
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
      packages={packages}
      benefits={benefits}
      testimonials={testimonials}
      sponsorshipOptions={sponsorshipOptions}
      specialOptions={specialOptions}
    />
  );
}
