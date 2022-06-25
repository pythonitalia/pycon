import classnames from "classnames";

type OverlayTheme = "black" | "white" | "black-light";

type BackgroundWrapperProps = {
  id?: string;
  backgroundImageClass: string;
  overlayTheme: OverlayTheme;
  overlay?: boolean;
};

type InnerContentProps = {
  id?: string;
  title?: string;
  subTitle?: string;
  textTheme?: "black" | "white";
};

type SectionItemProps = {
  id?: string;
  title?: string;
  subTitle?: string;
  withBackground?: boolean;
  textTheme?: "black" | "white";

  // background classes
  backgroundImageClass?: string;
  overlay?: boolean;
  overlayTheme?: OverlayTheme;
};

const BackgroundWrapper = ({
  backgroundImageClass,
  overlay,
  overlayTheme,
  children,
  id,
}: React.PropsWithChildren<BackgroundWrapperProps>) => {
  return (
    <div
      className={classnames(
        "relative bg-cover bg-center bg-local bg-no-repeat h-screen flex items-center justify-center",
        backgroundImageClass,
      )}
      id={id}
    >
      {overlay && (
        <div
          className={classnames("absolute top-0 left-0 bottom-0 right-0", {
            "bg-black bg-opacity-30": overlayTheme === "black-light",
            "bg-black bg-opacity-70": overlayTheme === "black",
            "bg-white bg-opacity-70": overlayTheme === "white",
          })}
        ></div>
      )}

      <div className="flex content-center max-w-4xl px-5 m-auto text-center">
        <div className="z-10 content-start top-3">{children}</div>
      </div>
    </div>
  );
};

const InnerContent = ({
  title,
  subTitle,
  textTheme,
  children,
  id,
}: React.PropsWithChildren<InnerContentProps>) => {
  return (
    <div id={id} className={classnames("bg-transparent")}>
      <div className="max-w-full mx-auto md:max-w-xl">
        <div className="text-center">
          {title && (
            <p
              className={classnames(
                "my-4 text-3xl leading-8 font-extrabold tracking-tight sm:text-4xl",
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
            <p className="max-w-2xl mx-auto mb-4 text-xl text-gray-500">
              {subTitle}
            </p>
          )}
          {children}
        </div>
      </div>
    </div>
  );
};

export const SectionItem = ({
  withBackground = false,
  backgroundImageClass = "bg-pycon-group",
  overlay = true,
  overlayTheme = "black",
  id,
  ...props
}: React.PropsWithChildren<SectionItemProps>) => {
  if (withBackground) {
    return (
      <BackgroundWrapper
        id={id}
        backgroundImageClass={backgroundImageClass}
        overlay={overlay}
        overlayTheme={overlayTheme}
      >
        <InnerContent {...props} />
      </BackgroundWrapper>
    );
  }
  return <InnerContent id={id} {...props} />;
};
