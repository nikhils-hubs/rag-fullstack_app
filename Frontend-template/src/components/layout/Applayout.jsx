import Navbar from "./Navbar"
import MainLayout from "./MainLayout"
import ChatInput from "../Input/ChatInput"
import { useState } from "react"

function AppLayout() {
    let [messages, setMessages] = useState([])
    let [isTyping, setIsTyping] = useState(false);

    function addMessage(newMsg) {
        setMessages((prev) => [...prev, newMsg])
        setIsTyping(true);
        setTimeout(() => {
            const fakeAiReply = {
                id: Date.now() + 1,
                role: "ai",
                content: "This is a placeholder response while the real API isn't connected yet.",
            };
            setMessages((prev) => [...prev, fakeAiReply])
            setIsTyping(false)
        }, 4000)
    }
    return (
        <div className="h-screen flex flex-col">
            <Navbar />
            <MainLayout messages={messages} isTyping={isTyping} />
            <ChatInput onSend={addMessage} />
        </div>
    )
}

export default AppLayout;