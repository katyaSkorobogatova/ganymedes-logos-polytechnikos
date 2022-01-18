const newsContainer = document.querySelector('.main__newsContainer');
const url = '/notpublished/load';

async function getArticles(url) {
    try {
        let res = await fetch(url);
        return await res.json();
    } catch (error) {
        console.log(error);
    }
}

async function renderArticles(url, parent) {
    let magazines = await getArticles(url);
    let html = '';
    magazines.forEach(magazine => {
        let htmlSegment = `<div class="main__article">
                                <div class="main__articleUpperPart">
                                    <div class="main__articleTitleWrapper">
                                        <span class="main__articleTitle">Časopis # ${magazine.magazine_number}</span>
                                    </div>
                                </div>
                                <div class="main__articleLowerPart">
                                    <div class="main__articleButton">
                                        <a href="/notpublished/${magazine.id}/publish" class="main__articleSource">Publikovat časopis</a>
                                    </div>
                                </div>
                            </div>`;

        html += htmlSegment;
    });

    parent.innerHTML = html;
}

renderArticles(url, newsContainer);