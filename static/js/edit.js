const form = document.querySelector('.main__form');
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
    let articleToEdit = await getArticles(url);
    let parsedData = JSON.parse(articleToEdit);
    console.log(parsedData);
    parent.innerHTML += `<div class="main__formTitle">
                            <label for="name">Název článku: </label>
                            <input name="name" id="name" value="${parsedData[0].fields.name}">
                        </div>
                        <div class="main__formText">
                            <label for="text">Text článku: </label>
                            <textarea name="text" id="text">${parsedData[0].fields.text}</textarea>
                        </div>
                        <div class="main__formButtonContainer">
                            <button class="main__formButton">Uložit změny</button>
                        </div>`;
}

renderArticles(url, form);
