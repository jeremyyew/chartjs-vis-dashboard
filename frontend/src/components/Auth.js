import axios from 'axios';
import Const from './Const';
// const BASE_URL = 'http://localhost:8000';
const { BASE_URL } = Const;

function authenticate(data) {
  const url = `${BASE_URL}/login`;
  // const url = '/upload/'
  return axios({
    method: 'post',
    url,
    data,
    config: { headers: { 'Content-Type': 'multipart/form-data' } },
  }).then((response) => {
    console.log('AUTH RESPONSE:', response.data);
    return response.data;
  }).catch((error) => {
    console.log(error);
  });
}

export default { authenticate };
