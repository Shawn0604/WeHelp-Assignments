const burgerMenu = document.querySelector('.burger-menu');
const popupMenu = document.querySelector('.popup-menu');

burgerMenu.addEventListener('click', function() {
  burgerMenu.classList.toggle('active');
  popupMenu.classList.toggle('active');
});

const closeIcon = document.querySelector('.close-icon');

closeIcon.addEventListener('click', function() {
  burgerMenu.classList.remove('active');
  popupMenu.classList.remove('active');
});


// fetch data----------------------------------
function findFirstImage(filelist) {
  const pattern = /https?:\/\/[^"]+?\.jpe?g/i;
  const match = filelist.match(pattern);
  if (match) {
    return match[0];
  } else {
    return null;
  }
}

async function fetchData() {
  const content = document.querySelector('.content');
  const promotions = content.querySelector('.promotions');
  const boxes = content.querySelector('.boxes');

  const response = await fetch('https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1');
  const data = await response.json();
  spotArray = (data["data"]["results"]);

  for (let i = 0; i < 13; i++) {
    if (i < 3) {
      const div = document.createElement('div');
      div.classList.add('promotion');

      const img = document.createElement('img');
      img.src = findFirstImage(spotArray[i]["filelist"]);
      img.alt = spotArray[i]["stitle"];
      div.appendChild(img);

      const p = document.createElement('p');
      p.textContent = spotArray[i]["stitle"].length > 7 ? spotArray[i]["stitle"].slice(0, 7) + "..." : spotArray[i]["stitle"];
      div.appendChild(p);

      promotions.appendChild(div);
    } else {
      const div = document.createElement('div');
      div.classList.add('box');

      const img = document.createElement('img');
      img.src = findFirstImage(spotArray[i]["filelist"]);
      img.alt = spotArray[i]["stitle"];
      div.appendChild(img);

      const boxText = document.createElement('div');
      boxText.classList.add('box-text');
      const p = document.createElement('p');
      p.textContent = spotArray[i]["stitle"].length > 7 ? spotArray[i]["stitle"].slice(0, 7) + "..." : spotArray[i]["stitle"];
      boxText.appendChild(p);
      div.appendChild(boxText);

      const star = document.createElement('span');
      star.classList.add('fa', 'fa-star');
      div.appendChild(star);

      boxes.appendChild(div);
    }
  }
}

fetchData()