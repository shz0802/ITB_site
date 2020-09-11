import setting from "./components/setting";
import $ from "jquery";
import 'slick-carousel';

const entriesPerPage = 9;

const getQueries = (str)=>{
    let queries = {};
    if(!str){return queries;}
    str.split('&').forEach(function(str){
        var queryArr = str.split('=');
        queries[queryArr[0]] = queryArr[1];
    });
    return queries;
}

$(()=>{
    //create category tab
    let labelList = setting.newsLabel;
    for (let label in labelList) {
        let labelDOM = "<li class='news-category__list-item'><a href='./?filter="+ label + "'>" + labelList[label] + "</a></li>";
        $(".news-category__list").append(labelDOM);
    }

    let queries = getQueries(location.search.slice(1));
    if(location.pathname=="/news/"||location.pathname=="/dev/news/"){
        $.ajax({
            url: "../assets/json/news-list.json",
            type:"GET",
            dataType:"json",
            }).done(function(data){
                let newsList = data["news-list"];
                let pageId = queries["page"]?parseInt(queries["page"]):1;

                if(queries["filter"]){
                    let filter = queries["filter"];
                    //validation
                    if(filter=="management"||filter=="benron"||filter=="debate"||filter=="event"||filter=="others"){
                        newsList = newsList.filter((news)=>{
                            return news["label"] == filter;
                        });
                        $(".subpage-top").hide();
                        $("#main").addClass("news-page-no-top");
                        $("#news-page__title").html("カテゴリー：" + labelList[filter]);
                    }
                }else{
                    $(".news-back-ontop").hide();
                }

                //最大ページ数を超えていたらid=1に飛ばす
                let maxPageNum = Math.ceil(newsList.length/entriesPerPage);
                if(pageId>maxPageNum){
                    pageId=1;
                    window.location.search = "";
                }else if(pageId>1){
                    $(".subpage-top").hide();
                    $("#main").addClass("news-page-no-top");
                }
                
                if(maxPageNum>1){
                    //pagination作る
                    for(let i=1;i<maxPageNum+1;i++){
                        let paginationDOM = "";
                        if(i==pageId){
                            paginationDOM = "<li class='news-pagination__list-item is-current'>"+ String(i) +"</li>";
                        }else{
                            paginationDOM = "<li class='news-pagination__list-item'><a href='?page="+ String(i) +"'>"+ String(i) +"</a></li>";
                        }
                        $(".news-pagination__list").append(paginationDOM);
                    }
                    //scroll調整
                    $(".news-pagination__list").scrollLeft($(".news-pagination__list-item").width()*(pageId-1));

                    //pagination next/prev作る
                    if(pageId!=1){
                        $(".news-pagination").append("<div class='news-pagination__next'><p>次へ</p><a href='?page="+ String(pageId-1) +"'></a></div>");
                    }
                    if(pageId!=maxPageNum){
                        $(".news-pagination").append("<div class='news-pagination__prev'><p>前へ</p><a href='?page="+ String(pageId+1) +"'></a></div>");
                    }
                }else{
                    $(".news-pagination").hide();
                }
                
                let idFrom = entriesPerPage*(pageId-1);
                let idTo = Math.min(newsList.length-1,entriesPerPage*pageId - 1);
                for(let i=idFrom;i<idTo+1;i++){
                    let news = newsList[i],
                        newsDOM = "",
                        newsId = setting.createNewsId(news),
                        newsDate = String(news.year) + "/" + ("00"+String(news.month)).slice(-2) + "/" + ("00"+String(news.day)).slice(-2);
                    if(news.img){
                        newsDOM = "<li class='main-news__list-item with-image'>"
                                    + "<div class='main-news__list-item__label " + "label-" + news.label +"'>" + labelList[news.label] + "</div>"
                                    + "<div class='main-news__list-item__caption'>"
                                        + "<div class='main-news__list-item__caption__date'>" + newsDate + "</div>"
                                        + "<div class='main-news__list-item__caption__title'>" + news.title + "</div>"
                                    + "</div>"
                                    + "<div class='main-news__list-item__img'>" 
                                        + "<img class='lozad' src='../assets/image/news/" + newsId + "/0.jpg' alt='" + news.title + "'></div>"
                                    + "</div>"
                                    + "<a class='main-news__list-item__link' href='" + newsId + "'></a>"
                                    + "<div class='main-news__list-item__cover'></div>"
                                    + "</li>"
                    }else{
                        newsDOM = "<li class='main-news__list-item no-image'>"
                                    + "<div class='main-news__list-item__label " + "label-" + news.label +"'>" + labelList[news.label] + "</div>"
                                    + "<div class='main-news__list-item__date'>" + newsDate + "</div>"
                                    + "<div class='main-news__list-item__title'>" + news.title + "</div>"
                                    + "<a class='main-news__list-item__link' href='" + newsId + "'></a>"
                                    + "</li>"
                    }
                    $(".main-news__list").append(newsDOM);
                }
            }).fail(function(jqXHR, textStatus, errorThrown ) {
                console.log(jqXHR.status,textStatus,errorThrown);
        });
    }else{
        let slide = $('.main-news__img-list').slick({
            arrows: false,
            centerMode: true,
            infinite: false, 
            responsive:[
                {
                    breakpoint: 600,
                    settings: {
                        centerPadding: "10%",
                    }
                },
                {
                    breakpoint: 9999,
                    settings: {
                        centerPadding: "20%",
                    }
                }
            ]
        });
        let timeoutId;
        window.addEventListener("resize",()=>{
            clearTimeout(timeoutId);
            timeoutId = setTimeout(()=>{
                slide.slick("reinit");
            },500);
        });
    }
});
