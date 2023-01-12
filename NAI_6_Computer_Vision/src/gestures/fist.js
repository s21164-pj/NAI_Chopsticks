import {Finger, FingerCurl, FingerDirection, GestureDescription} from 'fingerpose';

export const fist = new GestureDescription('fist');

fist.addCurl(Finger.Thumb, FingerCurl.HalfCurl, .7);
fist.addCurl(Finger.Thumb, FingerCurl.FullCurl,.7);


for(let finger of [Finger.Index, Finger.Middle, Finger.Ring, Finger.Pinky]) {
    fist.addCurl(finger, FingerCurl.FullCurl, 1.0);
}