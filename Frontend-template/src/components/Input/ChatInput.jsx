import { useState } from "react"
import SendButton from "./SendButton"
import AttachButton from "./AttachButton"
import ModelSelector from "./ModelSelector"
import useAutoSize from "./AutoResizeTextArea"

function ChatInput(props) {
    const onSend = props.onSend
    let [value, setValue] = useState("")
    const textareaRef = useAutoSize(value);
    const isEmpty = value.trim() === ""

    function handleSend() {
        if (isEmpty) return;

        const newMessage = {
            id: Date.now(),
            role: "user",
            content: value,
        }
        onSend(newMessage)
        setValue("")
    }
    function handleAttach() {
        console.log("attach clicked");

    }
    function handleKeyDown(e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    }

    return (
        <footer className="w-full px-6 py-4 bg-zinc-900">
            <div className="mx-auto w-full max-w-4xl rounded-3xl border border-zinc-700 bg-zinc-800 px-5 py-4">
                <textarea
                    ref={textareaRef}
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                    placeholder="Ask me anything..."
                    className="w-full resize-none bg-transparent text-base text-zinc-100 outline-none
                     max-h-40 outflow-y-auto"
                    onKeyDown={handleKeyDown}
                />
                <div className="flex items-center justify-between mt-3">
                    <div className="flex items-center gap-2">
                        <AttachButton onClick={handleAttach} />
                        <ModelSelector />

                    </div>
                    <SendButton onClick={handleSend} disabled={isEmpty} />

                </div>
            </div>
        </footer>
    )
}
export default ChatInput