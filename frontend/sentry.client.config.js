import * as Sentry from "@sentry/nextjs";

const SENTRY_DSN = process.env.SENTRY_DSN || process.env.NEXT_PUBLIC_SENTRY_DSN;

Sentry.init({
  dsn: SENTRY_DSN,
  tracesSampleRate: 0.4,
  replaysSessionSampleRate: 0.2,
  replaysOnErrorSampleRate: 1.0,
  integrations: [new Sentry.Replay(), new Sentry.BrowserTracing()],
});
