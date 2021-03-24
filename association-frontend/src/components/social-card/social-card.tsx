type EventCardProps = {
  component: React.ReactElement;
};
const SocialCard = ({ component }: EventCardProps) => {
  return <div className="p-4 soverflow-hidden">{component}</div>;
};
export default SocialCard;
