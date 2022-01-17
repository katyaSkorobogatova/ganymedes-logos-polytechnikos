const newsContainer = document.querySelector('.main__newsContainer');
const url = 'load';
const reviewersUrl = 'reviewerload';

async function getArticles(url) {
    try {
        let res = await fetch(url);
        return await res.json();
    } catch (error) {
        console.log(error);
    }
}

const generateReviewers = reviewersArr => {
    let html = '<option value=""></option>';

    reviewersArr.forEach(reviewer => html += `<option class="notBlank" value="${reviewer.name}" data="${reviewer.id}">${reviewer.name}</option>`)

    return html;
}

const fetchArticleAndReviewer = (articleId, reviewerId) => {
    fetch(`setreviewer?reviewer=${reviewerId}&article=${articleId}`);
}

async function renderArticles(url, parent) {
    let articles = await getArticles(url);
    let reviewers = await getArticles(reviewersUrl);
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
                                            <div class="main__articleButtonsContainer-left">
                                                <div class="main__articleButton">
                                                    <a href="/article/${article.id}" class="main__articleButtonLink" target="_blank">Číst více</a>
                                                </div>
                                                <div class="main__articleButton">
                                                    <a href="/article/${article.id}/edit" class="main__articleButtonLink">Upravit</a>
                                                </div>
                                            </div>
                                            <div class="main__articleButtonsContainer-right">
                                                <div class="main__articleButton">
                                                    <a href="/article/${article.id}/delete" class="main__articleButtonLink">Odstranit</a>
                                                </div>
                                                <div class="main__articleButton">
                                                    <a href="/pending/${article.id}/todraft" class="main__articleButtonLink">Poslat zpět autorovi</a>
                                                </div>
                                            </div>
                                            <div class="main__articleButtonsContainer-dropdown">
                                                <form action="">
                                                    <label for="reviewer">Zvolte si oponenta:</label>
                                                    <select id="reviewer" name="reviewer" data="${article.id}" idReviewer="${article.id_reviewer}">
                                                        ${generateReviewers(reviewers)}
                                                    </select>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>`;

        html += htmlSegment;
    });

    parent.innerHTML = html;

    const reviewersOptions = document.querySelectorAll('.main__articleButtonsContainer-dropdown form select option.notBlank');

    reviewersOptions.forEach(option => {
        if (option.parentNode.getAttribute('idReviewer') === option.getAttribute('data')) option.setAttribute('selected', 'selected');
    });

    reviewersOptions.forEach(option => addEventListener('input', () => {
        let articleID = option.parentNode.getAttribute('data');
        let reviewerID = option.getAttribute('data');

        fetchArticleAndReviewer(articleID, reviewerID);
    }));
}

renderArticles(url, newsContainer);
