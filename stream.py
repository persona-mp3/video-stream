import cv2 as cv


def stream_video():
    print("streaming video")
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("could not open camera")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            print("no more frames to return")
            break

        cv.imshow("xtal300", frame)
        print("taping....")

        if cv.waitKey(1) == ord('q'):
            print("quiting recording")
            break

    cap.realease()
    cv.destroyAllWindows()


stream_video()
