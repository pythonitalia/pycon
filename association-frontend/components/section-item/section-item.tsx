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
    <div className="py-6 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          {title && (
            <p className="text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              {title}
            </p>
          )}
          {subTitle && (
            <p className="mt-4 max-w-2xl text-xl text-gray-500 mx-auto">
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
