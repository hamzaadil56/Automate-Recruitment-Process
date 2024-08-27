const Alert = ({
  message,
  onClose,
}: {
  message: string;
  onClose: () => void;
}) => {
  if (!message) return null;

  return (
    <div className="fixed top-4 right-4 bg-green-500 text-white p-4 rounded shadow-lg">
      <div className="flex justify-between items-center">
        <span>{message}</span>
        <button onClick={onClose} className="ml-4 font-bold">
          X
        </button>
      </div>
    </div>
  );
};

export default Alert;
