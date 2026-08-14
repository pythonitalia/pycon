import { Link } from "@inertiajs/react";

import { LoginForm } from "@/components/login-form";

export default function Login({
  nextUrl,
  privacyPolicyUrl,
  resetPasswordUrl,
}: {
  nextUrl: string;
  privacyPolicyUrl: string;
  resetPasswordUrl: string;
}) {
  return (
    <main className="isolate flex min-h-dvh flex-col items-center justify-center gap-6 bg-muted p-6 antialiased md:p-10">
      <div className="flex w-full max-w-sm flex-col gap-6">
        <Link
          className="flex items-center gap-2 self-center font-medium"
          href="/dashboard"
        >
          <div
            aria-hidden="true"
            className="flex size-6 items-center justify-center rounded-md bg-primary text-xs font-semibold text-primary-foreground tabular-nums"
          >
            Py
          </div>
          PyCon Italia Dashboard
        </Link>
        <LoginForm
          nextUrl={nextUrl}
          privacyPolicyUrl={privacyPolicyUrl}
          resetPasswordUrl={resetPasswordUrl}
        />
      </div>
    </main>
  );
}
