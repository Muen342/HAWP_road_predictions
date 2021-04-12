const fs = require('fs');
const MAXDEV = 20

const PATH = './data/wireframe/images'
var files = fs.readdirSync(PATH);

const calcDist = (X,Y)=>{
    return Math.sqrt((parseFloat(X[0])-parseFloat(Y[0]))*(parseFloat(X[0])-parseFloat(Y[0]))+ (parseFloat(X[1])-parseFloat(Y[1]))*(parseFloat(X[1])-parseFloat(Y[1])))
}

const genLine = (X,Y)=>{
    const m = (parseFloat(Y[1])-parseFloat(X[1]))/(parseFloat(Y[0])-parseFloat(X[0]))
    let b;
    if(Math.abs(m) == Infinity){
        // if vertical use b as x intercept
         b = X[0];
    }
    else{
         b = parseFloat(X[1])-(m*parseFloat(X[0]))
    }
    return [m,b]
}

const findIntersect = (line, Y)=>{
    if(Math.abs(line[0]) == Infinity){
        return [line[1], Y[1]];
    }
    else if(line[0] == 0){
        return [Y[0], line[1]]
    }
    else{
        const m = -1/line[0]
        const b2 = parseFloat(Y[1])-(m*parseFloat(Y[0]))
        const x = (b2-line[1])/(line[0]-m)
        const y = m*x+b2
        return [x,y]
    }
}

files = files.filter(a=>a.includes('.lines'))
let total = files.length
let slicepoint2 = Math.round(0.8*total);
let testFiles2 = files.slice(slicepoint2);


let toFile = [];
for(const file of testFiles2){
    const data = fs.readFileSync(PATH + '/' + file, 'utf8');

    let c = data.split('\n');
    c.pop();
    let d = []
    for(const i of c){
        let temp = i.split(' ');
        temp.pop();
        d.push(temp);
    }
    let junctions = [];
    let lines = []
    let isValid = true;
    for(const i of d){
        let point = [parseFloat(i[0]), parseFloat(i[1])];
        let point2 = [parseFloat(i[i.length - 2]), parseFloat(i[i.length - 1])];
        let line = genLine(point, point2);
        let midpoint
        if(i.length%4 == 2){
            midpoint = [parseFloat(i[Math.floor(i.length/2)-1]), parseFloat(i[Math.floor(i.length/2)])];
        }
        else{
            midpoint = [parseFloat(i[Math.floor(i.length/2)]), parseFloat(i[Math.floor(i.length/2)+1])];
        }
        if(calcDist(findIntersect(line, midpoint),midpoint) > 50){
            isValid = false;
            break;
        }
        if(point[0] < 0 || point[1] < 0){
            if(line[1]<0){
                point = [(-1)*(line[1])/line[0], 0]
            }
            else{
                point = [0,line[1]];
            }
        }
        junctions.push(point);
        junctions.push(point2);
        lines.push([point[0],point[1],point2[0],point2[1]]);
    }
    if(junctions.length < 3 || isValid == false){
        continue;
    }
    
    const filename = file.replace('lines.txt', 'jpg');

    let final = {}
    final['height'] = 590;
    final['width'] = 1640
    final['lines'] = lines;
    final['filename'] = filename;
    final['junc'] = junctions
    
    toFile.push(final);
}

// convert JSON object to string
const data3 = JSON.stringify(toFile);
// write JSON string to a file
fs.writeFile('testCUlane.json', data3, (err) => {
    if (err) {
        throw err;
    }
    console.log("JSON data is saved.");
});