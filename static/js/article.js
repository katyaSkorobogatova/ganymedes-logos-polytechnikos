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
    let article = await getArticles(url);
    let parsedData = JSON.parse(article);
    console.log(parsedData);
    let htmlSegment = `<div class="main__article">
                            <div class="main__articleUpperPart">
                                <div class="main__articleTitleWrapper">
                                    <span class="main__articleTitle">${parsedData[0].fields.name}</span>
                                    <span class="main__articleTitle">Článek # ${parsedData[0].pk}</span>
                                </div>
                                <br />
                                <span class="main__articleAuthor">${parsedData[0].fields.autor}</span>
                            </div>
                            <div class="main__articleLowerPart">
                                <div class="main__articleText">${parsedData[0].fields.text}</div>
                                <br />
                                <span class="main__articleDate">${parsedData[0].fields.date_of_create}</span>
                            </div>
                        </div>`;

    parent.innerHTML = htmlSegment;
}

renderArticles(url, newsContainer);
