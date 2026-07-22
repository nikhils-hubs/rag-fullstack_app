import { Paperclip } from "lucide-react"

function AttachButton(props) {
    const onClick = props.onClick
    return (
        <button className="p-2 rounded-full hover:bg-zinc-700 transition-colors">
            <Paperclip size={20} className="text-zinc-400" />
        </button>
    );
}

export default AttachButton;