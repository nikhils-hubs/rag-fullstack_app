import axios from "axios"

const API = axios.create({
    baseURL: "http://localhost:8000",
});

const sendChatMessage = async (message) => {
    const { data } = await API.post("/chat", {
        message,
    })
    return data
}

export default sendChatMessage