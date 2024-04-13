const stations = [
    "Songshan",
    "Nanjing Shanmin",
    "Taipei Arena",
    "Nanjing Fuxing",
    "Songjiang Nanjing",
    "Zhongshan",
    "Beimen",
    "Ximen",
    "Xiaonanmen",
    "Chiang Kai-Shek Memorial Hall",
    "Guting",
    "Taipower Building",
    "Gongguan",
    "Wanlong",
    "Jingmei",
    "Dapinglin",
    "Qizhang",
    "Xiaobitan",
    "Xindian City Hall",
    "Xindian"
];

const messages = {
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Leslie": "I'm at home near Xiaobitan station.",
    "Vivian": "I'm at Xindian station waiting for you."
};

function getStationIndex(stationName) {
    if (stationName === "Xiaobitan") {
        return stations.indexOf("Qizhang");
    } else if (stations.includes(stationName)) {
        return stations.indexOf(stationName);
    } else {
        return -1;
    }
}

function findAndPrint(messages, currentStation) {
    const currentStationIndex = getStationIndex(currentStation);
    if (currentStationIndex === -1) {
        return null;
    }

    let nearestFriends = [];
    let minDistance = Infinity;

    for (const [name, message] of Object.entries(messages)) {
        let stationName = null;
        for (const station of stations) {
            if (message.includes(station)) {
                stationName = station;
                break;
            }
        }

        if (stationName !== null) {
            const friendStationIndex = getStationIndex(stationName);
            if (friendStationIndex !== -1) {
                const distance = Math.abs(currentStationIndex - friendStationIndex);
                if (distance < minDistance) {
                    minDistance = distance;
                    nearestFriends = [name];
                } else if (distance === minDistance) {
                    nearestFriends.push(name);
                }
            }
        }
    }

    // return nearestFriends.join(" ");
    console.log(nearestFriends.join(" "))
}

findAndPrint(messages, "Wanlong"); // print Mary
findAndPrint(messages, "Songshan"); // print Copper
findAndPrint(messages, "Qizhang"); // print Leslie
findAndPrint(messages, "Ximen"); // print Bob
findAndPrint(messages, "Xindian City Hall"); // print Vivian


