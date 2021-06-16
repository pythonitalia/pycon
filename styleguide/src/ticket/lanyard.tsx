import React from "react";

export const Lanyard = () => {
  return (
    <div className="flex flex-col items-center justify-center w-full">
      <div className="z-30 h-1 origin-bottom ticket:scale-y-150 scale-y-10000 ticket:h-24 transform-gpu w-14 bg-cornflower-blue" />
      <div className="z-30 h-10 -mt-2 transform-gpu rounded-b-md w-14 bg-cornflower-blue" />

      <div
        style={{
          clipPath:
            "polygon(92.5% -26px, 97px -1px, 96px 28px, 61.25% 50%, 63.75% 130.36%, -30px 55.36%, 0px 0px)",
        }}
        className="z-20 w-20 -mt-5 border-4 rounded-full h-14 border-grey"
      />
    </div>
  );
};
