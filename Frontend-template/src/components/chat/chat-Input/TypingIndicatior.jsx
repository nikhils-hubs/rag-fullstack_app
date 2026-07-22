function TypingIndicator() {
    return (
        <div className="flex items-start gap-3 px-4 py-3">
            <div className="w-8 h-8 rounded-full bg-zinc-700 flex items-center justify-center text-sm font-medium text-zinc-100 shrink-0">
                A
            </div>
            <div className="flex items-center gap-1 pt-2">
                <span className="w-2 h-2 bg-zinc-500 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                <span className="w-2 h-2 bg-zinc-500 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                <span className="w-2 h-2 bg-zinc-500 rounded-full animate-bounce"></span>
            </div>
        </div>
    );
}

export default TypingIndicator;