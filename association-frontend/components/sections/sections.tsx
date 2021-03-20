import SectionEvents from "../section-events/section-events";
import SectionFollowUs from "../section-follow-us/section-follow-us";
import SectionJoin from "../section-join/section-join";
import SectionPythonIta from "../section-python-ita/section-python-ita";

const Sections = () => {
  return (
    <div className="relative pt-16 pb-32 overflow-hidden">
      <SectionPythonIta />
      <SectionJoin />
      <SectionEvents />
      <SectionFollowUs />
    </div>
  );
};

export default Sections;
