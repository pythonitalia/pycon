import SectionItem from "~/components/section-item/section-item";

const SectionPythonIta = () => {
  return (
    <SectionItem title={"Python Italia 🐍"}>
      <p className="max-w-2xl text-xl text-gray-500 mx-auto">
        Python è la nostra passione, diffonderlo la nostra missione.
      </p>
      <p className="mt-4 max-w-2xl text-xl text-gray-500 mx-auto">
        Siamo Python Italia, un’organizzazione no-profit nata a Firenze
        nell’Aprile del 2007 dal sogno di alcuni fan italiani del più bel
        linguaggio di programmazione che ci sia.
      </p>
      <p className="mt-4 max-w-2xl text-xl text-gray-500 mx-auto">
        Da allora siamo cresciuti in una community che conta più di 400 membri.
        Collaboriamo con community simili per scambiare idee, organizzare
        eventi, imparare, crescere insieme e per avere un sacco di
        pydivertimento!
      </p>
    </SectionItem>
  );
};
export default SectionPythonIta;
