import SectionEvents from "../section-events/section-events";
import SectionJoin from "../section-join/section-join";
import SectionPythonIta from "../section-python-ita/section-python-ita";
import SectionSocialMedia from "../section-social-media/section-social-media";

const Sections = () => {
  return (
    <div className="m-8 overflow-hidden">
      <SectionPythonIta />
      <SectionJoin />
      <SectionEvents />
      <SectionSocialMedia />
    </div>
  );
};

export default Sections;
