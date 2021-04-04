import React, { useState } from "react";
import { useFormState } from "react-use-form-state";

import Button from "../button/button";
import GoogleIcon from "../icons/google";
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
  const [{ fetching, data }, login] = useLoginMutation();
  const [registerData, register] = useRegisterMutation();
  console.log({ fetching, data, registerData });

  const submitLogin = async () => {
    const result = await login({
      input: {
        email: formState.values.email,
        password: formState.values.password,
      },
    });
    console.log({
      email: formState.values.email,
      password: formState.values.password,
    });
    console.log(result);

    if (result.data.login.__typename === "LoginSuccess") {
      window.dispatchEvent(new Event("userLoggedIn"));
      closeModalHandler();
    }
  };
  console.log({ fetching, data, registerData });

  const submitRegister = async () => {
    const result = await register({
      input: {
        email: formState.values.email,
        password: formState.values.password,
      },
    });

    console.log({
      email: formState.values.email,
      password: formState.values.password,
    });
    console.log(result);

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

  return (
    <Modal showModal={showModal} closeModalHandler={closeModalHandler}>
      <div className="items-center">
        <h3
          className="mb-6 text-3xl text-center font-extrabold text-gray-900"
          id="modal-title"
        >
          {isLoggingIn && "Accedi al tuo account Python Italia"}
          {!isLoggingIn && "Entra nella community di Python Italia!"}
        </h3>

        <div className="flex flex-col max-w-sm mx-auto">
          <div className="mb-5 flex flex-col">
            <Input placeholder="Email" {...email("email")} />
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
              {...password("password")}
            />
            <div className="place-self-start">
              <a
                href="#"
                className="underline mt-1 block text-bluecyan hover:text-yellow"
              >
                Hai dimenticato la password?
              </a>
            </div>
          </div>

          <div>
            <Button
              text={isLoggingIn ? "Accedi" : "Registrati"}
              onClick={handleSubmit}
            />
          </div>
          {/* <div className="mb-4 relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white text-gray-500">
                Or continue with
              </span>
            </div>
          </div>

          <button className="flex justify-center appearance-none rounded-none px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-bluecyan focus:z-10 sm:text-xl rounded-t-md rounded-b-md ">
            <div className="px-3 flex items-right">
              <GoogleIcon />
            </div>

            <div className="text-gray-900">
              <a href="#" className="select-none">
                Continua con google
              </a>
            </div>
          </button> */}
        </div>
      </div>
    </Modal>
  );
  return null;
};

export default ModalSigning;
