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
        profilePicture: "/images/harry-percival.jpg",
        status: "TBC",
      },
      events: [
        {
          start: "2021-06-16T17:00+02:00",
          end: "2021-06-16T20:00+02:00",
          type: "LIVE_CODING",
          performer: {
            fullName: "Aaron Bassett",
            profilePicture: "/images/aaron-basset.jpg",
          },
          slug: "aaron-basset-live-coding",
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T20:00+02:00",
          end: "2021-06-16T20:15+02:00",
          status: "CONFIRMED",
          type: "INTERMISSION",
          title: "Live Coding wrap up",
        },

        {
          start: "2021-06-16T20:15+02:00",
          end: "2021-06-16T20:30+02:00",
          type: "PERFORMANCE",
          title: "Artistic Performance by Łukasz Langa",
          performer: {
            fullName: "Łukasz Langa",
            profilePicture: "/images/lukasz-langa.jpg",
          },
          slug: "lukasz-langa-performance",
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T20:30+02:00",
          end: "2021-06-16T20:40+02:00",
          type: "LIGHTNING_TALK",
          title: "Lightning talk by Tania Allard",
          performer: {
            fullName: "Tania Allard",
            profilePicture: "/images/tania-allard.jpg",
          },
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T20:40+02:00",
          end: "2021-06-16T20:50+02:00",
          type: "LIGHTNING_TALK",
          title: "Lightning talk by Alessandro Molina",
          performer: {
            fullName: "Alessandro Molina",
            profilePicture: "/images/alessandro-molina.jpg",
          },
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T20:50+02:00",
          end: "2021-06-16T21:10+02:00",
          type: "DIVERSITY_SUCCESS_STORY",
          title: "Diversity Success Story - Serena Sensini",
          performer: {
            fullName: "Serena Sensini",
            profilePicture: "/images/serena-sensini.jpg",
          },
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T21:10+02:00",
          end: "2021-06-16T22:00+02:00",
          type: "AMA",
          title: "PSF - Ask Me Anything",
          performers: [
            {
              fullName: "Ewa Jodlowska",
              profilePicture: "/images/ewa-jodlowska.jpg",
              twitter: "ewa_jodlowska",
              bio: "Executive Director for the Python Software Foundation",
            },
            {
              fullName: "Lorena Mesa",
              profilePicture: "/images/lorena-mesa.jpg",
              twitter: "loooorenanicole",
              website: "https://lorenamesa.com/",
              bio:
                "@PyLadiesChicago, @ThePSF Chair, Director, Fellow; @github engineer #LatinxInTech who 💖 live long, 🏳️‍🌈, 🐍, 🚀, 🏃 & prosper 🖖🏽; opinions my own. She/her.",
            },
          ],
          slug: "psf-ama",
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T22:00+02:00",
          end: "2021-06-16T23:00+02:00",
          type: "QUIZ",
          title: "Pub Quiz",
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T23:00+02:00",
          end: "2021-06-16T23:10+02:00",
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
          start: "2021-06-17T17:00+02:00",
          actualStart: "2021-06-17T18:30+02:00",
          end: "2021-06-17T20:00+02:00",
          type: "LIVE_CODING",
          performer: {
            fullName: "TBC",
            profilePicture: null,
          },
          status: "CONFIRMED",
        },

        {
          start: "2021-06-17T20:00+02:00",
          end: "2021-06-17T20:15+02:00",
          type: "INTERMISSION",
          status: "CONFIRMED",
          title: "Live Coding wrap up",
        },

        {
          start: "2021-06-17T20:15+02:00",
          end: "2021-06-17T20:30+02:00",
          type: "LIGHTNING_TALK",
          title: "Lightning Talk - SEMILLA — a neural audio synthesizer",
          performer: {
            fullName: "Moisés Horta Valenzuela",
            profilePicture: "/images/moises.jpg",
            bio:
              "Moisés Horta Valenzuela sound artist and electronic musician from Tijuana, México working in the fields of computer music and the history and politics of emerging technologies. My practice attempts to disrupt dichotomies with juxtapositions, such as utopia with dystopia and folk traditions with capitalist modernity.",
            twitter: "hexorcismos",
            website: "https://moiseshorta.audio/",
          },
          status: "CONFIRMED",
        },

        {
          start: "2021-06-17T20:30+02:00",
          end: "2021-06-17T20:40+02:00",
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
          start: "2021-06-17T20:40+02:00",
          end: "2021-06-17T20:50+02:00",
          type: "LIGHTNING_TALK",
          title: "Lightning Talk - Structure of Brain Activity",
          performer: {
            fullName: "Jacob Billings",
            profilePicture: "/images/jacob-billings.jpg",
          },
          status: "CONFIRMED",
        },

        {
          start: "2021-06-17T20:50+02:00",
          end: "2021-06-17T21:10+02:00",
          type: "DIVERSITY_SUCCESS_STORY",
          title: "Diversity Success Story - Darya Majidi",
          performers: [
            {
              fullName: "Darya Majidi",
              profilePicture: "/images/darya-majidi.jpg",
              bio:
                "Entrepreneur, computer science degree, economics master, expert in artificial intelligence and Healthcare, founder and CEO Daxo Group, a company of strategic consulting, founder and CEO Daxolab, innovative startup incubator, Member of Singularity University Faculty. She was the councilor for innovation of the Municipality of Livorno, President of the Youth of Confindustria Livorno and lecturer in prestigious international universities. Mentor, speaker, author of books «Women 4.0» and “Digital Sisterhood”, she is the founder of the Women 4.0 Community.",
            },
          ],
          slug: "darya-majidi-success-story",
          status: "CONFIRMED",
        },

        {
          start: "2021-06-17T21:10+02:00",
          end: "2021-06-17T22:00+02:00",
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
          slug: "ines-montani-sebastian-ramirez-interview",
          status: "CONFIRMED",
        },

        {
          start: "2021-06-17T22:00+02:00",
          end: "2021-06-17T23:00+02:00",
          type: "PERFORMANCE",
          title: "Monty Python Performance",
          performer: {
            fullName: "",
            profilePicture: null,
          },
          status: "CONFIRMED",
        },

        {
          start: "2021-06-17T23:00+02:00",
          end: "2021-06-17T23:10+02:00",
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
          start: "2021-06-18T17:00+02:00",
          end: "2021-06-18T20:00+02:00",
          type: "LIVE_CODING",
          performer: {
            fullName: "Al Sweigart",
            profilePicture: "/images/al-sweigart.jpg",
          },
          slug: "al-sweigart-live-coding",
          status: "CANCELLED",
        },

        {
          start: "2021-06-18T20:00+02:00",
          end: "2021-06-18T20:15+02:00",
          status: "CONFIRMED",
          type: "INTERMISSION",
          title: "Live Coding wrap up",
        },

        {
          start: "2021-06-18T20:15+02:00",
          end: "2021-06-18T20:30+02:00",
          type: "LIGHTNING_TALK",
          title: "TBC",
          performer: null,
          status: "TBC",
        },

        {
          start: "2021-06-18T20:30+02:00",
          end: "2021-06-18T20:50+02:00",
          type: "LIGHTNING_TALK",
          title: "The evolution of the African Python Community",
          performer: {
            fullName: "Aisha Bello",
            profilePicture: "",
            bio:
              "Aisha is based out of Toronto, Canada and works as a Solutions Architect for AWS. She co-founded and is a former board member of the Python Nigeria Community, a Python Software Foundation fellow, Django Girls board member, Django Software Foundation member and winner of the 2016 Malcolm Tredinnick Memorial award. Aisha is passionate about mentoring African women through PyLadies and DjangoGirls and bringing communities together via conferences such as PyCon. She has helped organized a number of conferences including PyCon Nigeria and Pycon Africa. \nAisha also co-hosts a podcast called “Rogue Unlearning” where she talks about a range of topics about unlearning beliefs that inhibits growth. Since the pandemic when she’s not taking long walks listening to her favorite selection of Afropop, She enjoys painting.",
          },
          status: "CONFIRMED",
          size: 2,
        },

        {
          start: "2021-06-18T20:50+02:00",
          end: "2021-06-18T21:10+02:00",
          type: "DIVERSITY_SUCCESS_STORY",
          title: "Diversity Success Story - Eleonora Rocca",
          performers: [
            {
              fullName: "Eleonora Rocca",
              profilePicture: "/images/eleonora-rocca.jpg",
            },
          ],
          slug: "eleonora-rocca-success-story",
          status: "CONFIRMED",
        },

        {
          start: "2021-06-18T21:10+02:00",
          end: "2021-06-18T22:00+02:00",
          type: "LIGHTNING_TALK",
          title: "What's new in Python 3.10",
          performers: [
            {
              fullName: "Pablo Galindo Salgado",
              bio:
                "Pablo Galindo Salgado works in the Python Infrastructure team at the Software Infrastructure department at Bloomberg L.P. He is a CPython core developer and a Theoretical Physicist specialized in general relativity and black hole physics. He is currently serving on the Python Steering Council and he is the release manager for Python 3.10 and 3.11. He has also a cat but he does not code.",
              profilePicture: "/images/pablo-galindo.jpg",
              twitter: "pyblogsal",
            },
          ],
          status: "CONFIRMED",
        },

        {
          start: "2021-06-18T22:00+02:00",
          end: "2021-06-18T23:00+02:00",
          type: "QUIZ",
          title: "Game",
          status: "TBC",
        },

        {
          start: "2021-06-18T23:00+02:00",
          end: "2021-06-18T23:10+02:00",
          type: "CLOSING",
          title: "Closing session",
          status: "CONFIRMED",
        },
      ],
    },
  ],
};

export const Standard = () => <Schedule program={program} />;
