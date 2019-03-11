import http from "./httpService";
const apiEndpoint = process.env.REACT_APP_API_ENDPOINT;
const pollId = process.env.REACT_APP_POLL_ID;

export function getAnswers() {
  const endpoint = `${apiEndpoint}/answers?pollId=${pollId}`;
  const response = http.get(endpoint, { crossdomain: true });
  return response;
}

export function saveAnswer(description) {
  const data = { pollId: Number(pollId), description: description, votes: 0 };
  const endpoint = `${apiEndpoint}/answers`;
  const response = http.post(endpoint, data, { crossdomain: true });
  return response;
}

export function getPolls() {
  const endpoint = `${apiEndpoint}/polls?pollId=${pollId}`;
  const response = http.get(endpoint, { crossdomain: true });
  return response;
}

export function incrementVotes(answer) {
  localStorage.setItem("pollAnswer", answer);
  const endpoint = `${apiEndpoint}/answers?description=${answer}`;
  const response = http.put(endpoint, { crossdomain: true });
  return response;
}
