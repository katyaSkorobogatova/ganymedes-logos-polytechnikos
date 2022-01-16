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
    parent.innerHTML = `<div class="main__article">
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
                            <hr />
                            <div class="main__articleReviewWrapper">
                                <div class="main__articleReviewer">Reviewer is here</div>
                                <div class="main__articleEvaluations">                                
                                    <div class="main__articleEvaluation">Relevantnost: 5</div>
                                    <div class="main__articleEvaluation">Zajímavost: 4</div>
                                    <div class="main__articleEvaluation">Užitnost: 2</div>
                                    <div class="main__articleEvaluation">Originalita: 5</div>
                                    <div class="main__articleEvaluation">Profesionální úroveň: 5</div>
                                    <div class="main__articleEvaluation">Jazyková úroveň: 5</div>
                                    <div class="main__articleEvaluation">Stylistická úroveň: 5</div>
                                </div>
                                <div class="main__articleEvaluation-comment">
                                    <div class="main__articleEvaluation-commentLabel">Komentář: </div>
                                    <div class="main__articleEvaluation-commentText">Komentář recenzenta 123 abc Komentář recenzenta 123 abc Komentář recenzenta 123 abc Komentář recenzenta 123 abc Komentář recenzenta 123 abc Komentář recenzenta 123 abc Komentář recenzenta 123 abc Komentář recenzenta 123 abc Komentář recenzenta 123 abc Komentář recenzenta 123 abc</div>
                                </div>
                            </div>
                        </div>`;
}

renderArticles(url, newsContainer);
