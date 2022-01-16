const newsContainer = document.querySelector('.main__newsContainer');
const url = 'load';

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
                                    <div class="main__articleDateAndButtonsContainer">
                                        <span class="main__articleDate">${article.date_of_create}</span>
                                        <div class="main__articleButtonsContainer">
                                            <div class="main__articleButton">
                                                <a href="/article/${article.id}" class="main__articleButtonLink">Číst více</a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>`;

        html += htmlSegment;
    });

    parent.innerHTML = html;
}

renderArticles(url, newsContainer);