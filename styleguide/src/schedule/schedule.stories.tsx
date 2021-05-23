import React from "react";
import { Schedule } from "./schedule";
import { ScheduleProgram } from "./types";

export default {
  title: "Schedule",
};


const program: ScheduleProgram = {
  days: [
    {
      date: "2021-06-16",
      mc: {
        fullName: "Harry Percival",
        profilePicture: null,
        status: "TBC",
      },
      events: [
        {
          start: "2021-06-16T17:00",
          end: "2021-06-16T20:00",
          type: "LIVE_CODING",
          performer: {
            fullName: "Aaron Bassett",
            profilePicture: "/images/aaron-basset.jpeg",
          },
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T20:00",
          end: "2021-06-16T20:15",
          status: "CONFIRMED",
          type: "INTERMISSION",
          title: "Live Coding wrap up",
        },

        {
          start: "2021-06-16T20:15",
          end: "2021-06-16T20:30",
          type: "PERFORMANCE",
          title: "Artistic Performance by Ania Wsz",
          performer: {
            fullName: "Ania Wsz",
            profilePicture: "/images/ania-wsz.jpg",
          },
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T20:30",
          end: "2021-06-16T20:40",
          type: "LIGHTNING_TALK",
          title: "Lightning talk by Tania Allard",
          performer: {
            fullName: "Tania Allard",
            profilePicture: "/images/tania-allard.jpg",
          },
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T20:40",
          end: "2021-06-16T20:50",
          type: "LIGHTNING_TALK",
          title: "Lightning talk by Alessandro Molina",
          performer: {
            fullName: "Alessandro Molina",
            profilePicture: "/images/alessandro-molina.jpg",
          },
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T20:50",
          end: "2021-06-16T21:10",
          type: "DIVERSITY_SUCCESS_STORY",
          title: "Diversity Success Story - TBD",
          performers: [
            {
              fullName: "Fiorella De Luca",
              profilePicture: "/images/fiorella-de-luca.jpg",
            },
            {
              fullName: "Sabrina Scoma",
              profilePicture: "/images/sabrina-scoma.jpg",
            },
            {
              fullName: "Ambra Tonon",
              profilePicture: "/images/ambra-tonon.jpg",
            },
          ],
          status: "TBC",
        },

        {
          start: "2021-06-16T21:10",
          end: "2021-06-16T22:00",
          type: "AMA",
          title: "PSF - Ask Me Anything",
          performers: [
            {
              fullName: "Ewa Jodlowska",
              profilePicture: "/images/ewa-jodlowska.jpg",
            },
            {
              fullName: "Lorena Mesa",
              profilePicture: "/images/lorena-mesa.jpg",
            },
          ],
          status: "TBC",
        },

        {
          start: "2021-06-16T22:00",
          end: "2021-06-16T23:00",
          type: "QUIZ",
          title: "Pub Quiz",
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T23:00",
          end: "2021-06-16T23:10",
          type: "CLOSING",
          title: "Closing session",
          status: "CONFIRMED",
        },
      ],
    },
    {
      date: "2021-06-17",
      mc: {
        fullName: "Cheuk Ting Ho",
        profilePicture: "/images/cheuk-ting-ho.jpg",
        status: "TBC",
      },
      events: [
        {
          start: "2021-06-17T17:00",
          end: "2021-06-17T20:00",
          type: "LIVE_CODING",
          performer: {
            fullName: "Nina Zakharenko",
            profilePicture: "/images/nina-zakharenko.jpg",
          },
          status: "TBC",
        },

        {
          start: "2021-06-17T20:00",
          end: "2021-06-17T20:15",
          type: "INTERMISSION",
          status: "CONFIRMED",
          title: "Live Coding wrap up",
        },

        {
          start: "2021-06-17T20:15",
          end: "2021-06-17T20:30",
          type: "LIGHTNING_TALK",
          title: "Lightning Talk - TBD",
          performer: {
            fullName: "TBC",
            profilePicture: null,
          },
          status: "TBC",
        },

        {
          start: "2021-06-17T20:30",
          end: "2021-06-17T20:40",
          type: "LIGHTNING_TALK",
          title: "TBC",
          performers: [
            {
              fullName: "Ernesto Arbitrio",
              profilePicture: "/images/ernesto-arbitrio.jpg",
            },
            {
              fullName: "Alessia Marcolini",
              profilePicture: "/images/alessia-marcolini.jpg",
            },
          ],
          status: "CONFIRMED",
        },

        {
          start: "2021-06-17T20:40",
          end: "2021-06-17T20:50",
          type: "LIGHTNING_TALK",
          title: "Lightning Talk - TBD",
          performer: {
            fullName: "TBC",
            profilePicture: null,
          },
          status: "TBC",
        },

        {
          start: "2021-06-17T20:50",
          end: "2021-06-17T21:10",
          type: "DIVERSITY_SUCCESS_STORY",
          title: "Diversity Success Story - TBD",
          performers: [],
          status: "TBC",
        },

        {
          start: "2021-06-17T21:10",
          end: "2021-06-17T22:00",
          type: "INTERVIEW",
          title: "Interview with Ines Montani and Sebastián Ramírez",
          performers: [
            {
              fullName: "Ines Montani",
              profilePicture: "/images/ines-montani.png",
            },
            {
              fullName: "Sebastián Ramírez",
              profilePicture: "/images/sebastian-ramirez.jpg",
            },
          ],
          status: "CONFIRMED",
        },

        {
          start: "2021-06-17T22:00",
          end: "2021-06-17T23:00",
          type: "PERFORMANCE",
          title: "Monty Python Performance",
          performer: {
            fullName: "",
            profilePicture: null,
          },
          status: "CONFIRMED",
        },

        {
          start: "2021-06-17T23:00",
          end: "2021-06-17T23:10",
          type: "CLOSING",
          title: "Closing session",
          status: "CONFIRMED",
        },
      ],
    },
    {
      date: "2021-06-18",
      mc: {
        fullName: "Miriah Peterson",
        profilePicture: "/images/miriah-peterson.jpg",
        status: "CONFIRMED",
      },
      events: [
        {
          start: "2021-06-18T17:00",
          end: "2021-06-18T20:00",
          type: "LIVE_CODING",
          performer: {
            fullName: "Al Sweigart",
            profilePicture: "/images/al-sweigart.jpg",
          },
          status: "CONFIRMED",
        },

        {
          start: "2021-06-18T20:00",
          end: "2021-06-18T20:15",
          status: "CONFIRMED",
          type: "INTERMISSION",
          title: "Live Coding wrap up",
        },

        {
          start: "2021-06-18T20:15",
          end: "2021-06-18T20:30",
          type: "PERFORMANCE",
          title: "Artistic Performance TBC",
          performer: null,
          status: "TBC",
        },

        {
          start: "2021-06-18T20:30",
          end: "2021-06-18T20:40",
          type: "LIGHTNING_TALK",
          title: "TBC",
          performer: null,
          status: "TBC",
        },

        {
          start: "2021-06-18T20:40",
          end: "2021-06-18T20:50",
          type: "LIGHTNING_TALK",
          title: "TBC",
          performer: null,
          status: "TBC",
        },

        {
          start: "2021-06-18T20:50",
          end: "2021-06-18T21:10",
          type: "DIVERSITY_SUCCESS_STORY",
          title: "Diversity Success Story - Eleonora Rocca",
          performers: [
            {
              fullName: "Eleonora Rocca",
              profilePicture: "/images/eleonora-rocca.jpg",
            },
            {
              fullName: "Fiorella De Luca",
              profilePicture: "/images/fiorella-de-luca.jpg",
            },
            {
              fullName: "Sabrina Scoma",
              profilePicture: "/images/sabrina-scoma.jpg",
            },
            {
              fullName: "Ambra Tonon",
              profilePicture: "/images/ambra-tonon.jpg",
            },
          ],
          status: "CONFIRMED",
        },

        {
          start: "2021-06-18T21:10",
          end: "2021-06-18T22:00",
          type: "AMA",
          title: "TBC",
          performers: [],
          status: "TBC",
        },

        {
          start: "2021-06-18T22:00",
          end: "2021-06-18T23:00",
          type: "QUIZ",
          title: "Game",
          status: "TBC",
        },

        {
          start: "2021-06-18T23:00",
          end: "2021-06-18T23:10",
          type: "CLOSING",
          title: "Closing session",
          status: "CONFIRMED",
        },
      ],
    },
  ],
};

export const Standard = () => <Schedule program={program} />;
