import SectionPicture from "./section-picture";

type SectionItemProps = {
  title: string;
  description?: string;
  pictureSrc?: string;
};

const SectionItem: React.FC<SectionItemProps> = ({
  title,
  description,
  ...props
}) => {
  return (
    <div className="mt-24">
      <div className="lg:mx-auto lg:max-w-7xl lg:px-8 lg:grid lg:grid-cols-2 lg:grid-flow-col-dense lg:gap-24">
        <div className="px-4 max-w-xl mx-auto sm:px-6 lg:py-16 lg:max-w-none lg:mx-0 lg:px-0">
          <div>
            <div className="mt-6">
              <h2 className="text-3xl font-extrabold tracking-tight text-gray-900">
                {title}
              </h2>
              <p className="mt-4 text-lg text-gray-500">{description}</p>
            </div>
          </div>
        </div>
        {props.pictureSrc && <SectionPicture src={props.pictureSrc} />}
      </div>
    </div>
  );
};
export default SectionItem;
