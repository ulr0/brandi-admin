import axios from 'axios'
import store from '@/store/index'

export default {
  store: store,
  computed: {
    constants() {
      return this.$store.state.const
    }
  },
  methods: {
    get(url, config) {
      config = this.cloneAndAuthHeader(config)
      return axios.get(url, config)
    },
    post(url, data, config) {
      config = this.cloneAndAuthHeader(config)
      return axios.post(url, data, config)
    },
    delete(url, config) {
      config = this.cloneAndAuthHeader(config)
      return axios.delete(url, config)
    },
    put(url, data, config) {
      config = this.cloneAndAuthHeader(config)
      return axios.put(url, data, config)
    },
    patch(url, data, config) {
      config = this.cloneAndAuthHeader(config)
      return axios.patch(url, data, config)
    },
    cloneAndAuthHeader(config) {
      if (config === undefined) config = {}
      else config = JSON.parse(JSON.stringify(config))
      if (config.headers === undefined) config.headers = {}
      const token = localStorage.getItem('access_token')
      config.headers.Authorization = token
      config.timeout = 10000
      return config
    },
    download(url, config, filename) {
      config = this.cloneAndAuthHeader(config)
      config.responseType = 'arraybuffer'
      axios.get(url, config).then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]))
        // const fileName = getFileName(response.headers['content-disposition'])
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', filename) // or any other extension
        document.body.appendChild(link)
        link.click()
      })
    }
  }
}

// function getFileName(contentDisposition) {
//   const fileName = contentDisposition
//     .split(';')
//     .filter((ele) => {
//       return ele.indexOf('fileName') > -1
//     })
//     .map((ele) => {
//       return ele
//         .replace(/"/g, '')
//         .split('=')[1]
//     })
//   return fileName[0] ? fileName[0] : null
// }
