module.exports = {
    mode: 'production',
    entry: {
        "top": "./src/js/top.js",
        "common": "./src/js/common.js",
        "news": "./src/js/news.js",
        "form": "./src/js/form.js",
    },
    output: {
        path: `${__dirname}/dist/assets/js`,
        filename: "[name].js",
    },  
    module: {
        rules: [
            {
                test: /\.css$/,
                use: ["style-loader","css-loader"]
            }
        ],
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env'],
                        plugins: ['@babel/plugin-transform-runtime']
                    }
                }
            }
        ]
    }
}