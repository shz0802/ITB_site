module.exports = {
    mode: 'production',
    entry: {
        top: './src/js/top.js',
        common: './src/js/common.js',
        news: './src/js/news.js',
        form: './src/js/form.js'
    },
    output: {
        filename: "[name].js"
    }
}