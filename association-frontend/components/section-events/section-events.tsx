import EventCard from "../event-card/event-card";
import SectionItem from "../section-item/section-item";

const SectionEvents = () => {
  return (
    <SectionItem title={"Eventi 🍺"} subTitle={" We like to be busy! 🎯"}>
      <div className="space-y-10 md:space-y-0 md:grid md:grid-cols-3 md:gap-x-8 md:gap-y-10  sm:grid-cols-1">
        <EventCard
          title={"PyCon IT"}
          description={
            "Dalla nostra passione per Python è nata PyCon Italia. Ogni anno organizziamo la più grande conferenza italiana su Python. \n Ogni tanto diventiamo anche Europei, come nel 2011, 2012, 2013 e 2017, collaborando all’organizzazione di EuroPython."
          }
          isOnline={false}
        />
        <EventCard title={"PyFestival"} />
        <EventCard title={"Python Italia Meets..."} />
      </div>
    </SectionItem>
  );
};
export default SectionEvents;
