import classnames from "classnames";

type BackgroundWrapperProps = {
  backgroundImageClass: string;
  overlayTheme: "black" | "white";
  overlay?: boolean;
};

type InnerContentProps = {
  title?: string;
  subTitle?: string;
  textTheme?: "black" | "white";
};

type SectionItemProps = {
  title?: string;
  subTitle?: string;
  withBackground?: boolean;
  textTheme?: "black" | "white";

  // background classes
  backgroundImageClass?: string;
  overlay?: boolean;
  overlayTheme?: "black" | "white";
};

const BackgroundWrapper: React.FC<BackgroundWrapperProps> = ({
  backgroundImageClass,
  overlay,
  overlayTheme,
  children,
}) => {
  return (
    <div
      className={classnames(
        "relative bg-cover bg-center bg-local bg-no-repeat h-screen",
        backgroundImageClass,
      )}
    >
      {overlay && (
        <div
          className={classnames("absolute top-0 left-0 bottom-0 right-0", {
            "bg-black bg-opacity-60": overlayTheme === "black",
            "bg-white bg-opacity-60": overlayTheme === "white",
          })}
        ></div>
      )}

      <div className="absolute top-2/4 left-2/4 transform -translate-x-1/2 -translate-y-1/2">
        <div className="max-w-4xl m-auto flex content-center text-center  ">
          <div className="content-start z-10 top-3 ">{children}</div>
        </div>
      </div>
    </div>
  );
};

const InnerContent: React.FC<InnerContentProps> = ({
  title,
  subTitle,
  textTheme,
  children,
}) => {
  return (
    <div className={classnames("bg-transparet")}>
      <div className="max-w-7xl mx-auto">
        <div className="text-center">
          {title && (
            <p
              className={classnames(
                "my-4 text-3xl leading-8 font-extrabold tracking-tight  sm:text-4xl",
                {
                  "text-gray-900": textTheme === "black",
                  "text-white": textTheme === "white",
                },
              )}
            >
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

const SectionItem: React.FC<SectionItemProps> = ({
  withBackground = false,
  backgroundImageClass = "bg-pycon-group",
  overlay = true,
  overlayTheme = "black",
  ...props
}) => {
  console.log({ withBackground, backgroundImageClass });
  if (withBackground) {
    return (
      <BackgroundWrapper
        backgroundImageClass={backgroundImageClass}
        overlay={overlay}
        overlayTheme={overlayTheme}
      >
        <InnerContent {...props} />
      </BackgroundWrapper>
    );
  }
  return <InnerContent {...props} />;
};
export default SectionItem;
