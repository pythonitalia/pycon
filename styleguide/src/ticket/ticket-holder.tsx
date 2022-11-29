import React from "react";

type Props = {
  children: React.ReactNode;
};

export const TicketHolder = React.forwardRef<HTMLDivElement, Props>(
  ({ children }, ref) => (
    <div
      ref={ref}
      className="relative z-10 px-4 pb-4 bg-white shadow-xl pt-14 ticket:pt-20 -mt-7 rounded-xl"
    >
      {/* large */}
      <div className="absolute w-16 h-5 rounded-xl top-4 left-11 ticket:left-1/4 bg-coral"></div>

      {/* round one */}
      <div className="absolute w-5 h-5 transform -translate-x-1/2 rounded-full top-4 bg-coral left-1/2"></div>

      {/* large */}
      <div className="absolute w-16 h-5 rounded-xl top-4 right-11 ticket:right-1/4 bg-coral"></div>

      {children}
    </div>
  )
);
