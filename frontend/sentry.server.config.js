import * as Sentry from "@sentry/nextjs";

import { sentryConfig } from "./sentry";

Sentry.init(sentryConfig);
