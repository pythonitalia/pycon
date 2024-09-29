import { compile } from "~/helpers/markdown";

export function LocationPage({
  location,
}: {
  location: { city: { text: string }; country: { text: string } };
}) {
  return (
    <div className="page bg-cream flex flex-col gap-[1cm] p-[2cm] relative h-screen">
      {/* TODO: conference location */}
      <h1 className="text-xl font-bold">Bologna, Italy</h1>

      {/* TODO: conference location image */}
      <img
        className="w-full border-4 border-black aspect-[9/12] object-cover"
        src="https://images.unsplash.com/photo-1671794646570-cba0e7dc162b?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        alt=""
      />

      <p className="bg-yellow border-4 border-black px-[1cm] py-[0.5cm] absolute w-[45%] bottom-[4cm] left-[1cm]">
        {compile(location.city.text).tree}
      </p>

      <p className="bg-purple border-4 border-black px-[0.5cm] py-[0.5cm] absolute w-[40%] bottom-[1cm] right-[1cm]">
        {compile(location.country.text).tree}
      </p>
    </div>
  );
}
