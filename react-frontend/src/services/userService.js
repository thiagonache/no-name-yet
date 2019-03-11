import http from "./httpService";

const apiEndpoint = `${process.env.REACT_APP_API_ENDPOINT}/register`;

export function register(user) {
  const response = http.post(apiEndpoint, {
    email: user.username,
    password: user.password,
    name: user.name
  });
  return response;
}
