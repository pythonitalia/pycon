import * as React from "react";

export const SnakeBody = (props: React.SVGProps<SVGSVGElement>) => {
  return (
    <svg width={311} height={102} viewBox="0 0 311 102" fill="none" {...props}>
      <g clipPath="url(#prefix__clip0_438_22076)">
        <path
          d="M291.95 2.902H3V52.01c19.438 18.728 51.432 18.587 70.886-.142 19.454-18.728 58.323-18.728 77.777 0 19.454 18.729 58.369 18.729 77.8 0 19.43-18.728 58.322-18.728 77.776 0h.632V2.902c0-.052-14.436-.005-15.921 0z"
          fill="#FCE8DE"
        />
        <path
          d="M73.886 51.867c19.454-18.728 58.347-18.728 77.777 0 19.431 18.729 58.346 18.729 77.8 0 19.454-18.728 58.323-18.728 77.777 0h.632V99v-.006c-.012-.037-.507.006-16.044.006H3V52.01c19.454 18.728 51.448 18.562 70.886-.142z"
          fill="#F17A5D"
        />
        <path
          d="M3 2.901h288.828c.047 0 16.044-.055 16.044 0V99"
          stroke="#0E1116"
          strokeWidth={5}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M307.872 99c0-.047.265 0-16.044 0H3V3.01m304.239 48.858c-19.453-18.729-58.346-18.729-77.776 0-19.431 18.728-58.346 18.728-77.8 0-19.454-18.729-58.323-18.729-77.777 0C54.432 70.596 22.438 73.237 3 54.51"
          stroke="#0E1116"
          strokeWidth={5}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </g>
      <defs>
        <clipPath id="prefix__clip0_438_22076">
          <path fill="#fff" transform="rotate(-90 51 51)" d="M0 0h102v311H0z" />
        </clipPath>
      </defs>
    </svg>
  );
};
