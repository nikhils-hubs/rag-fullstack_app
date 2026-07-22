import UserMessage from "./UserMessage";
import AiMessage from "./AiMessage";
import TypingIndicator from "./chat-Input/TypingIndicatior";

const dumpyMessage = [
    { id: 1, role: "user", content: "Hey, how are you?" },
    { id: 2, role: "ai", content: "I'm doing great! How can I help you today?" },
    { id: 3, role: "user", content: "Can you explain React hooks?" },
    { id: 4, role: "ai", content: "React is a powerful JavaScript library used for building modern, interactive user interfaces. Instead of directly manipulating the Document Object Model (DOM), React uses a Virtual DOM to efficiently determine what changes need to be applied, resulting in better performance and a smoother user experience. One of React's biggest strengths is its component-based architecture, where the UI is divided into reusable pieces called components. Each component manages its own logic and can receive data through props while maintaining internal data using state. React Hooks such as useState and useEffect simplify state management and side effects, making functional components far more powerful than before. As applications grow, developers often organize components into folders, create custom hooks, and separate business logic from presentation to improve maintainability. React also works seamlessly with modern tools like Vite, Tailwind CSS, React Router, and various backend technologies, making it an excellent choice for full-stack development. Whether you're building a personal portfolio, an AI-powered chatbot, a Retrieval-Augmented Generation application, or a large enterprise dashboard, React provides the flexibility, performance, and ecosystem needed to create scalable, maintainable, and responsive web applications while keeping the codebase organized, reusable, easy to debug, and enjoyable to develop over time.." },
    { id: 5, role: "user", content: "What is useState?" },
    { id: 6, role: "ai", content: "useState is a React hook that allows functional components to manage local state." },
    { id: 7, role: "user", content: "What about useEffect?" },
    { id: 8, role: "ai", content: "useEffect lets you perform side effects like fetching data or updating the DOM." },
    { id: 9, role: "user", content: "How do I center a div?" },
    { id: 10, role: "ai", content: "Using Flexbox with justify-content and align-items is the easiest way ." },

    { id: 11, role: "user", content: "Explain Flexbox." },
    { id: 12, role: "ai", content: "Flexbox is a one-dimensional layout model used for arranging items in rows or columns." },
    { id: 13, role: "user", content: "What is Tailwind CSS?" },
    { id: 14, role: "ai", content: "Tailwind CSS is a utility-first CSS framework that speeds up UI development." },
    { id: 15, role: "user", content: "What is Node.js?" },
    { id: 16, role: "ai", content: "Node.js is a JavaScript runtime built on Chrome's V8 engine." },
    { id: 17, role: "user", content: "What is Express?" },
    { id: 18, role: "ai", content: "Express is a minimal web framework for Node.js." },
    { id: 19, role: "user", content: "What is MongoDB?" },
    { id: 20, role: "ai", content: "MongoDB is a NoSQL database that stores data in JSON-like documents." },

    { id: 21, role: "user", content: "What's PostgreSQL?" },
    { id: 22, role: "ai", content: "PostgreSQL is a powerful open-source relational database." },
    { id: 23, role: "user", content: "Explain JWT." },
    { id: 24, role: "ai", content: "JWT is a compact token format used for authentication." },
    { id: 25, role: "user", content: "What is REST API?" },
    { id: 26, role: "ai", content: "REST APIs use HTTP methods like GET, POST, PUT, and DELETE." },
    { id: 27, role: "user", content: "Difference between PUT and PATCH?" },
    { id: 28, role: "ai", content: "PUT replaces a resource, while PATCH partially updates it." },
    { id: 29, role: "user", content: "Explain async/await." },
    { id: 30, role: "ai", content: "async/await simplifies working with asynchronous JavaScript code." },
];

function ChatList(props) {
    const messages = props.messages
    const isTyping = props.isTyping;
    return (
        <div className="max-w-4xl mx-auto flex flex-col">
            {messages.map((msg) =>
                msg.role === "user" ?
                    (<UserMessage key={msg.id} content={msg.content} />)
                    :
                    (<AiMessage key={msg.id} content={msg.content} />)
            )}
            {isTyping && <TypingIndicator />}
        </div>
    )
}

export default ChatList