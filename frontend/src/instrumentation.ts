export async function register() {
  if (
    process.env.NEXT_RUNTIME === "nodejs" &&
    process.env.NEXT_MANUAL_SIG_HANDLE
  ) {
    const fs = await import("fs");

    process.on("SIGTERM", () => {
      fs.writeFileSync("/tmp/shutdown", "1");
    });
  }
}
