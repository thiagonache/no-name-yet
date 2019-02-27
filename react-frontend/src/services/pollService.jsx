import http from "./httpService";
const apiEndpoint = process.env.REACT_APP_API_ENDPOINT;

export function getVotes(vote) {
  const endpoint = `${apiEndpoint}/poll?vote=${vote}`;
  const response = http.get(endpoint, { crossdomain: true });
  return response;
}

export function incrementVotes(vote) {
  const data = { vote: vote };
  const endpoint = `${apiEndpoint}/poll`;
  const response = http.post(endpoint, data);
  return response;
}
