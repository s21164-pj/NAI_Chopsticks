import {Finger, FingerCurl, FingerDirection, GestureDescription} from 'fingerpose';

export const raisedHand = new GestureDescription('raised_hand');

for (let finger of [
    Finger.Thumb,
    Finger.Index,
    Finger.Middle,
    Finger.Ring,
    Finger.Pinky
]) {

    raisedHand.addCurl(finger, FingerCurl.NoCurl, 1.0);
}
for (let finger of [
    Finger.Index,
    Finger.Middle,
    Finger.Ring,
    Finger.Pinky
]) {

    raisedHand.addDirection(finger, FingerDirection.VerticalUp, 0.95);
    raisedHand.addDirection(finger, FingerDirection.DiagonalUpLeft, 0.2);
    raisedHand.addDirection(finger, FingerDirection.DiagonalUpRight, 0.2);
}

// Thumb
raisedHand.addDirection(Finger.Thumb, FingerDirection.HorizontalRight, 0.5);
raisedHand.addDirection(Finger.Thumb, FingerDirection.HorizontalLeft, 0.5);