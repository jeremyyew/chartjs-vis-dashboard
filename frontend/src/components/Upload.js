import * as axios from 'axios';

// const BASE_URL = 'http://localhost:8000';
const BASE_URL = 'http://chairviz.herokuapp.com';

function upload(formData) {
  const url = `${BASE_URL}/upload/`;
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

export { upload };
