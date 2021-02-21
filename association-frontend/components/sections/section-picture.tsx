import clsx from "clsx";

type SectionPictureProps = {
  src: string;
  reverse?: boolean;
};

const SectionPicture: React.FC<SectionPictureProps> = ({
  src,
  reverse = false,
}) => {
  return (
    <div
      className={clsx(
        "mt-12 sm:mt-16 lg:mt-0",
        reverse ? "lg:col-start-1" : "",
      )}
    >
      <div className="pl-4 -mr-48 sm:pl-6 md:-mr-16 lg:px-0 lg:m-0 lg:relative lg:h-full">
        <img
          className="w-full rounded-xl shadow-xl ring-1 ring-black ring-opacity-5 lg:absolute lg:left-0 lg:h-full lg:w-auto lg:max-w-none"
          src={src}
          alt="Inbox user interface"
        />
      </div>
    </div>
  );
};
export default SectionPicture;
