import clsx from "clsx";
import React from "react";
import { getBackgroundClasses } from "../colors-utils";
import { Text } from "../text";
import { Color } from "../types";

type Props = {
  image?: string;
  letter?: string;
  letterBackgroundColor?: Color | "none";
  alt?: string;
};

export const Avatar = ({
  image,
  letter,
  letterBackgroundColor = "none",
  alt,
}: Props) => {
  return (
    <div className="w-8 h-8 rounded-full select-none">
      {image && (
        <img
          loading="lazy"
          className="w-full h-full rounded-full border-1"
          src={image}
          alt={alt}
        />
      )}
      {!image && letter && (
        <div
          className={clsx(
            "w-full h-full rounded-full border-1 flex items-center justify-center",
            {
              ...getBackgroundClasses(letterBackgroundColor),
            }
          )}
        >
          <Text weight="strong" size="label3">
            {letter[0]}
          </Text>
        </div>
      )}
    </div>
  );
};
