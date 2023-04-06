export default async function handler(req, res) {
  const { secret, path } = req.body;

  if (secret !== process.env.REVALIDATE_SECRET) {
    return res.status(401).json({ message: "Invalid secret" });
  }

  if (!path) {
    return res.status(400).json({ message: "Invalid path" });
  }

  try {
    await res.revalidate(path);
    return res.json({ revalidated: true });
  } catch (err) {
    console.error(err);
    return res.status(500).send("Error revalidating");
  }
}
