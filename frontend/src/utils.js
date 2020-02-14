export default {
  methods: {
    url(path) {
      let base =  process.env.NODE_ENV == "production" ? "" : "https://2f0c8691.ngrok.io"
      return base + path
    }
  }
}