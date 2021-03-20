import EventCard from "../event-card/event-card";

const SectionEvents = () => {
  return (
    <div className="bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Eventi 🍺
          </p>
          <p className="mt-4 max-w-2xl text-xl text-gray-500 mx-auto">
            We like to be busy! 🎯
          </p>
          <div className="mt-5">
            <dl className="space-y-10 md:space-y-0 md:grid md:grid-cols-3 md:gap-x-8 md:gap-y-10  sm:grid-cols-1">
              <EventCard
                title={"PyCon IT"}
                description={
                  "Dalla nostra passione per Python è nata PyCon Italia. Ogni anno organizziamo la più grande conferenza italiana su Python. \n Ogni tanto diventiamo anche Europei, come nel 2011, 2012, 2013 e 2017, collaborando all’organizzazione di EuroPython."
                }
                isOnline={false}
              />
              <EventCard title={"PyFestival"} />
              <EventCard title={"Python Italia Meets..."} />
            </dl>
          </div>
        </div>
      </div>
    </div>
  );
};
export default SectionEvents;
