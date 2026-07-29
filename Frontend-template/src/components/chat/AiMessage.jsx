function AiMessage(props) {
    const content = props.content
    const image_url = props.image_url
    return (
        <div className="flex items-start gap-3 px-4 py-3">
            <div className="w-8 h-8 rounded-full bg-zinc-700 flex items-center justify-center text-sm 
            font-medium text-zinc-100 shrink-0">
                A
            </div>
            <div className="flex-1">
                <p className="text-zinc-100 text-base leading-relaxed">
                    {content}
                </p>
                {image_url && (
                    <img
                        src={`http://localhost:8000${image_url}`}
                        alt="generated diagram"
                        className="mt-4 rounded-lg max-w-full"
                    />
                )}
            </div>
        </div>
    );
}

export default AiMessage;