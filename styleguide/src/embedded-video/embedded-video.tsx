import React from "react";

type EmbeddedVideoProps = {
  link: string;
  width: number;
  height: number;
};

export const EmbeddedVideo = ({ link, width, height }: EmbeddedVideoProps) => {
  return (
    <div className="flex items-center justify-center ">
      <iframe
        width={width} //"560"
        height={height} // "315"
        src={link}
        title="YouTube video player"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"

        allowfullscreen="true"
      ></iframe>
    </div>
  );
};
