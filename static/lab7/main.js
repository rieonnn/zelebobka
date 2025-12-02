function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function(data) {
        return data.json();
    })
    .then(function(films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitle = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            // Форматируем название: русское название основное, оригинальное в скобках курсивом
            let titleHTML = films[i].title_ru;

            // Если оригинальное название отличается от русского, добавляем его
            if (films[i].title && films[i].title !== films[i].title_ru) {
                titleHTML += ' <span style="font-style: italic; color: #666;">(' + films[i].title + ')</span>';
            }

            tdTitle.innerHTML = titleHTML;
            tdYear.innerText = films[i].year;

            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            editButton.onclick = function() {
                editFilm(films[i].id);
            };

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.onclick = function() {
                deleteFilm(films[i].id, films[i].title_ru);
            };

            tdActions.append(editButton);
            tdActions.append(delButton);

            tr.append(tdTitle);
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    });
}

function showModal() {
    // Очищаем сообщение об ошибке при открытии модального окна
    document.getElementById('description-error').innerText = '';
    document.querySelector('div.modal').style.display = 'block';
    document.querySelector('.modal-overlay').style.display = 'block';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
    document.querySelector('.modal-overlay').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title_ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';

    // Очищаем сообщение об ошибке
    document.getElementById('description-error').innerText = '';

    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title_ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    }

    const url = `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    // Очищаем все предыдущие ошибки
    document.getElementById('description-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('title_ru-error').innerText = '';
    document.getElementById('year-error').innerText = '';

    fetch(url, {
        method: method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        return resp.json();
    })
    .then(function(errors) {
        if(errors) {
            if(errors.title_ru)
                document.getElementById('title_ru-error').innerText = errors.title_ru;
            if(errors.title)
                document.getElementById('title-error').innerText = errors.title;
            if(errors.year)
                document.getElementById('year-error').innerText = errors.year;
            if(errors.description)
                document.getElementById('description-error').innerText = errors.description;
        }
    });
}


function editFilm(id) {
    // Очищаем сообщение об ошибке перед открытием
    document.getElementById('description-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('title_ru-error').innerText = '';
    document.getElementById('year-error').innerText = '';

    fetch(`/lab7/rest-api/films/${id}`)
    .then(function(data) {
        return data.json();
    })
    .then(function(film) {
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title;
        document.getElementById('title_ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        showModal();
    });
}

function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}` , {method: 'DELETE'})
        .then(function () {
            fillFilmList();
        });
}
