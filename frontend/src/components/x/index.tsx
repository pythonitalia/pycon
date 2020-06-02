/** @jsx jsx */
import { Box } from "@theme-ui/components";
import { Fragment, useState } from "react";
import { jsx } from "theme-ui";

import { useCurrentLanguage } from "../../context/language";
import { Link } from "../link";

function useLocalStorage(key: string, initialValue: any) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);

      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.log(error);

      return initialValue;
    }
  });

  const setValue = (value: any) => {
    try {
      const valueToStore =
        value instanceof Function ? value(storedValue) : value;

      setStoredValue(valueToStore);

      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.log(error);
    }
  };

  return [storedValue, setValue];
}

const English = () => (
  <Fragment>
    <Box as="p" sx={{ mb: 3, fontSize: 1 }}>
      Since from the very beginning, the Python community stand out to reject
      every kind of discrimination. In every event, was it a small one or a huge
      one, directly organised or indirectly linked to our organisation, the
      moral Code of Conduct our community always shared and applied helped us
      opposing the unpleasant attempts to use the differences that distinguish
      everyone of us to categorise, divide and discriminate people.
    </Box>
    <Box as="p" sx={{ mb: 3, fontSize: 1 }}>
      In some context it was more difficult than in others, and definitely the
      extreme situation that the USA are going through now makes us understand
      how society is still far from accepting itself as the manifold and
      incredibly complex and multifaceted net of experiences, memory, history,
      curiosity, intuition, sensitivity, emotions, points of view, talents and
      features that it is. The immeasurable richness which is inside all this
      differences should associate everyone in a society where the color of our
      skin as our politic, sexual, philosophic, religious, social and cultural
      orientation, our origin, social class, knowledge, education, fade together
      and blend making us all equal in our uniqueness.
    </Box>
    <Box as="p" sx={{ mb: 3, fontSize: 1 }}>
      This is the reason why the Python Italia Association want to officially
      rise up in support of the Python Software Foundation official public
      statement regarding the recent happenings and the{" "}
      <Link
        href="https://twitter.com/hashtag/BlackLivesMatter"
        sx={{ color: "rgb(255, 255, 255)", fontWeight: "bold" }}
      >
        #BlackLivesMatter
      </Link>{" "}
      movement
    </Box>

    <Box as="p" sx={{ mb: 3, fontSize: 1 }}>
      <Link
        href="https://twitter.com/ThePSF/status/1267591714925133825"
        sx={{ color: "rgb(255, 255, 255)", fontWeight: "bold" }}
      >
        https://twitter.com/ThePSF/status/1267591714925133825
      </Link>
    </Box>
    <Box as="p" sx={{ mb: 3, fontSize: 1 }}>
      Our social efforts will always be against every discrimination and
      supporting the acknowledgement of diversity as a fundamental value of our
      society.
    </Box>

    <Box as="p" sx={{ mb: 3, fontSize: 1, fontWeight: "bold" }}>
      The Python Italia Association and the PyCon Italia organising team.
    </Box>
  </Fragment>
);

const Italian = () => (
  <Fragment>
    <Box as="p" sx={{ mb: 3, fontSize: 1 }}>
      Fin dall’inizio, la comunità Python si è distinta per ripudiare ogni tipo
      di discriminazione. In ogni evento, piccolo o grande, direttamente
      organizzato o indirettamente correlato, il codice di condotta morale che
      la comunità ha da sempre condiviso ed applicato è servito ad arginare gli
      odiosi tentativi di usare le differenze che caratterizzano ognuno di noi
      per categorizzare e separare e discriminare.
    </Box>
    <Box as="p" sx={{ mb: 3, fontSize: 1 }}>
      In alcuni contesti è stato più difficile che in altri, e sicuramente la
      situazione estrema che oggi si sta verificando in USA ci fa capire quanto
      ancora la società sia lontana dall’accettarsi per la multiforme ed
      incredibilmente sfaccettata e complessa rete di esperienze, memoria,
      storia, curiosità, intuizione, sensibilità, emozioni, punti di vista,
      capacità e peculiarità che è. L’immensa ricchezza che si trova in questa
      infinità di differenze ci dovrebbe accomunare tutti in una società dove i
      colori della nostra pelle, i nostri orientamenti politici, sessuali,
      filosofici, religiosi, sociali, culturali, la nostra provenienza, classe
      sociale, conoscenza, formazione, sfumano fino a scomparire rendendoci
      tutti uguali nella nostra unicità.
    </Box>
    <Box as="p" sx={{ mb: 3, fontSize: 1 }}>
      E’ per questo che l’Associazione Python Italia vuole comunicare in maniera
      ufficiale ed univoca il suo supporto al comunicato ufficiale della Python
      Software Foundation riguardo ai recenti avvenimenti e al movimento{" "}
      <Link
        href="https://twitter.com/hashtag/BlackLivesMatter"
        sx={{ color: "rgb(255, 255, 255)", fontWeight: "bold" }}
      >
        #BlackLivesMatter
      </Link>{" "}
    </Box>

    <Box as="p" sx={{ mb: 3, fontSize: 1 }}>
      <Link
        href="https://twitter.com/ThePSF/status/1267591714925133825"
        sx={{ color: "rgb(255, 255, 255)", fontWeight: "bold" }}
      >
        https://twitter.com/ThePSF/status/1267591714925133825
      </Link>
    </Box>
    <Box as="p" sx={{ mb: 3, fontSize: 1 }}>
      Il nostro sforzo sociale andrà sempre nella direzione della lotta alla
      discriminazione ed al supporto al riconoscimento della diversità come
      valore fondamentale della nostra società.
    </Box>

    <Box as="p" sx={{ mb: 3, fontSize: 1, fontWeight: "bold" }}>
      L’associazione Python Italia e lo staff di PyCon Italia.
    </Box>
  </Fragment>
);

export const X = () => {
  const [closed, updateClosed] = useLocalStorage("x/2020", false);
  const language = useCurrentLanguage();

  if (closed) {
    return null;
  }

  return (
    <Box
      onClick={() => updateClosed(true)}
      sx={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        background: "rgba(0, 0, 0, 0.5)",
        zIndex: 2020,
        overflow: "scroll",
      }}
    >
      <Box
        onClick={(e: any) => e.stopPropagation()}
        sx={{
          color: "rgb(255, 255, 255)",
          background: "rgba(0, 0, 0)",
          mt: 100,
          mx: "auto",
          py: 3,
          px: 4,
          width: "90%",
          maxWidth: 600,
          textAlign: "justify",
        }}
      >
        {language === "it" ? <Italian /> : <English />}
      </Box>
    </Box>
  );
};
