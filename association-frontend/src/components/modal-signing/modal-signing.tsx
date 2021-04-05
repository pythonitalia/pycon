import classnames from "classnames";
import React, { useState } from "react";
import { useFormState } from "react-use-form-state";

import { getMessageForError, isErrorTypename } from "~/helpers/errors-to-text";

import { Alert, Variant } from "../alert/alert";
import Button from "../button/button";
import Input from "../input/input";
import Modal from "../modal/modal";
import { useLoginMutation } from "./login.generated";
import { useRegisterMutation } from "./register.generated";

type ModalSigningProps = {
  showModal: boolean;
  closeModalHandler?: () => void;
};

type SigningForm = {
  email: string;
  password: string;
};

const ModalSigning: React.FC<ModalSigningProps> = ({
  showModal,
  closeModalHandler,
}) => {
  const [formState, { email, password }] = useFormState<SigningForm>();
  // login or signup
  const [isLoggingIn, setIsLoggingIn] = useState(true);
  const [loginData, login] = useLoginMutation();
  const [registerData, register] = useRegisterMutation();

  const submitLogin = async () => {
    const result = await login({
      input: {
        email: formState.values.email,
        password: formState.values.password,
      },
    });

    if (result.data.login.__typename === "LoginSuccess") {
      window.dispatchEvent(new Event("userLoggedIn"));
      closeModalHandler();
    }
  };

  const submitRegister = async () => {
    const result = await register({
      input: {
        email: formState.values.email,
        password: formState.values.password,
      },
    });

    if (result.data.register.__typename === "RegisterSuccess") {
      console.log("register success!");
      closeModalHandler();
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isLoggingIn) {
      submitLogin();
    } else {
      submitRegister();
    }
  };

  const isRunningMutation = loginData.fetching || registerData.fetching;
  const mutationResultTypename = isLoggingIn
    ? loginData.data?.login?.__typename
    : registerData.data?.register?.__typename;
  const operationFailed = isErrorTypename(mutationResultTypename);

  return (
    <Modal
      className="items-center"
      showModal={showModal}
      closeModalHandler={closeModalHandler}
    >
      <h3
        className="mb-6 text-3xl text-center font-extrabold text-gray-900"
        id="modal-title"
      >
        {isLoggingIn && "Accedi al tuo account Python Italia"}
        {!isLoggingIn && "Entra nella community di Python Italia"}
      </h3>

      <form className="flex flex-col max-w-sm mx-auto" onSubmit={handleSubmit}>
        <div className="mb-5 flex flex-col">
          <Input required placeholder="Email" {...email("email")} />
          <div className="place-self-start">
            <a
              href="#"
              className="underline mt-1 block text-bluecyan hover:text-yellow "
              onClick={(e) => {
                e.preventDefault();
                setIsLoggingIn(!isLoggingIn);
              }}
            >
              {isLoggingIn ? "Non hai un account?" : "Hai già un account?"}
            </a>
          </div>
        </div>

        <div className="mb-7 flex flex-col">
          <Input
            placeholder={"Password"}
            type={"password"}
            required
            {...password("password")}
          />
          <div
            className={classnames("place-self-start", {
              "opacity-0": !formState.values.email,
            })}
          >
            <a
              href="#"
              className="underline text-left mt-1 block text-bluecyan hover:text-yellow"
            >
              Hai dimenticato la password?
            </a>
          </div>
        </div>

        {isRunningMutation && <Alert variant={Variant.INFO}>Please wait</Alert>}
        {operationFailed && mutationResultTypename && (
          <Alert variant={Variant.ERROR}>
            {getMessageForError(mutationResultTypename)}
          </Alert>
        )}

        <div>
          <Button text={isLoggingIn ? "Accedi" : "Registrati"} />
        </div>
      </form>
    </Modal>
  );
};

export default ModalSigning;
