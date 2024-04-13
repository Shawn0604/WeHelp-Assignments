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
func("彭大牆", "陳王明雅", "吳明");  // 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花");  // 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花");  // 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆");  // 夏曼藍波安
