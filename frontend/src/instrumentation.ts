import * as Sentry from "@sentry/nextjs";

export async function register() {
  if (process.env.NEXT_RUNTIME === "nodejs") {
    await import("../sentry.server.config");
  }

  if (process.env.NEXT_RUNTIME === "edge") {
    await import("../sentry.edge.config");
  }

  if (
    process.env.NEXT_RUNTIME === "nodejs" &&
    process.env.NEXT_MANUAL_SIG_HANDLE
  ) {
    const fs = await import("fs");

    process.on("SIGTERM", () => {
      console.log("Received SIGTERM, starting graceful shutdown");

      fs.writeFileSync("/tmp/shutdown", "1");

      setTimeout(() => {
        process.exit(0);
      }, 20 * 1000); // 20 secs shutdown timeout
    });
  }
}

export const onRequestError = Sentry.captureRequestError;
