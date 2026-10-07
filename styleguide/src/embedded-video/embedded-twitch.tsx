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
      <iframe
        className="w-full h-full"
        width="100%"
        height="100%"
        src={`https://player.twitch.tv/?channel=${channel}&parent=${parent}&autoplay=${autoplay}`}
        title="Twitch video player"
        frameBorder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen={true}
      ></iframe>
  );
};
