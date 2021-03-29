import SectionItem from "~/components/section-item/section-item";

const SectionPyConIta = () => {
  return (
    <SectionItem
      title="PyCon Italia"
      withBackground={true}
      overlay={false}
      backgroundImageClass={"bg-pycon-group-blue"}
    >
      <p className="mb-4 max-w-2xl text-xl text-white text-center mx-auto">
        Dalla nostra passione per Python è nata PyCon Italia.
        <br />
        Ogni anno organizziamo la più grande conferenza italiana su Python.
        <br />
        Ogni tanto diventiamo anche Europei, come nel 2011, 2012, 2013 e 2017,
        collaborando all’organizzazione di EuroPython.
      </p>
      <p className="mt-12 max-w-2xl text-xl text-white text-center select-none mx-auto">
        <a
          href="https://pycon.it/en"
          target="_blank"
          className="px-6 py-4 border border-transparent text-base font-bold text-bluecyan uppercase tracking-widest bg-yellow  hover:bg-bluecyan hover:text-yellow shadow-solidblue hover:shadow-solidyellow"
        >
          Visita il sito
        </a>
      </p>
    </SectionItem>
  );
};

export default SectionPyConIta;
