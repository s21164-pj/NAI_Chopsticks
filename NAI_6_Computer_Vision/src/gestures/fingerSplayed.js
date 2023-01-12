import {Finger, FingerCurl, FingerDirection, GestureDescription} from 'fingerpose';

export const fingerSplayed = new GestureDescription('finger_splayed');

for (let finger of [
    Finger.Thumb,
    Finger.Index,
    Finger.Middle,
    Finger.Ring,
    Finger.Pinky
]) {

    fingerSplayed.addCurl(finger, FingerCurl.NoCurl, 1.0);
}
for (let finger of [
    Finger.Thumb,
    Finger.Index,
    Finger.Middle,
    Finger.Ring,
    Finger.Pinky
]) {

    fingerSplayed.addCurl(finger, FingerCurl.NoCurl, 1.0);
}

fingerSplayed.addDirection(Finger.Thumb, FingerDirection.HorizontalRight, 0.70);
fingerSplayed.addDirection(Finger.Thumb, FingerDirection.HorizontalLeft, 0.70);

fingerSplayed.addDirection(Finger.Index, FingerDirection.VerticalUp, 0.75);
fingerSplayed.addDirection(Finger.Index, FingerDirection.DiagonalUpLeft, 0.9);

fingerSplayed.addDirection(Finger.Middle, FingerDirection.VerticalUp, 0.9);
fingerSplayed.addDirection(Finger.Middle, FingerDirection.DiagonalUpLeft, 0.75);

fingerSplayed.addDirection(Finger.Ring, FingerDirection.VerticalUp, 0.9);
fingerSplayed.addDirection(Finger.Ring, FingerDirection.DiagonalUpRight, 0.75);

fingerSplayed.addDirection(Finger.Pinky, FingerDirection.VerticalUp, 0.75);
fingerSplayed.addDirection(Finger.Pinky, FingerDirection.DiagonalUpRight, 0.9);