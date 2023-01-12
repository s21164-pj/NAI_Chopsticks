//rysowanie dłoni (siatka i kropki)
export const drawHand = (predictions, ctx) => {
    if (predictions.length > 0) {
        predictions.forEach((prediction)=> {
            const landmarks = prediction.landmarks;

            for (let j = 0; j < Object.keys(fingerJoints).length; j++) {
                let finger = Object.keys(fingerJoints)[j];
                for (let k = 0; k < fingerJoints[finger].length -1; k++) {
                    const firstJointIndex = fingerJoints[finger][k];
                    const secondJointIndex = fingerJoints[finger][k+1];

                    //rysowanie lini pomiędzy kropkami
                    ctx.beginPath();
                    ctx.moveTo(
                            landmarks[firstJointIndex][0],
                            landmarks[firstJointIndex][1],
                    );
                    ctx.lineTo(
                        landmarks[secondJointIndex][0],
                        landmarks[secondJointIndex][1],
                    );
                    //wygląd linii i jej generowanie
                    ctx.strokeStyle = "yellow";
                    ctx.lineWith = 5;
                    ctx.stroke();
                }
            }

            for (let i=0; i<landmarks.length; i++) {
                // odczytywanie współrzędnych kropek
                const x = landmarks[i][0];
                const y = landmarks[i][1];
                const z = landmarks[i][2];

                // rysowanie kropek
                ctx.beginPath();
                ctx.arc(x, y, 5, 0, 3 * Math.PI)

                // Kolor kropek na łączeniach
                ctx.fillStyle = "red";
                ctx.fill();
            }
        })
    }
}

// przypisanie kropek to poszczególnych palców
const fingerJoints = {
    thumb: [0, 1, 2, 3, 4],
    indexFinger: [0, 5, 6, 7, 8],
    middleFinger: [0, 9, 10, 11, 12],
    ringFinger: [0, 13, 14, 15, 16],
    pinky: [0, 17, 18, 19, 20],
};