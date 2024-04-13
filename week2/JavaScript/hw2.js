function book(consultants, hour, duration, criteria) {
    // 根據標準對顧問進行排序
    let sortedConsultants;
    if (criteria === "price") {
        sortedConsultants = consultants.slice().sort((a, b) => a.price - b.price);
    } else if (criteria === "rate") {
        sortedConsultants = consultants.slice().sort((a, b) => b.rate - a.rate);
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
