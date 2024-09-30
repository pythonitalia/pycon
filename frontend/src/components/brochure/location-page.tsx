import { compile } from "~/helpers/markdown";

export function LocationPage({
  location,
}: {
  location: {
    city: string;
    cityDescription: string;
    country: string;
    countryDescription: string;
    imageUrl: string;
  };
}) {
  return (
    <div className="page bg-cream flex flex-col gap-[1cm] p-[2cm] relative h-screen">
      <h1 className="text-xl font-bold">
        {location.city}, {location.country}
      </h1>

      <img
        className="w-full border-4 border-black aspect-[9/12] object-cover"
        src={location.imageUrl}
        alt=""
      />

      <p className="bg-yellow border-4 border-black px-[1cm] py-[0.5cm] absolute w-[45%] bottom-[4cm] left-[1cm]">
        {compile(location.cityDescription).tree}
      </p>

      <p className="bg-purple border-4 border-black px-[0.5cm] py-[0.5cm] absolute w-[40%] bottom-[1cm] right-[1cm]">
        {compile(location.countryDescription).tree}
      </p>
    </div>
  );
}
