import setting from "./components/setting";
import Swiper from 'swiper';
import 'style-loader!css-loader!swiper/css/swiper.css';

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

document.addEventListener('DOMContentLoaded', async ()=>{
    //create category tab
    let labelList = setting.newsLabel;
    for (let label in labelList) {
        let li = document.createElement('li');
        li.classList.add('news-category__list-item');
        let link = document.createElement('a');
        link.setAttribute('href', './?filter='+ label);
        li.textContent = labelList[label];
        li.append(link);
        document.getElementById("news-category__list").append(li);
    }

    if(document.getElementById('news-img-list')){
        new Swiper('#news-img-list', {
            preloadImages: false,
            lazy: {
                loadPrevNext: true,
            }
        });
        
        let listItem = document.querySelectorAll('news-img-list-item');
        for(let i=0; i < listItem.length; i++){
            listItem[i].style.width = '100%';
        }
    }

    let queries = getQueries(location.search.slice(1));
    if(location.pathname=="/news/"||location.pathname=="/dev/news/"){
        let res = await fetch("../assets/json/news-list.json");
        if(res.ok){
            let data = await res.json();
            let newsList = data["news-list"];
            let pageId = queries["page"]?parseInt(queries["page"]):1;

            if(queries["filter"]){
                let filter = queries["filter"];
                //validation
                if(filter=="management"||filter=="benron"||filter=="debate"||filter=="event"||filter=="others"){
                    newsList = newsList.filter((news)=>{
                        return news["label"] == filter;
                    });
                    document.getElementById('subpage-top').style.display = 'none';
                    document.getElementById('main').classList.add('news-page-no-top');
                    document.getElementById('news-page__title').textContent = 'カテゴリー：' + labelList[filter];
                }
            }else{
                document.getElementById('back-to-top').style.display = 'none';
            }

            //最大ページ数を超えていたらid=1に飛ばす
            let maxPageNum = Math.ceil(newsList.length/entriesPerPage);
            if(pageId>maxPageNum){
                pageId=1;
                window.location.search = "";
            }else if(pageId>1){
                document.getElementById('subpage-top').style.display = 'none';
                document.getElementById('main').classList.add('news-page-no-top');
            }
            
            if(maxPageNum>1){
                //pagination作る
                for(let i=1;i<maxPageNum+1;i++){
                    let paginationDOM = document.createElement('li');
                    paginationDOM.classList.add('news-pagination__list-item');
                    if(i==pageId){
                        paginationDOM.classList.add('is-current');
                        paginationDOM.textContent = String(i);
                    }else{
                        let link = document.createElement('a');
                        link.setAttribute('href', '?page=' + String(i));
                        link.textContent = String(i);
                        paginationDOM.append(link);
                    }
                    document.getElementById('news-pagination__list').append(paginationDOM);
                }
                //scroll調整
                let itemWidth = document.getElementsByClassName("news-pagination__list-item")[0].offsetWidth;
                document.getElementById("news-pagination__list-container").scrollLeft = itemWidth*(pageId-1);

                //pagination next/prev作る
                if(pageId!=1){
                    let newsPagination = document.createElement('div');
                        newsPagination.classList.add('news-pagination__next');
                    let p = document.createElement('p');
                    let link = document.createElement('a');
                    p.textContent = '次へ';
                    newsPagination.append(p);
                    link.setAttribute('href', '?page=' + String(pageId-1))
                    newsPagination.append(link);
                    document.getElementById('news-pagination').append(newsPagination);
                }
                if(pageId!=maxPageNum){
                    let newsPagination = document.createElement('div');
                        newsPagination.classList.add('news-pagination__prev');
                    let p = document.createElement('p');
                    let link = document.createElement('a');
                    p.textContent = '前へ';
                    newsPagination.append(p);
                    link.setAttribute('href', '?page=' + String(pageId+1))
                    newsPagination.append(link);
                    document.getElementById('news-pagination').append(newsPagination);
                }
            }else{
                document.getElementById('news-pagination').style.display = 'none';
            }
            
            let idFrom = entriesPerPage*(pageId - 1);
            let idTo = Math.min(newsList.length - 1, entriesPerPage*pageId - 1);
            for(let i=idFrom; i<idTo+1; i++){
                let news = newsList[i];
                let newsId = setting.createNewsId(news);
                let newsDate = String(news.year) + "/" + ("00"+String(news.month)).slice(-2) + "/" + ("00"+String(news.day)).slice(-2);

                let newsBlock = document.createElement('li');
                    newsBlock.classList.add('news-list-item');
                let label = document.createElement('div');
                    label.classList.add('news-list-item__label', 'label-' + news.label);
                    label.textContent = labelList[news.label];
                newsBlock.append(label);
                let link = document.createElement('a');
                    link.classList.add('news-list-item__link');
                    link.setAttribute('href', newsId);
                let date = document.createElement('div');
                    date.textContent = newsDate;
                let title = document.createElement('div');
                    title.textContent = news.title;
                
                if(news.img){
                    newsBlock.classList.add('with-image');
                    let caption = document.createElement('div');
                        caption.classList.add('news-list-item__caption');
                    date.classList.add('news-list-item__caption__date');
                    caption.append(date);
                    title.classList.add('news-list-item__caption__title');
                    caption.append(title);
                    caption.append(link);
                    newsBlock.append(caption);
                    let imgWrapper = document.createElement('div');
                        imgWrapper.classList.add('news-list-item__img');
                    let img = document.createElement('img');
                        img.setAttribute('src', '../assets/image/news/' + newsId + '/0.jpg');
                        img.setAttribute('alt', news.title);
                    imgWrapper.append(img);
                    newsBlock.append(imgWrapper);
                    let cover = document.createElement('div');
                        cover.classList.add('news-list-item__cover');
                    newsBlock.append(cover);
                }else{
                    newsBlock.append(link);
                    newsBlock.classList.add('no-image');
                    date.classList.add('news-list-item__date');
                    newsBlock.append(date);
                    title.classList.add('news-list-item__title');
                    newsBlock.append(title);
                }
                document.getElementById('news-list').append(newsBlock);
            }
        }else{
            console.log(res.status);
        };
    }else{
        // article page
        let links = document.getElementById('news-content').querySelectorAll('a');
        for(let i=0; i<links.length; i++){
            let link = links[i];
            link.classList.add('text-link');
            if(link.getAttribute('href').indexOf('http') != -1){
                link.setAttribute('target', '_blank');
                link.setAttribute('rel', 'noopener noreferrer');
            }
        }

        let highlightTexts = document.getElementById('news-content').querySelectorAll('[data-highlight]');
        for(let i=0; i<highlightTexts.length; i++){
            let text = highlightTexts[i];
            text.classList.add('highlight');
        }
    }
});
