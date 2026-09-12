import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

const client = axios.create({ baseURL: API });

export const getStats = () => client.get("/rulebook/stats").then((r) => r.data);
export const getRulebook = () => client.get("/rulebook").then((r) => r.data);
export const ask = (question) => client.post("/ask", { question }).then((r) => r.data);
export const getEvalQuestions = () => client.get("/evaluation/questions").then((r) => r.data);
export const runEvaluation = () => client.post("/evaluation/run", {}, { timeout: 180000 }).then((r) => r.data);
export const getLatestEvaluation = () => client.get("/evaluation/latest").then((r) => r.data);
