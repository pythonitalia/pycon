import React, { useState } from "react";

import { SectionItem } from "~/components/section-item";
import { useStripe } from "~/hooks/use-stripe";
import { useUser } from "~/hooks/use-user";

import { Button } from "../button";
import { ModalSigning } from "../modal-signing";
import { useManageSubscriptionMutation } from "./manage-subscription.generated";
import { useSubscribeMutation } from "./subscribe.generated";

const SignUpOrSignIn = ({ toggleModal }) => {
  return (
    <SectionItem
      title={"Unisciti ora"}
      textTheme={"white"}
      withBackground={true}
      backgroundImageClass={"bg-reception-desk-pycon-10"}
    >
      <div className="lg:flex-shrink-0">
        <div className="inline-flex rounded-md shadow">
          <Button text={"Unisciti ora"} onClick={toggleModal} />
        </div>
      </div>
    </SectionItem>
  );
};

const BecameMember = () => {
  const { redirectToCheckout } = useStripe();
  const [{}, subscribeMutation] = useSubscribeMutation();

  const subscribe = async () => {
    const result = await subscribeMutation();
    if (
      result?.data.subscribeUserToAssociation.__typename === "CheckoutSession"
    ) {
      const stripeSessionId =
        result.data.subscribeUserToAssociation.stripeSessionId;
      redirectToCheckout(stripeSessionId);
    }
  };

  return (
    <SectionItem
      title={"Iscriviti all'assaciozione"}
      textTheme={"white"}
      withBackground={true}
      backgroundImageClass={"bg-reception-desk-pycon-10"}
    >
      <div className="lg:flex-shrink-0">
        <div className="inline-flex rounded-md shadow">
          <Button text={"Iscriviti ora"} onClick={subscribe} />
        </div>
      </div>
    </SectionItem>
  );
};

const ManageSubscription = () => {
  const [{}, manageSubsriptionMutation] = useManageSubscriptionMutation();
  const onClick = async () => {
    const result = await manageSubsriptionMutation();
    if (
      result?.data.manageUserSubscription.__typename == "CustomerPortalResponse"
    ) {
      window.location.href =
        result.data.manageUserSubscription.billingPortalUrl;
    }
  };

  return (
    <SectionItem
      title={"Gestisci la tua iscrizione"}
      textTheme={"white"}
      withBackground={true}
      backgroundImageClass={"bg-reception-desk-pycon-10"}
    >
      <div className="lg:flex-shrink-0">
        <div className="inline-flex rounded-md shadow">
          <Button text={"Gestisci la tua iscrizione"} onClick={onClick} />
        </div>
      </div>
    </SectionItem>
  );
};

export const SectionJoin = () => {
  const { user } = useUser();

  const [showModal, setShowModal] = useState(false);
  const toggleModal = () => {
    setShowModal(!showModal);
  };

  return (
    <>
      <ModalSigning showModal={showModal} closeModalHandler={toggleModal} />
      {!user && <SignUpOrSignIn toggleModal={toggleModal} />}
      {user && !user.isPythonItaliaMember && <BecameMember />}
      {user && user.isPythonItaliaMember && <ManageSubscription />}
    </>
  );
};
