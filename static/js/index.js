const newsContainer = document.querySelector('.main__newsContainer');

const url = 'ссылОЧКА';

const getArticles = elem => {
    let elemContent = '';

    fetch(url)
        .then(data => data.json())
        .then(data => {
            for (let key in data) {
                elemContent += `<div class="main__article">${data[key]}</div>`;
            }
        })

    elem.innerHTML = elemContent;
}

getArticles(newsContainer);