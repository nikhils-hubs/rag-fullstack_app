import { useState } from "react";
import Models from "../../data/model";

function ModelSelector() {
    let [selectModel, setSelectModel] = useState(Models[0])
    return (
        <select value={selectModel}
            onChange={(e) => setSelectModel(e.target.value)}
            className=" flex-1 bg-zinc-800 text-zinc-300 text-sm rounded-lg pl-3 py-2 
            outline-none cursor-pointer hover:bg-zinc-700 transition-colors"
        >
            {Models.map((model) => (
                <option key={model} value={model}>
                    {model}
                </option>
            ))}

        </select>
    );
}

export default ModelSelector;