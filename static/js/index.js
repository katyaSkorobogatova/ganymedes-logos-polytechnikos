const newsContainer = document.querySelector('.main__newsContainer');
const url = 'article/';

async function getArticles(url) {
    try {
        let res = await fetch(url);
        return await res.json();
    } catch (error) {
        console.log(error);
    }
}

async function renderArticles(url, parent) {
    let articles = await getArticles(url);
    let html = '';
    articles.forEach(article => {
        let htmlSegment = `<div class="main__article">
                                <div class="main__articleUpperPart">
                                    <div class="main__articleTitleWrapper">
                                        <span class="main__articleTitle">${article.title}</span>
                                        <span class="main__articleTitle">Článek # ${article.id}</span>
                                    </div>
                                    <br />
                                    <span class="main__articleAuthor">${article.author}</span>
                                </div>
                                <div class="main__articleLowerPart">
                                    <div class="main__articleText">${article.text}</div>
                                    <div class="main__articleReadmoreAndDate">
                                        <span class="main__articleDate">Doplnit datum publikace</span>
                                        <span class="main__articleReadmore">
                                            <a href="article/${article.id}" target="__blank" class="main__articleSource">
                                                <b>Číst více</b>
                                            </a>
                                        </span>
                                    </div>
                                </div>
                            </div>`;

        html += htmlSegment;
    });

    parent.innerHTML = html;
}

renderArticles(url, newsContainer);