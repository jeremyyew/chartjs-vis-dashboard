import * as axios from 'axios';

const BASE_URL = process.env.VUE_APP_API_BASE_URL;
// const BASE_URL = 'http://chairviz.herokuapp.com';

function upload(formData, method) {
  const url = `${BASE_URL}${method}/`;
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
