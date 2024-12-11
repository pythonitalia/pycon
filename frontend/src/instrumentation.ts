import fs from "fs";

export function register() {
  if (process.env.NEXT_RUNTIME === "nodejs") {
    if (process.env.NEXT_MANUAL_SIG_HANDLE) {
      process.on("SIGTERM", () => {
        fs.writeFileSync("/tmp/shutdown", "1");
      });
    }
  }
}
