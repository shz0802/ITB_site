const gulp = require("gulp");
const ejs = require("gulp-ejs");
const sass = require("gulp-sass");
const autoprefixer = require("gulp-autoprefixer");
const cleanCSS = require("gulp-clean-css");
const browserSync = require("browser-sync");
const plumber = require("gulp-plumber");
const rename = require("gulp-rename");
const fs =require('fs');
const webpackStream = require("webpack-stream");
const webpack = require("webpack");
const webpackConfig = require("./webpack.config.js");

const fileDir = {
    srcEjs: ["src/ejs/**/*.ejs","!src/ejs/**/_*.ejs"],
    srcScss: "src/scss/**/*.scss",
    distCss: "dist/assets/css/",
    srcJs: "src/js/**/*.js",
    distJs: "dist/assets/js/",
    newsJson: "dist/assets/json/news-list.json",
    newsTemplate: "src/ejs/news/_news-template.ejs"
}

const compileEjs = ()=>{
    return gulp.src(fileDir.srcEjs)
        .pipe(plumber())
        .pipe(ejs())
        .pipe(rename({extname:".html"}))
        .pipe(gulp.dest("dist/"));
}

const compileSass = ()=>{
    return gulp.src(fileDir.srcScss)
        .pipe(plumber({
            errorHandler: function(err) {
              console.log(err.CssSyntaxError);
              this.emit('end');
            }
        }))
        .pipe(sass())
        .pipe(autoprefixer())
        .pipe(cleanCSS())
        .pipe(gulp.dest(fileDir.distCss))
        .pipe(browserSync.reload({stream: true}));
};

const compileJs = ()=>{
    return gulp.src(fileDir.srcJs)
        .pipe(plumber())
        .pipe(webpackStream(webpackConfig,webpack))
        .pipe(gulp.dest(fileDir.distJs));
}

const createNewsEjs = (done)=>{
    newsList = JSON.parse(fs.readFileSync(fileDir.newsJson, 'utf8'))["news-list"];
    for(i=0;i<newsList.length;i++){
        let news = newsList[i];
        news.id = String(news.year) + "-" + String(news.month) + "-" + String(news.day) + "_" + news.name;
        if(news.img){
            let path = "dist/assets/image/news/" + news.id;
            fs.mkdir(path,(err)=>{});
        }
        
        let nextNews = i==0?null:newsList[i-1];
        let prevNews = i==(newsList.length-1)?null:newsList[i+1];
        if(!news.customizedHtml){
            gulp.src(fileDir.newsTemplate)
                .pipe(plumber())
                .pipe(ejs({news: news,next: nextNews,prev: prevNews}))
                .pipe(rename(news.id + ".html"))
                .pipe(gulp.dest("dist/news/"));
        }
    }
    done();
}

const initBrowserSync = (done)=>{
    browserSync({
        server:{
            baseDir: "dist/",
            index: "index.html",
            notify: false,
        },
    });
    done();
};

const reloadBrowser = (done)=>{
    browserSync.reload();
    done();
}

const watchFiles = (done)=>{
    gulp.watch("src/ejs/**/*.ejs", gulp.series(compileEjs,reloadBrowser));
    gulp.watch(fileDir.srcJs, gulp.series(compileJs,reloadBrowser));
    gulp.watch(fileDir.srcScss, compileSass);
    gulp.watch([fileDir.newsJson,fileDir.newsTemplate], gulp.series(createNewsEjs,reloadBrowser));
    done();
}

exports.default = gulp.parallel(watchFiles,initBrowserSync);
exports.create = createNewsEjs;