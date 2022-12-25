import React from "react";

export const SideText = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="px-4 py-3.5 lg:px-6 flex items-center gap-3">
      {children}
    </div>
  );
};
