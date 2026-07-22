import Navbar from "./Navbar"
import MainLayout from "./MainLayout"
import ChatInput from "../Input/ChatInput"
import { useState } from "react"
import sendChatMessage from "../../services/api"

function AppLayout() {
    let [messages, setMessages] = useState([])
    let [isTyping, setIsTyping] = useState(false);

    async function addMessage(newMsg) {
        setMessages((prev) => [...prev, newMsg])
        setIsTyping(true);
        try {
            const response = await sendChatMessage(newMsg.content)
            const aireply = {
                id: Date.now(),
                role: "system",
                content: response.message_to_send
            }
            setMessages((prev) => [...prev, aireply])
        }
        catch (err) {
            console.error(err)
            setMessages((prev) => [...prev,
            {
                id: Date.now(),
                role: "system",
                content: "Something went Wrong"
            }
            ])
        }
        finally {
            setIsTyping(false)
        }
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