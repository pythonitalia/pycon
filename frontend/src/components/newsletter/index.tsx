import React from "react";
import { useMailchimp } from "react-use-mailchimp";

const url = "";

export const NewsletterForm: React.SFC = props => {
  const [mailchimp, subscribe] = useMailchimp({
    url,
  });
  return (
    <>
      <h1>Inscriviti alla newsletter</h1>
    </>
  );
};
