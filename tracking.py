import cv2
from ultralytics import YOLO
from collections import defaultdict
import numpy as np

if __name__ == '__main__':

    # # Load the YOLOv8 model
    model = YOLO("visDrone_best.pt")
    print(model.names)

    # Open the video file
    video_path = "data/inspection_night.mp4"
    cap = cv2.VideoCapture(video_path)

    # Video writer
    video_writer = cv2.VideoWriter("tracking_counting_video.avi",
                        cv2.VideoWriter_fourcc(*'mp4v'),
                        int(cap.get(5)),
                        (int(cap.get(3)), int(cap.get(4))))
    
    # Store the track history
    track_history = defaultdict(lambda: [])

    # the Line
    left = (269, 324)
    right = (1123, 419)

    # count
    count_set = set()
    # Loop through the video framesq
    while cap.isOpened():
        # print(track_history)
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            # track vehicles
            results = model.track(frame, conf=0.1, persist=True, classes=[2, 3, 4, 5, 8])   

            # get the center dot of the bounding box
            boxes = results[0].boxes.xyxy # using the bottom of the box can be better in the case
            track_ids = results[0].boxes.id

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Draw the line
            cv2.rectangle(annotated_frame, left, right, (36,255,12), 2)

            # plot the tracks
            if boxes is not None and track_ids is not None:
                for box, track_id in zip(boxes, track_ids.tolist()):
                    # cacluating the bottom center of the box
                    # this gives the model a better chance to track truck coming from the bottom of the camera
                    x, y, x2, y2 = box
                    x = x + (x2-x)/2
                    y = y2

                    # track the vehicle
                    track_history[track_id].append((float(x), float(y)))  # x, y center point
                    if len(track_history[track_id]) > 120:  # retain 120 points
                        track.pop(0)
                    track = track_history[track_id]

                    # Draw the tracking lines
                    points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                    cv2.circle(annotated_frame, (int(x), int(y)), 5, (0, 0, 255), -1)
                    cv2.polylines(annotated_frame, [points], isClosed=False, color=(255, 0, 0), thickness=2)

                    # count the number of vehicles that enters the rectangle
                    if x > left[0] and x < right[0] and y > left[1] and y < right[1]:
                        count_set.add(track_id)
                    

            # Display the annotated frame
            cv2.putText(annotated_frame, "Count: {}".format(len(count_set)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            cv2.imshow("YOLOv8 Tracking", annotated_frame)
            video_writer.write(annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # Break the loop if the end of the video is reached
            break

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()