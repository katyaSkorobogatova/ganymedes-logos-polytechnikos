const newsContainer = document.querySelector('.main__newsContainer');
const url = 'load';
const magazinesUrl = '/notpublished/load';

async function getArticles(url) {
    try {
        let res = await fetch(url);
        return await res.json();
    } catch (error) {
        console.log(error);
    }
}

const generateMagazines = magazinesArr => {
    let html = '<option value=""></option>';

    magazinesArr.forEach(magazine => html += `<option class="notBlank" value="${magazine.magazine_number}" data="${magazine.id}">${magazine.magazine_number}</option>`)

    return html;
}

const fetchArticleAndMagazine = (articleId, magazineId) => {
    fetch(`set?magazine=${magazineId}&article=${articleId}`);
}

async function renderArticles(url, parent) {
    let articles = await getArticles(url);
    let magazines = await getArticles(magazinesUrl);
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
                                            </div>
                                            <div class="main__articleButtonsContainer-dropdown">
                                                <form action="">
                                                    <label for="magazine">Zvolte si číslo časopisu:</label>
                                                    <select id="magazine" name="magazine" data="${article.id}" numberMagazine="${article.magazine}">
                                                        ${generateMagazines(magazines)}
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

    const magazinesOptions = document.querySelectorAll('.main__articleButtonsContainer-dropdown form select option.notBlank');

    magazinesOptions.forEach(option => {
        if (option.parentNode.getAttribute('numberMagazine') === option.getAttribute('data')) option.setAttribute('selected', 'selected');
    });

    magazinesOptions.forEach(option => addEventListener('input', () => {
        let articleID = option.parentNode.getAttribute('data');
        let magazineID = option.getAttribute('data');

        fetchArticleAndMagazine(articleID, magazineID);
    }));
}

renderArticles(url, newsContainer);