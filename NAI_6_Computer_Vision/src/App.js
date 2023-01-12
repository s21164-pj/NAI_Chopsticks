import React, {useRef, useState} from "react";
import * as tf from "@tensorflow/tfjs";
import * as handpose from "@tensorflow-models/handpose";
import Webcam from "react-webcam";
import './App.css';
import {drawHand} from "./utilities";
import * as fp from "fingerpose";

//importy gestów
import {raisedHand} from "./gestures/raisedHand";
import {fingerSplayed} from "./gestures/fingerSplayed";
import {fist} from "./gestures/fist";
import {okGesture} from "./gestures/okGesture";
import {victory} from "./gestures/victory";

function App() {
    const webcamRef = useRef(null);
    const canvasRef = useRef(null);

    const [emoji, setEmoji] = useState(null);
    const [confidence, setConfidence] = useState(null);
    const quotes = {thumbs_up:'👍', victory:'✌',raised_hand:'✋', finger_splayed:'🖐', fist:'✊', ok:'👌'};

    /*
    * Załaduj wstępnie nauczony model uczenia maszynowego do wykrywania pozycji rąk i
    * wykrywaj co 100 milisekund.
    */
    const runHandpose = async () =>{
        const net = await handpose.load()
        console.log('Handpose loaded')
        setInterval(() =>{
            detect(net)
        }, 100)
    }
    
    // Przekaż przesyłany model wykrywania pozycji rąk jako parametr "net" do wykrywania pozycji rąk na wejściu wideo.
    const detect = async (net) =>{     
        //  Sprawdź czy wideo jest prawidłowo załadowane  
        if (typeof webcamRef.current !=="undefined" &&
            webcamRef.current !== null &&
            webcamRef.current.video.readyState === 4
        ) {
            // Jeśli wideo jest prawidłowo odzcytywane, ustaw obraz
            const video = webcamRef.current.video;
            const videoWidth = webcamRef.current.video.videoWidth;
            const videoHeight = webcamRef.current.video.videoHeight;

            webcamRef.current.video.width = videoWidth;
            webcamRef.current.video.height = videoHeight;

            canvasRef.current.width = videoWidth;
            canvasRef.current.height = videoHeight;
            // Wywołanie funkcji estimateHands do analizy wejścia obrazu, zwraca wykryte pozycję rąk
            const hand = await  net.estimateHands(video);
            // Wyświetl zwrócone dane w konsoli
            console.log(hand);


            if (hand.length > 0) {
                // Stwórz tablicę gestów, które program będzie rozpoznawał
                const GE = new fp.GestureEstimator([
                    fp.Gestures.ThumbsUpGesture,
                    victory,
                    raisedHand,
                    fingerSplayed,
                    okGesture
                ]);

                const gesture = await GE.estimate(hand[0].landmarks, 7);
                console.log(gesture);
                if (gesture.gestures !== undefined && gesture.gestures.length > 0) {
                    // Stwórz tablicę "confidence" zawierającą wartości "predykcji" dla każdego gestu z tablicy "gestures" 
                    // oraz wyświetl najbardziej prawdopodobny gest
                    const confidence = gesture.gestures.map(
                        (prediction) => prediction.confidence
                    );
                    console.log(confidence)
                    // Tworzymy zmienną "maxConfidence" przechowującą indeks gestu o największej wartości pewności
                    const maxConfidence = confidence.indexOf(
                        Math.max.apply(null, confidence)
                    );
                    // Ustawiamy zmienną "emoji" na nazwę gestu o największej wartości pewności
                    setEmoji(gesture.gestures[maxConfidence].name);
                    // Ustawiamy zmienną "confidence" na wartość pewności dla gestu o największej wartości 
                    // pewności zaokrągloną do dwóch miejsc po przecinku
                    setConfidence(gesture.gestures[maxConfidence].confidence.toFixed(2))
                    // Wyświetlamy w konsoli zmienną "emoji"
                    console.log(emoji);
                }
            }
            // Tworzymy zmienną "ctx", która przechowuje kontekst 2D elementu canvas, którego referencję trzymamy w zmiennej "canvasRef".
            // Następnie wywołujemy funkcję "drawHand" przekazując jako argumenty zmienną "hand" oraz zmienną "ctx".
            const ctx = canvasRef.current.getContext("2d");
            drawHand(hand, ctx);
        }
    };

    runHandpose()

    //Wyświetlanie widoku. Kamera i siatka dłoni są na siebie idealnie nałożone
    return (
        <div className="App">
            <header className="App-header">
                <Webcam
                    ref={webcamRef}
                    style={{
                        position: "absolute",
                        marginLeft: "auto",
                        marginRight: "auto",
                        left: 0,
                        right: 0,
                        textAlign: "center",
                        zindex: 9,
                        width: 640,
                        height: 480,
                    }}
                />

                <canvas
                    ref={canvasRef}
                    style={{
                        position: "absolute",
                        marginLeft: "auto",
                        marginRight: "auto",
                        left: 0,
                        right: 0,
                        textAlign: "center",
                        zindex: 9,
                        width: 640,
                        height: 480,
                    }}
                />
                {emoji !== null ? (
                    <p style={{
                        position: "absolute",
                        marginLeft: "auto",
                        marginRight: "auto",
                        left: 0,
                        bottom: 800,
                        right: 0,
                        textAlign: "center",
                        height: 100,
                    }}>
                        {quotes[emoji]} {confidence}
                    </p>
                ) : (
                    ""
                )}
            </header>
        </div>
    );
}

export default App;
