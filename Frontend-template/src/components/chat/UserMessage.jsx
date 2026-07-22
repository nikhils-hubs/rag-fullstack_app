function UserMessage(props) {
    const content = props.content
    return (
        <div className="flex justify-end px-4 py-3">
            <div className="bg-indigo-600 text-white rounded-2xl px-4 py-2 max-w-[75%]">
                <p className="text-base leading-relaxed">
                    {content}
                </p>
            </div>
        </div>
    );
}

export default UserMessage;