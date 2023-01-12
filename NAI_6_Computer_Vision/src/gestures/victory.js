import {Finger, FingerCurl, FingerDirection, GestureDescription} from 'fingerpose';

export const victory = new GestureDescription('victory');


victory.addCurl(Finger.Thumb, FingerCurl.HalfCurl, 0.5);
victory.addCurl(Finger.Thumb, FingerCurl.NoCurl, 0.5);
victory.addDirection(Finger.Thumb, FingerDirection.VerticalUp, 1.0);
victory.addDirection(Finger.Thumb, FingerDirection.DiagonalUpLeft, 1.0);

victory.addCurl(Finger.Index, FingerCurl.NoCurl, 1.0);
victory.addDirection(Finger.Index, FingerDirection.VerticalUp, 0.75);
victory.addDirection(Finger.Index, FingerDirection.DiagonalUpLeft, 1.0);

victory.addCurl(Finger.Middle, FingerCurl.NoCurl, 1.0);
victory.addDirection(Finger.Middle, FingerDirection.VerticalUp, 1.0);
victory.addDirection(Finger.Middle, FingerDirection.DiagonalUpLeft, 0.75);

victory.addCurl(Finger.Ring, FingerCurl.FullCurl, 1.0);
victory.addDirection(Finger.Ring, FingerDirection.VerticalUp, 0.2);
victory.addDirection(Finger.Ring, FingerDirection.DiagonalUpLeft, 1.0);
victory.addDirection(Finger.Ring, FingerDirection.HorizontalLeft, 0.2);

victory.addCurl(Finger.Pinky, FingerCurl.FullCurl, 1.0);
victory.addDirection(Finger.Pinky, FingerDirection.VerticalUp, 0.2);
victory.addDirection(Finger.Pinky, FingerDirection.DiagonalUpLeft, 1.0);
victory.addDirection(Finger.Pinky, FingerDirection.HorizontalLeft, 0.2);

victory.setWeight(Finger.Index, 2);
victory.setWeight(Finger.Middle, 2);
