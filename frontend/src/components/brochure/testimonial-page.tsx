import clsx from "clsx";

const getBackgroundColor = (index: number) => {
  return {
    0: "bg-purple",
    1: "bg-yellow",
    2: "bg-grey-100",
    3: "bg-pink",
    4: "bg-orange",
    5: "bg-blue",
    6: "bg-coral",
  }[index % 7];
};

export function TestimonialsPage({
  testimonials,
}: {
  testimonials: Array<{ text: string; author: string }>;
}) {
  return (
    <div className="page bg-cream flex flex-col gap-[1cm] p-[2cm]">
      <h1 className="text-xl font-bold">Testimonials</h1>

      <div className="flex flex-col gap-[2cm]">
        {testimonials.map((t, i) => (
          <blockquote
            key={t.text}
            className={clsx(
              "border-4 border-black p-[0.5cm] w-[80%] text-md",
              {
                "self-start": i % 2 === 0,
                "self-end": i % 2 === 1,
              },
              getBackgroundColor(i),
            )}
          >
            <p>{t.text}</p>
            <footer className="mt-[0.5cm] uppercase font-bold">
              {t.author}
            </footer>
          </blockquote>
        ))}
      </div>
    </div>
  );
}
