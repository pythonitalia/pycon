import React from "react";

type EmbeddedTwitchProps = {
  channel: string;
  autoplay?: boolean;
  width: number;
  height: number;
  parent?: string;
};

export const EmbeddedTwitch = ({ channel, autoplay=false, width, height, parent="localhost" }: EmbeddedTwitchProps) => {
  return (
    <div className="flex items-center justify-center ">
      <iframe
        width={width}
        height={height}
        src={`https://player.twitch.tv/?channel=${channel}&parent=${parent}&autoplay=${autoplay}`}
        title="YouTube video player"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"

        allowfullscreen="true"
      ></iframe>
    </div>
  );
};
