const newsContainer = document.querySelector('.main__newsContainer');
const articleUrl = 'load';
const reviewUrl = '/review';

async function getArticles(url) {
    try {
        let res = await fetch(url);
        return await res.json();
    } catch (error) {
        console.log(error);
    }
}

async function renderArticles(url, parent) {
    let article = await getArticles(articleUrl);
    let parsedArticleData = JSON.parse(article);
    let parsedReviewData;
    if (parsedArticleData[0].fields.id_review !== null) {
        let review = await getArticles(`${reviewUrl}/${parsedArticleData[0].fields.id_review}`);
        parsedReviewData = JSON.parse(review);
    } else {
        parsedReviewData = null;
    }
    parent.innerHTML = `<div class="main__article">
                            <div class="main__articleUpperPart">
                                <div class="main__articleTitleWrapper">
                                    <span class="main__articleTitle">${parsedArticleData[0].fields.name}</span>
                                    <span class="main__articleTitle">Článek # ${parsedArticleData[0].pk}</span>
                                </div>
                                <br />
                                <span class="main__articleAuthor">${parsedArticleData[0].fields.autor}</span>
                            </div>
                            <div class="main__articleLowerPart">
                                <div class="main__articleText">${parsedArticleData[0].fields.text}</div>
                                <br />
                                <span class="main__articleDate">${parsedArticleData[0].fields.date_of_create}</span>
                            </div>
                            ${parsedReviewData !== null
                                ?   `<hr />
                                    <div class="main__articleReviewWrapper">
                                        <div class="main__articleReviewer">${parsedReviewData[0].fields.reviewer}</div>
                                        <div class="main__articleEvaluations">                                
                                            <div class="main__articleEvaluation">Relevantnost: ${parsedReviewData[0].fields.relevancy}</div>
                                            <div class="main__articleEvaluation">Zajímavost: ${parsedReviewData[0].fields.interesting}</div>
                                            <div class="main__articleEvaluation">Užitnost: ${parsedReviewData[0].fields.usefulness}</div>
                                            <div class="main__articleEvaluation">Originalita: ${parsedReviewData[0].fields.originality}</div>
                                            <div class="main__articleEvaluation">Profesionální úroveň: ${parsedReviewData[0].fields.proffesional_level}</div>
                                            <div class="main__articleEvaluation">Jazyková úroveň: ${parsedReviewData[0].fields.language_level}</div>
                                            <div class="main__articleEvaluation">Stylistická úroveň: ${parsedReviewData[0].fields.stylistic_level}</div>
                                        </div>
                                        <div class="main__articleEvaluation-comment">
                                            <div class="main__articleEvaluation-commentLabel">Komentář: </div>
                                            <div class="main__articleEvaluation-commentText">${parsedReviewData[0].fields.commentary}</div>
                                        </div>
                                    </div>`
                                :   `<div></div>`}
                        </div>`;
}

renderArticles(articleUrl, newsContainer);
