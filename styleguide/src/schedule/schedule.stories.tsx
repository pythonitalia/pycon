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
        profilePicture: "...",
        status: "TBC",
      },
      events: [
        {
          start: "2021-06-16T17:00",
          end: "2021-06-16T20:00",
          type: "LIVE_CODING",
          title: "Live Coding with Aaron Bassett",
          performer: {
            fullName: "Aaron Bassett",
            profilePicture: "...",
          },
          status: "TBC",
        },

        {
          start: "2021-06-16T20:00",
          end: "2021-06-16T20:15",
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
            profilePicture: "...",
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
            profilePicture: "...",
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
            profilePicture: "...",
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
              profilePicture: "...",
            },
            {
              fullName: "Sabrina Scoma",
              profilePicture: "...",
            },
            {
              fullName: "Ambra Tonon",
              profilePicture: "...",
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
              fullName: "Lelio Campanile",
              profilePicture: "...",
            },
            {
              fullName: "Luca Fedrizzi",
              profilePicture: "...",
            },
          ],
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T22:00",
          end: "2021-06-16T22:10",
          type: "LIGHTNING_TALK",
          title: "Lightning Talk - TBD",
          performer: {
            fullName: "TBC",
            profilePicture: "...",
          },
          status: "TBC",
        },

        {
          start: "2021-06-16T22:10",
          end: "2021-06-16T22:30",
          type: "PERFORMANCE",
          title: "Artistic Performance - TBD",
          performer: {
            fullName: "TBC",
            profilePicture: "...",
          },
          status: "TBC",
        },

        {
          start: "2021-06-16T22:30",
          end: "2021-06-16T23:30",
          type: "QUIZ",
          title: "Pub Quiz",
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T23:30",
          end: "2021-06-16T23:40",
          type: "CLOSING",
          title: "Closing session",
          status: "CONFIRMED",
        },
      ],
    },
    {
      date: "2021-06-16",
      mc: {
        fullName: "Harry Percival",
        profilePicture: "...",
        status: "TBC",
      },
      events: [
        {
          start: "2021-06-16T17:00",
          end: "2021-06-16T20:00",
          type: "LIVE_CODING",
          title: "Live Coding with Aaron Bassett",
          performer: {
            fullName: "Aaron Bassett",
            profilePicture: "...",
          },
          status: "TBC",
        },

        {
          start: "2021-06-16T20:00",
          end: "2021-06-16T20:15",
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
            profilePicture: "...",
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
            profilePicture: "...",
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
            profilePicture: "...",
          },
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T21:00",
          end: "2021-06-16T21:10",
          type: "DIVERSITY_SUCCESS_STORY",
          title: "Diversity Success Story - TBD",
          performers: [
            {
              fullName: "Fiorella De Luca",
              profilePicture: "...",
            },
            {
              fullName: "Sabrina Scoma",
              profilePicture: "...",
            },
            {
              fullName: "Ambra Tonon",
              profilePicture: "...",
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
              fullName: "Lelio Campanile",
              profilePicture: "...",
            },
            {
              fullName: "Luca Fedrizzi",
              profilePicture: "...",
            },
          ],
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T22:00",
          end: "2021-06-16T22:10",
          type: "LIGHTNING_TALK",
          title: "Lightning Talk - TBD",
          performer: {
            fullName: "TBC",
            profilePicture: "...",
          },
          status: "TBC",
        },

        {
          start: "2021-06-16T22:10",
          end: "2021-06-16T22:30",
          type: "PERFORMANCE",
          title: "Artistic Performance - TBD",
          performer: {
            fullName: "TBC",
            profilePicture: "...",
          },
          status: "TBC",
        },

        {
          start: "2021-06-16T22:30",
          end: "2021-06-16T23:30",
          type: "QUIZ",
          title: "Pub Quiz",
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T23:30",
          end: "2021-06-16T23:40",
          type: "CLOSING",
          title: "Closing session",
          status: "CONFIRMED",
        },
      ],
    },
  ],
};

program.days.push(program.days[0]);

export const Standard = () => <Schedule program={program} />;
