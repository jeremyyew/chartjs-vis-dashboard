import * as axios from 'axios';

const BASE_URL = 'http://localhost:8000';
//const BASE_URL = 'http://chairdatavis.herokuapp.com';

function parse(formData) {
  const url = `${BASE_URL}/parse/`;
  // const url = '/upload/'
  return axios({
    method: 'post',
    url,
    data: formData,
    config: { headers: { 'Content-Type': 'multipart/form-data' } },
  }).then((response) => {
    console.log('Response data:', response.data);
    return response.data;
  }).catch((error) => {
    console.log(error);
  });
}

export { parse };
