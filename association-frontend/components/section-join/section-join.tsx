import SectionItem from "../section-item/section-item";

const SectionJoin = () => {
  return (
    <SectionItem title={"Vuoi unirti? ➡️"}>
      <div className="mt-8 lg:mt-0 lg:flex-shrink-0">
        <div className="inline-flex rounded-md shadow">
          <a
            href="#"
            className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
          >
            Crea/Entra nel tuo account{" "}
          </a>
        </div>
        <div className="ml-3 inline-flex rounded-md shadow">
          <a
            href="#"
            className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-indigo-50"
          >
            Contattaci via mail{" "}
          </a>
        </div>
      </div>
    </SectionItem>
  );
};
export default SectionJoin;
