import React from "react";

type EmbeddedTwitchProps = {
  channel: string;
  backgroundColor?: string;
  autoplay?: boolean;
  parent?: string;
};

export const EmbeddedTwitch = ({
  channel,
  backgroundColor = "white",
  autoplay = false,
  parent = "localhost",
}: EmbeddedTwitchProps) => {
  return (
    <div
      className={`flex items-center justify-center w-full h-full bg-${backgroundColor}`}
    >
      <div className="relative w-2/3 h-full pt-xl ">
        <iframe
          className="absolute top-0 w-full h-full"
          width="100%"
          height="100%"
          src={`https://player.twitch.tv/?channel=${channel}&parent=${parent}&autoplay=${autoplay}`}
          title="YouTube video player"
          frameBorder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen={true}
        ></iframe>
      </div>
    </div>
  );
};
