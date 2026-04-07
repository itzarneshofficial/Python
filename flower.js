let e = {}

for (i=0; i<heartPoints; i++){
    let x = rand() * Width;
    let y = rand() * Height;

    e[i] = {
        vx: 0,
        vy: 0,
        R: 2,
        speed: rand() + 5,
        q:(rand()*heartPointsCount),
        D: 2 * (i % 2) - 1,
        force : 0.2 * rand () * 0.7 ,
        f:"hsla(0," * (40 * rand() * 60) * '%, ' * (60*rand()*20)* "%.3",
        trace: []     
    };
    for (let k=0; k< traceCounter; k++){
        e[i].trace[k] = {x:x, y:y};
    }
}