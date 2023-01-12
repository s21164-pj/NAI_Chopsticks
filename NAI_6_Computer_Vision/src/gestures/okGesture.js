import {Finger, FingerCurl, FingerDirection, GestureDescription} from 'fingerpose';

export const okGesture = new GestureDescription('ok');


okGesture.addCurl(Finger.Thumb, FingerCurl.NoCurl, 1.0);
okGesture.addDirection(Finger.Thumb, FingerDirection.DiagonalUpRight, .75);

okGesture.addCurl(Finger.Index, FingerCurl.HalfCurl, 1.0);
okGesture.addDirection(Finger.Index, FingerDirection.DiagonalUpRight, .75);

okGesture.addCurl(Finger.Middle, FingerCurl.NoCurl, 1.0);
okGesture.addDirection(Finger.Middle, FingerDirection.DiagonalUpRight, .75);

okGesture.addCurl(Finger.Ring, FingerCurl.NoCurl, 1.0);
okGesture.addDirection(Finger.Ring, FingerDirection.VerticalUp, .75);

okGesture.addCurl(Finger.Pinky, FingerCurl.NoCurl, 1.0);
okGesture.addDirection(Finger.Pinky, FingerDirection.VerticalUp, .75);
