import React from "react";

type Props = {
  children: React.ReactNode;
  overlayStyle?: any;
  contentStyle?: any;
  overlayAs?: React.ElementType;
};

export const FullscreenOverlay = ({
  children,
  overlayStyle,
  contentStyle,
  overlayAs,
}: Props) => {
  const OverlayComponent = overlayAs ?? "div";

  return (
    <div className="fixed inset-0 z-20">
      <OverlayComponent
        style={overlayStyle}
        className="absolute inset-0 z-10 transition-opacity bg-black bg-opacity-75"
      />
      <div style={contentStyle} className="relative z-20 flex justify-center">
        {children}
      </div>
    </div>
  );
};
