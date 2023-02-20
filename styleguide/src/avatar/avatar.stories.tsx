import React from "react";
import { Avatar } from "./avatar";

export default {
  title: "Avatar",
  parameters: {
    layout: "centered",
  },
};

export const Primary = () => {
  return (
    <>
      <Avatar
        alt="Speaker avatar"
        image="https://images.unsplash.com/photo-1532170579297-281918c8ae72?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=900&ixid=MnwxfDB8MXxyYW5kb218MHx8ZmFjZSx3b21hbix5b3VuZ3x8fHx8fDE2NzY0ODc5MzE&ixlib=rb-4.0.3&q=80&w=900"
      />
      <Avatar
        alt="Speaker avatar"
        letter="Marco Acierno"
        letterBackgroundColor="coral"
      />
    </>
  );
};
