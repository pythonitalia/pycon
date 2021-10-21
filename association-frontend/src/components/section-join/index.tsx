import React, { useEffect, useState } from "react";

import { useRouter } from "next/router";

import { Button } from "~/components/button";
import { ModalSigning } from "~/components/modal-signing";
import { SectionItem } from "~/components/section-item";
import { useStripe } from "~/hooks/use-stripe";
import { useUser } from "~/hooks/use-user";

import { SimpleModal } from "../simple-modal";
import { useManageSubscriptionMutation } from "./manage-subscription.generated";
import { useSubscribeMutation } from "./subscribe.generated";

const SignUpOrSignIn = () => {
  const [showModal, setShowModal] = useState(false);
  const toggleModal = () => {
    setShowModal(!showModal);
  };

  return (
    <>
      <ModalSigning showModal={showModal} closeModalHandler={toggleModal} />

      <SectionItem
        id="membership"
        title={"Diventa membro"}
        textTheme={"white"}
        withBackground={true}
        backgroundImageClass={"bg-reception-desk-pycon-10"}
      >
        <BecomeMemberMainCopy />
        <p className="mx-auto mb-4 text-xl text-white">
          Per poter diventare membro, hai bisogno di un account!
          <br />
          Clicca il pulsante in basso per creare un account o loggarti.
          <br />
          <br />
          Se hai già un account pycon.it, puoi loggarti direttamente con la
          stessa email/password!
        </p>

        <div className="lg:flex-shrink-0">
          <div className="inline-flex rounded-md shadow">
            <Button text="Crea un account" onClick={toggleModal} />
          </div>
        </div>
      </SectionItem>
    </>
  );
};

const BecameMember = () => {
  const { redirectToCheckout } = useStripe();
  const [{ fetching }, subscribeMutation] = useSubscribeMutation();

  const subscribe = async () => {
    const result = await subscribeMutation();
    if (
      result?.data?.subscribeUserToAssociation.__typename === "CheckoutSession"
    ) {
      const stripeSessionId =
        result.data.subscribeUserToAssociation.stripeSessionId;
      redirectToCheckout(stripeSessionId);
    }
  };

  return (
    <SectionItem
      id="membership"
      title={"Diventa membro Python Italia"}
      textTheme={"white"}
      withBackground={true}
      backgroundImageClass={"bg-reception-desk-pycon-10"}
    >
      <BecomeMemberMainCopy />
      <div className="lg:flex-shrink-0">
        <div className="inline-flex rounded-md shadow">
          <Button
            text={"Iscriviti ora"}
            onClick={subscribe}
            loading={fetching}
          />
        </div>
      </div>
    </SectionItem>
  );
};

const BecomeMemberMainCopy = () => (
  <p className="mx-auto mb-4 text-xl text-white">
    Python Italia esiste principalmente grazie al supporto di volontari!
    <br />
    Diventa membro dell'associazione per contribuire alla crescita di Python
    Italia e le community Python locali.
  </p>
);

const ManageSubscription = () => {
  const [{ data: _ }, manageSubscriptionMutation] =
    useManageSubscriptionMutation();
  const onClick = async () => {
    const result = await manageSubscriptionMutation();
    if (
      result?.data.manageUserSubscription.__typename == "CustomerPortalResponse"
    ) {
      window.location.href =
        result.data.manageUserSubscription.billingPortalUrl;
    }
  };

  return (
    <SectionItem
      id="membership"
      title={"Gestisci la tua iscrizione"}
      textTheme={"white"}
      withBackground={true}
      backgroundImageClass={"bg-reception-desk-pycon-10"}
    >
      <p className="mx-auto mb-4 text-xl text-white">
        Grazie per il tuo supporto! 🙌 <br />
        Puoi gestire la tua iscrizione all'associazione usando questo pulsante:
      </p>

      <div className="lg:flex-shrink-0">
        <div className="inline-flex rounded-md shadow">
          <Button text={"Gestisci iscrizione"} onClick={onClick} />
        </div>
      </div>
    </SectionItem>
  );
};

const MembershipStatusModal = () => {
  const { query } = useRouter();
  const [modalAlreadyClosed, setModalAlreadyClosed] = useState(false);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    if (modalAlreadyClosed) {
      return;
    }

    const membershipStatus = query["membership-status"];
    setShowModal(Boolean(membershipStatus && membershipStatus === "success"));
  }, [query]);

  return (
    <SimpleModal
      showModal={showModal}
      closeModal={() => {
        setShowModal(false);
        setModalAlreadyClosed(true);
      }}
      title="🙌"
    >
      Grazie per esserti iscritto a Python Italia! 🎉
    </SimpleModal>
  );
};

export const SectionJoin = () => {
  const { user } = useUser();

  return (
    <>
      <MembershipStatusModal />
      {!user && <SignUpOrSignIn />}
      {user && !user.isPythonItaliaMember && <BecameMember />}
      {user && user.isPythonItaliaMember && <ManageSubscription />}
    </>
  );
};
