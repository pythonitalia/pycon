export function LocationPage() {
  return (
    <div className="page bg-cream flex flex-col gap-[1cm] p-[2cm] relative h-screen">
      <h1 className="text-xl font-bold">Bologna, Italy</h1>

      <img
        className="w-full border-4 border-black aspect-[9/12] object-cover"
        src="https://images.unsplash.com/photo-1671794646570-cba0e7dc162b?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        alt="Bologna, Italy"
      />

      <p className="bg-yellow border-4 border-black px-[1cm] py-[0.5cm] absolute w-[45%] bottom-[4cm] left-[1cm]">
        Bologna is one of the most charming cities of Italy and we love it. Many
        of our attendees enjoy coming here in autumn, for experiencing the rich
        history and culinary culture that will forever be an essential part of
        this place. Included in the UNESCO Creative Cities Network as a City of
        Music, the historic center of Bologna is a treasure trove of art and
        architecture. It has to be told that the PyCon Italia venue is located
        very close to the city center (10 minutes by walk) and many initiatives
        will be announced for sharing this treasure with our attendees.
      </p>

      <p className="bg-purple border-4 border-black px-[0.5cm] py-[0.5cm] absolute w-[40%] bottom-[1cm] right-[1cm]">
        Last but not least, Italy is famous in all the world for its food and
        our attendees never felt disappointed on how we want this tradition to
        be honored. Bologna, known as "La Grassa" (The Fat One), is especially
        renowned for its culinary excellence.
      </p>
    </div>
  );
}
