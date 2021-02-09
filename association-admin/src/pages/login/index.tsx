import { useFormState } from "react-use-form-state";

import Head from "next/head";
import { useRouter } from "next/router";

import { Alert } from "~/components/alert";
import { Button } from "~/components/button";
import { Card } from "~/components/card";
import { Heading } from "~/components/heading";
import { Input } from "~/components/input";
import { getMergedErrors } from "~/helpers/errors";

import { useLoginMutation } from "./login.generated";

type LoginForm = {
  email: string;
  password: string;
};

const Login = () => {
  const [formState, { email, password }] = useFormState<LoginForm>();
  const [{ fetching, data }, login] = useLoginMutation();
  const { replace } = useRouter();

  const submitLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    const result = await login({
      input: {
        email: formState.values.email,
        password: formState.values.password,
      },
    });

    if (result.data.login.__typename === "LoginSuccess") {
      localStorage.setItem("token", result.data.login.token);
      replace("/dashboard/users");
    }
  };

  return (
    <>
      <Head>
        <title>Login</title>
      </Head>

      <div className="flex flex-col w-full justify-center bg-gray-100">
        <div className="mx-auto w-full max-w-md">
          <Heading align="center">Sign in to your account</Heading>
        </div>
        <Card>
          <form className="space-y-6" onSubmit={submitLogin}>
            <Input
              errorMessage={getMergedErrors(
                data?.login.__typename === "LoginValidationError" &&
                  data?.login.errors.email,
              )}
              {...email("email")}
              label="Email address"
              required
            />

            <Input
              errorMessage={getMergedErrors(
                data?.login.__typename === "LoginValidationError" &&
                  data?.login.errors.password,
              )}
              {...password("password")}
              label="Password"
              required
            />

            <Button>
              {fetching && `Please wait`}
              {!fetching && `Sign in`}
            </Button>

            {data && data.login.__typename === "WrongEmailOrPassword" && (
              <Alert>Invalid email and password</Alert>
            )}
          </form>
        </Card>
      </div>
    </>
  );
};

export default Login;
