import * as React from "react";

export const TShirtIcon = (props: React.SVGProps<SVGSVGElement>) => {
  return (
    <svg width={32} height={32} fill="none" viewBox="0 0 32 32" {...props}>
      <path
        d="M24.676 3h-4.225c-1.338 6.056-8.662 4.507-9.155 0H7.634L2 8.634l4.085 4.084 1.267-1.267V28h17.324V11.45l1.62 1.268 4.014-4.084L24.676 3z"
        stroke="#0E1116"
        strokeWidth={2}
      />
    </svg>
  );
};
