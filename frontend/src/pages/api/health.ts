import fs from "fs";

export default async function handler(req, res) {
  if (fs.existsSync("/tmp/shutdown")) {
    return res.status(503).json({
      status: "shutdown",
      version: process.env.GIT_HASH,
    });
  }

  return res.json({
    status: "ok",
    version: process.env.GIT_HASH,
  });
}
