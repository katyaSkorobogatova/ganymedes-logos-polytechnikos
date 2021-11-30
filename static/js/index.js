const newsContainer = document.querySelector('.main__newsContainer');
const url = 'article/';

function createNode(element) {
    return document.createElement(element);
}

function append(parent, el) {
    return parent.appendChild(el);
}

const getArticles = (parent, child, className) => {
    fetch(url)
        .then(data => data.json())
        .then(data => {
            let news = data;
            for (k in news) {
                let childNode = createNode(child);
                childNode.classList.add(className);
                childNode.textContent = news[k];
                append(parent, childNode);
            }
        })
}

getArticles(newsContainer, 'div', 'main__article');