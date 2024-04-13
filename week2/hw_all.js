console.log("==========task1==========")
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

function findAndPrint(messages,currentStation) {
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
            const friendStationIndex =getStationIndex(stationName);
            if (friendStationIndex !== -1) {
                const distance = Math.abs(currentStationIndex-friendStationIndex);
                if (distance<minDistance) {
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

console.log("==========task2==========")
function book(consultants,hour,duration,criteria) {
    // 根據標準對顧問進行排序
    let sortedConsultants;
    if (criteria === "price") {
        sortedConsultants = consultants.slice().sort((a, b)=> a.price - b.price);
    } else if (criteria === "rate") {
        sortedConsultants = consultants.slice().sort((a, b)=> b.rate - a.rate);
    } else {
        console.log("Invalid criteria");
        return;
    }
    
    // 遍歷排序後的顧問
    for (const consultant of sortedConsultants) {
        // 檢查時間是否可用
        let available = true;
        for (let t = hour; t < hour + duration; t++) {
            if (consultant.schedule && consultant.schedule[t]) {
                available = false;
                break;
            }
        }
        
        // 如果時間可用，設置時間表並返回
        if (available) {
            for (let t = hour; t < hour + duration; t++) {
                if (!consultant.schedule) {
                    consultant.schedule = {};
                }
                consultant.schedule[t] = 1;
            }
            console.log(consultant.name);
            return;
        }
    }
    
    // 所有顧問都不可用
    console.log("No Service");
}

const consultants = [
    { name: "John", rate: 4.5, price: 1000 },
    { name: "Bob", rate: 3, price: 1200 },
    { name: "Jenny", rate: 3.8, price: 800 }
];

// 測試資料
book(consultants, 15, 1, "price");  // Jenny
book(consultants, 11, 2, "price");  // Jenny
book(consultants, 10, 2, "price");  // John
book(consultants, 20, 2, "rate");   // John
book(consultants, 11, 1, "rate");   // Bob
book(consultants, 11, 2, "rate");   // No Service
book(consultants, 14, 3, "price");  // John


console.log("==========task3==========")
function func(...names) {
    if (names.length === 0) {
        console.log("沒有資料");
        return;
    }

    const middleNameCount = {};  // 用於統計中間名出現次數

    // 收集並統計每個名字的中間名
    for (const name of names) {
        const middleIndex = Math.floor(name.length / 2);
        const middleName = name[middleIndex];
        middleNameCount[middleName] = (middleNameCount[middleName] || 0) + 1;
    }

    // 找出只出現一次的中間名
    const uniqueMiddleNames = Object.keys(middleNameCount).filter(name => middleNameCount[name] === 1);

    // 找到對應的名字並印出
    for (const name of names) {
        const middleIndex = Math.floor(name.length / 2);
        if (uniqueMiddleNames.includes(name[middleIndex])) {
            console.log(name);
            return;
        }
    }

    console.log("沒有");
}

// 測試資料
func("彭大牆", "陳王明雅", "吳明"); // print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花"); // print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); // print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆"); // print 夏曼藍波安


console.log("==========task4==========")

function getNumber(index) {
    let number = 0;
    if (index % 3 === 0) {
        number = 7 * Math.floor(index / 3);
    } else if (index % 3 === 1) {
        number = 7 * Math.floor((index + 2) / 3) - 3;
    } else if (index % 3 === 2) {
        number = 7 * Math.floor((index + 1) / 3) + 1;
    }
    console.log(number);
}

getNumber(1);   // print 4
getNumber(5);   // print 15
getNumber(10);  // print 25
getNumber(30);  // print 70



