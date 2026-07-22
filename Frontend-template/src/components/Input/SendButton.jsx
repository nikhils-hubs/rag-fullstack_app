import { ArrowUp } from "lucide-react";

function SendButton(props) {
    const onClick = props.onClick
    const disabled = props.disabled
    return (
        <button
            onClick={onClick}
            disabled={disabled}
            className={`p-2 rounded-full transition-colors 
                ${disabled
                    ? "bg-zinc-700 text-zinc-500 cursor-not-allowed"
                    : "bg-indigo-600 text-white hover:bg-indigo-500 cursor-pointer"
                }`}
        >
            <ArrowUp size={20} className="text-zinc-400" />
        </button>
    );
}

export default SendButton;