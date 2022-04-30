import clsx from "clsx";
import React from "react";

export const SpeakerSquare = ({
  name,
  subtitle,
  portraitUrl,
  className,
  linkWrapper,
}: {
  name: string;
  subtitle?: string;
  portraitUrl: string;
  className?: string;
  linkWrapper?: React.ReactNode;
}) => {
  const Wrapper: any = linkWrapper ? linkWrapper : <div />;

  return (
    <div className="aspect-w-1 aspect-h-1">
      <img
        src={portraitUrl}
        className="absolute top-0 left-0 w-full h-full filter grayscale brightness-75 object-cover"
      />
      {React.cloneElement(
        Wrapper,
        {
          className: "aspect-w-1 aspect-h-1",
        },
        <React.Fragment>
          <div
            className={clsx(
              "absolute top-0 left-0 w-full h-full opacity-50 blend-lighten",
              className
            )}
          />
          <div className="p-8 text-white font-medium flex justify-end flex-col">
            <p className="uppercase text-2xl">{name}</p>
            {subtitle ? <p className="text-lg">{subtitle}</p> : null}
          </div>
        </React.Fragment>
      )}
    </div>
  );
};
