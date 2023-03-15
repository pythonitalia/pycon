import {
  Separator,
  Spacer,
  SplitSection,
} from "@python-italia/pycon-styleguide";
import {
  SnakeLetter,
  SnakePencil,
} from "@python-italia/pycon-styleguide/illustrations";
import React from "react";

type Props = {
  children: React.ReactNode;
  bottomSection?: React.ReactNode;
  illustration?: "pencil" | "email" | "none";
};

export const LoginFlowLayout = ({
  children,
  bottomSection,
  illustration = "pencil",
}: Props) => {
  const IllustrationComponent = getIllustrationComponent(illustration);

  return (
    <SplitSection
      sideContent={<IllustrationComponent />}
      sideContentType="other"
      hideSideContentOnMobile={true}
      sideContentPadding={false}
      sideContentClassName="justify-center"
      contentSpacing="medium"
      className="justify-between"
    >
      <div className="lg:max-w-[650px] w-full">
        <Spacer size="2xl" />
        {children}
        {bottomSection && (
          <div className="mt-auto w-full">
            <Spacer size="3xl" />
            <Separator />
            <Spacer size="2md" />
            <div className="flex flex-col-reverse gap-4 text-center md:text-left md:flex-row justify-between items-center">
              {bottomSection}
            </div>
          </div>
        )}
      </div>
    </SplitSection>
  );
};

const getIllustrationComponent = (illustration: Props["illustration"]) => {
  switch (illustration) {
    case "pencil":
      return SnakePencil;
    case "email":
      return SnakeLetter;
    default:
      return "div";
  }
};
