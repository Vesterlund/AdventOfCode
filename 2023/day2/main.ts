import * as fs from 'fs';

const file = fs.readFileSync("input.txt");


const maxRed = 12;
const maxGreen = 13;
const maxBlue = 14;

const inputArray = file.toString().split("\n");

let idSum = 0;
let powerSum = 0;
//console.log(file.toString().split("\n"));

inputArray.forEach((row) => {
    let splitRow = row.split(":");

    let gameID = parseInt(splitRow[0].replace("Game ", ""))


    let cubeString = splitRow[1].replace("\r","")

    cubeString = cubeString.replace(/ /g, '');
    cubeString = cubeString.replaceAll("red","r");
    cubeString = cubeString.replaceAll("green", "g");
    cubeString = cubeString.replaceAll("blue", "b");


    let cubeSets = cubeString.split(";");

    let foundRed = 0;
    let foundGreen = 0;
    let foundBlue = 0;

    cubeSets.forEach((cubes) => {
        let colorCubes = cubes.split(",");


        colorCubes.forEach((cube) => {
            let col = cube.slice(-1)
            let val = parseInt(cube.slice(0,-1))

            switch (col) {
                case "r":
                    foundRed = Math.max(foundRed, val);
                    break;
                case "b":
                    foundBlue = Math.max(foundBlue, val);
                    break;
                case "g":
                    foundGreen = Math.max(foundGreen, val);
                    break;
            }
        })

    });

    if ((foundRed <= maxRed) && (foundGreen <= maxGreen) && (foundBlue <= maxBlue)) {
        idSum += gameID;
    }

    powerSum += foundRed*foundBlue*foundGreen;

});

console.log("Total id: " + idSum)
console.log("Power sum: " + powerSum)
