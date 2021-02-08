import Head from "next/head";

import { Button } from "~/components/button";
import { Card } from "~/components/card";
import { Heading } from "~/components/heading";
import { Input } from "~/components/input";

const Login = () => (
  <>
    <Head>
      <title>Login</title>
    </Head>

    <div className="flex flex-col w-full justify-center bg-gray-100">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <Heading align="center">Sign in to your account</Heading>
      </div>
      <Card>
        <form className="space-y-6">
          <Input
            id="email"
            type="email"
            name="email"
            label="Email address"
            autoComplete="email"
          />

          <Input
            id="password"
            type="password"
            name="password"
            label="Password"
            autoComplete="password"
          />

          <Button>Sign in</Button>

          {true && (
            <div className="rounded-md bg-red-50 p-4">
              <div className="flex">
                <div className="flex-shrink-0">aaa</div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">aa</h3>
                </div>
              </div>
            </div>
          )}
        </form>
      </Card>
    </div>
  </>
);

export default Login;
