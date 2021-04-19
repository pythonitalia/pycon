import { SectionItem } from "~/components/section-item";

export const SectionPythonIta = () => {
  return (
    <SectionItem
      title={"Python Italia 🐍"}
      withBackground={true}
      overlay={false}
      textTheme={"black"}
      backgroundImageClass={"bg-white-background"}
    >
      <p className="mx-auto mb-4 text-xl text-gray-500">
        Python è la nostra passione, diffonderlo la nostra missione.
      </p>
      <p className="mx-auto mb-4 text-xl text-gray-500">
        Siamo Python Italia, un’organizzazione no-profit nata a Firenze
        nell’Aprile del 2007 dal sogno di alcuni fan italiani del più bel
        linguaggio di programmazione che ci sia.
      </p>
      <p className="mx-auto mb-4 text-xl text-gray-500">
        Da allora siamo cresciuti in una community che conta più di 400 membri.
        Collaboriamo con community simili per scambiare idee, organizzare
        eventi, imparare, crescere insieme e per avere un sacco di
        pydivertimento!
      </p>
    </SectionItem>
  );
};
