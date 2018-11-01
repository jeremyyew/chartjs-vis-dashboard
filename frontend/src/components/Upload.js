import * as axios from 'axios';

const BASE_URL = 'http://localhost:8000';
//const BASE_URL = 'http://chairdatavis.herokuapp.com';

function upload(formData, functionUrl) {
  const url = `${BASE_URL}${functionUrl}`;
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

export { upload };
