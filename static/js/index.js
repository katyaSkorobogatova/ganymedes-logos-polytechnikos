const newsContainer = document.querySelector('.main__newsContainer');
const url = 'magazine/';

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
        let htmlSegment = `<div class="main__magazine">
                                <div class="main__magazineLeftPart">
                                    <div class="main__magazineTitle">Číslo časopisu: ${magazine.id}</div>
                                    <div class="main__magazineDate">${magazine.release_date}</div>
                                </div>
                                <div class="main__magazineRightPart">
                                    <div class="main__magazineReadmore">
                                        <a href="magazine/${magazine.id}" class="main__magazineSource">
                                            <b>Zhlédnout časopis</b>
                                        </a>
                                    </div>
                                </div>
                            </div>`;

        html += htmlSegment;
    });

    parent.innerHTML = html;
}

renderArticles(url, newsContainer);