import React from "react";
import { Avatar } from "../avatar/avatar";
import { AvatarGroup } from "./avatar-group";

export default {
  title: "Avatar Group",
  parameters: {
    layout: "centered",
  },
};

export const Primary = () => {
  return (
    <AvatarGroup>
      <Avatar image="https://images.unsplash.com/photo-1541257710737-06d667133a53?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=900&ixid=MnwxfDB8MXxyYW5kb218MHx8ZmFjZSx3b21hbix5b3VuZ3x8fHx8fDE2NzY0ODg1Nzc&ixlib=rb-4.0.3&q=80&w=900" />
      <Avatar image="https://images.unsplash.com/photo-1620504155085-d7b152a58e77?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=900&ixid=MnwxfDB8MXxyYW5kb218MHx8ZmFjZSx3b21hbix5b3VuZ3x8fHx8fDE2NzY0ODg1ODM&ixlib=rb-4.0.3&q=80&w=900" />
      <Avatar image="https://images.unsplash.com/photo-1502823403499-6ccfcf4fb453?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=900&ixid=MnwxfDB8MXxyYW5kb218MHx8ZmFjZSx3b21hbix5b3VuZ3x8fHx8fDE2NzY0ODg1OTM&ixlib=rb-4.0.3&q=80&w=900" />
      <Avatar letter="Marco" letterBackgroundColor="coral" />
      <Avatar letter="Ester" letterBackgroundColor="blue" />
    </AvatarGroup>
  );
};
