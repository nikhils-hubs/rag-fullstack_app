import { useEffect, useRef } from "react";

function useAutoSize(value) {
    const textareaRef = useRef(null);

    useEffect(() => {
        const textarea = textareaRef.current;
        if (textarea) {
            textarea.style.height = "auto";
            textarea.style.height = textarea.scrollHeight + "px";
        }
    }, [value]);

    return textareaRef;
}

export default useAutoSize;