import EmptyState from "../chat/chat-Input/EmptyState";
import ChatList from "../chat/ChatList";
function MainLayout(props) {
    const messages = props.messages
    const isTyping = props.isTyping

    const hasMessage = messages.length > 0

    return (
        <>
            <main className="flex-1 overflow-y-auto min-h-0 px-6 py-10 bg-zinc-900">
                {hasMessage ? (<ChatList messages={messages} isTyping={isTyping} />) : (<EmptyState />)}
            </main>
        </>
    );
}
export default MainLayout;