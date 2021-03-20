type EventCardProps = {
  title: string;
  description?: string;
  isOnline?: boolean;
};
const EventCard: React.FC<EventCardProps> = ({
  title,
  description,
  isOnline,
}) => {
  return (
    <div className="relative">
      <div className="h-full rounded-md shadow-lg ring-1 ring-black ring-opacity-5 overflow-hidden">
        <div className="mb-4 pb-32 bg-cover bg-center bg-gradient-to-br from-yellow-400 to-pink-500 bg-local bg-no-repeat "></div>
        <div>
          <div className="text-lg px-4 leading-6 font-medium text-gray-900">
            {title}
          </div>

          <div className="h-100 mt-2 px-4 pb-4 text-base text-gray-500">
            {description}
          </div>
        </div>
      </div>
    </div>
  );
};
export default EventCard;
