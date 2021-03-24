type SectionItemProps = {
  title?: string;
  subTitle?: string;
};
const SectionItem: React.FC<SectionItemProps> = ({
  title,
  subTitle,
  children,
}) => {
  return (
    <div className="my-16 bg-white">
      <div className="max-w-4xl mx-auto">
        <div className="text-center">
          {title && (
            <p className="my-4 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              {title}
            </p>
          )}
          {subTitle && (
            <p className="mb-4 max-w-2xl text-xl text-gray-500 mx-auto">
              {subTitle}
            </p>
          )}
          {children}
        </div>
      </div>
    </div>
  );
};
export default SectionItem;
