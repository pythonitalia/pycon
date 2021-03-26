import SectionEvents from "~/components/section-events/section-events";
import SectionJoin from "~/components/section-join/section-join";
import SectionPythonIta from "~/components/section-python-ita/section-python-ita";
import SectionSocialMedia from "~/components/section-social-media/section-social-media";

const Sections = () => {
  return (
    <div className="max-w-4xl m-auto px-8 overflow-hidden">
      <SectionPythonIta />
      <SectionJoin />
      <SectionEvents />
      <SectionSocialMedia />
    </div>
  );
};

export default Sections;
