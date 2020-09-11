const MODE = "production";
const enabledSourceMap = MODE === "development";

module.exports = {
    mode: MODE,
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
                test: /\.(sa|sc|c)ss$/,
                exclude: /node_modules/,
                use: [
                    'style-loader',
                    {
                        loader: 'css-loader',
                        options: {
                            url: false,
                            sourceMap: enabledSourceMap
                        }
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: enabledSourceMap
                        }
                    }
                ]
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