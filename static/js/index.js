const newsContainer = document.querySelector('.main__newsContainer');
const url = 'article/';

function createNode(element) {
    return document.createElement(element);
}

function append(parent, el) {
    return parent.appendChild(el);
}

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
                                    <span class="main__articleTitle">${article.title}</span>
                                    <br />
                                    <span class="main__articleAuthor">${article.author}</span>
                                </div>
                                <div class="main__articleLowerPart">
                                    <div class="main__articleText">${article.text}</div>
                                    <span class="main__articleReadmore">
                                        <a href=${article.url} target="__blank" class="main__articleSource">
                                            <b>Číst více</b>
                                        </a>
                                    </span>
                                </div>
                            </div>`;

        html += htmlSegment;
    });

    parent.innerHTML = html;
}

renderArticles(url, newsContainer);