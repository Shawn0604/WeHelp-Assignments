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
