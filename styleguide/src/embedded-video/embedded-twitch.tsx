import React from "react";

type EmbeddedVideoProps = {
  channel: string;
  autoplay?: boolean;
  width: number;
  height: number;
};

export const EmbeddedTwitch = ({ channel, autoplay=false, width, height }: EmbeddedVideoProps) => {
  return (
    <div className="flex items-center justify-center ">
      <iframe
        width={width} //"560"
        height={height} // "315"
        src={"https://player.twitch.tv/?channel="+channel+"&parent=localhost" + "&autoplay="+autoplay}
        title="YouTube video player"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"

        allowfullscreen="true"
      ></iframe>
    </div>
  );
};
