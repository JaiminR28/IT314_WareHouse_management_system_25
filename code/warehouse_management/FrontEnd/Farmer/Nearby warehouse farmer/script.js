'use strict';

const clearbtn = document.querySelector('.clear-btn');
const containerEl = document.querySelector('.container');
const addressEL = document.querySelector('.address');
const warehouselocationsEl = document.querySelector('.Warehouse--locations');
const areaLocationText = document.querySelector('.area--location-text');

async function getCurrentAdress() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(async position => {
      const { latitude, longitude } = position.coords;

      const response = await fetch(
        `https://www.mapquestapi.com/geocoding/v1/reverse?key=7NUljeotQj6pdb8DXIKuyN62EXTbmAHi&location=${latitude},${longitude}&includeRoadMetadata=true&includeNearestIntersection=true`
      );
      const jsonData = await response.json();
      const location = jsonData.results[0].locations[0];
      const addressText = `${location.adminArea6}, ${location.adminArea5}, ${location.adminArea3} ${location.adminArea1}`;

      addressEL.innerHTML = addressText;
      areaLocationText.innerHTML = `${location.adminArea6}, ${location.adminArea5}`;
    });
  }
}

getCurrentAdress();

let HomeIcon = L.icon({
  iconUrl: 'Images/homeIcon.png',
  iconSize: [50, 50], // size of the icon
  iconAnchor: [22, 94], // point of the icon which will correspond to marker's location
  shadowAnchor: [4, 62], // the same for the shadow
  popupAnchor: [-3, -76], // point from which the popup should open relative to the iconAnchor
});

let map = L.map('map').setView([23.1870706, 72.6268105], 15);

L.marker([23.1870706, 72.6268105], { icon: HomeIcon }).addTo(map);

L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> <a target="_blank" href="https://icons8.com/icon/65839/home-address">Home Address</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a> contributors',
}).addTo(map);

let locations = [
  {
    id: 1,
    lat: 23.185675,
    long: 72.629526,
    title: '5-Star Thing Storage',
    src: 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80',
    url: 'https://www.google.co.in/ ',

    rating: 3,
  },
  {
    id: 2,
    lat: 23.196996,
    long: 72.631386,
    title: 'hamofy',
    src: 'https://images.unsplash.com/photo-1627309366653-2dedc084cdf1?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1966&q=80',
    url: 'https://www.google.co.in/ ',

    rating: 5,
  },
  {
    id: 3,
    lat: 23.185158,
    long: 72.62724,
    title: 'Anetly',
    src: 'https://images.unsplash.com/photo-1557761469-f29c6e201784?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=849&q=80',
    url: 'https://www.google.co.in/ ',

    rating: 4,
  },
  {
    id: 4,
    lat: 23.184634,
    long: 72.628892,
    title: 'Upright Storage Locker Co',
    src: 'https://images.unsplash.com/photo-1599452390941-251da594d7e3?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80',
    url: 'https://www.google.co.in/ ',
    rating: 3,
  },
];

let popupOption = {
  closeButton: false,
};

locations.forEach(location => {
  new L.marker([location.lat, location.long], {
    icon: new L.DivIcon({
      className: 'my-div-icon',
      html: `<button class="pin--location"><p>${location.title}</p></button>`,
    }),
  })
    .addTo(map)
    .on('click', function () {
      let marker = this;
      // const popupEl = document.querySelectorAll('.popup');

      // popupEl.forEach(Element => {
      //   Element.classList.add('hidden');
      // });

      // if (event.target._popup) {
      //   console.log(event.target._popup);
      //   console.log(
      //     (event.target._popup._contentNode.parentNode.parentNode.style.opacity = 1)
      //   );
      // }

      marker.bindPopup(
        `      <div class="card">
        <div class="card_image">
          <img src=${location.src} alt="mixed vegetable salad in a mason jar." />
        </div>
        <div class="card_content">
          <h2 class="card_title">${location.title}</h2>
          <div class="card_text">
          </div>
        </div>
      </div>
          `,
        {
          maxWidth: 300,
          minWidth: 250,
          maxHeight: 160,
          autoPan: true,
          closeButton: true,
          autoPanPadding: [5, 5],
        }
      );

      marker.openPopup();
    });
});

const addWarehouseLocations = locations => {
  locations.forEach(location => {
    const html = `
    <div class="warehouse-location">
              <img
                class="warehouse--image"
                src= ${location.src}
                alt="warehouse image"
              />
              <div class="details-div">
                <h4 class="warehouse--name">${location.title}</h4>
                <div class="rating--div display-flex">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    fill="red"
                    class="details--svg"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z"
                    />
                  </svg>

                  <p class="details--div--heading">rating:</p>
                  <img
                    class="rating-img"
                    src="./Images/${location.rating}-star.svg"
                    alt="5 star rating"
                  />
                </div>
                <div class="distance-div display-flex">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 256 256"
                    fill="red"
                    class="details--svg"
                  >
                    <path
                      d="M229.33,98.21,53.41,33l-.16-.05A16,16,0,0,0,32.9,53.25a1,1,0,0,0,.05.16L98.21,229.33A15.77,15.77,0,0,0,113.28,240h.3a15.77,15.77,0,0,0,15-11.29l23.56-76.56,76.56-23.56a16,16,0,0,0,.62-30.38ZM224,113.3l-76.56,23.56a16,16,0,0,0-10.58,10.58L113.3,224h0l-.06-.17L48,48l175.82,65.22.16.06Z"
                    ></path>
                  </svg>
                  <p class="details--div--heading">distance:</p>
                  <p class="deatils--info">1.2 km</p>
                </div>
                <div class="capacity-div display-flex">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    class="red-stroke details--svg"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M7.875 14.25l1.214 1.942a2.25 2.25 0 001.908 1.058h2.006c.776 0 1.497-.4 1.908-1.058l1.214-1.942M2.41 9h4.636a2.25 2.25 0 011.872 1.002l.164.246a2.25 2.25 0 001.872 1.002h2.092a2.25 2.25 0 001.872-1.002l.164-.246A2.25 2.25 0 0116.954 9h4.636M2.41 9a2.25 2.25 0 00-.16.832V12a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 12V9.832c0-.287-.055-.57-.16-.832M2.41 9a2.25 2.25 0 01.382-.632l3.285-3.832a2.25 2.25 0 011.708-.786h8.43c.657 0 1.281.287 1.709.786l3.284 3.832c.163.19.291.404.382.632M4.5 20.25h15A2.25 2.25 0 0021.75 18v-2.625c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125V18a2.25 2.25 0 002.25 2.25z"
                    />
                  </svg>

                  <p class="details--div--heading">capacity:</p>
                  <ion-icon name="file-tray-stacked-outline"></ion-icon>
                  <p class="deatils--info">64 sq. ft</p>
                </div>
              </div>
            </div>
            <hr class="line-break" />
  `;

    warehouselocationsEl.innerHTML += html;
  });
};

addWarehouseLocations(locations);

// const options = {
//   method: 'GET',
//   headers: {
//     'X-RapidAPI-Key': '8048530456mshd702a7e93d8d947p133668jsn0dcdbe319bbd',
//     'X-RapidAPI-Host': 'trueway-matrix.p.rapidapi.com',
//   },
// };

// fetch(
//   'https://trueway-matrix.p.rapidapi.com/CalculateDrivingMatrix?origins=23.1870706%2C%2072.6268105&destinations=23.185675%2C72.629526',
//   options
// )
//   .then(response => response.json())
//   .then(response => console.log(response))
//   .catch(err => console.error(err));
