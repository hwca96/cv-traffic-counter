import cv2

class DrawLineWidget(object):
    def __init__(self, frame):
        self.original_image = frame
        self.clone = self.original_image.copy()

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.extract_coordinates)

        # List to store start/end points
        self.image_coordinates = []

    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_coordinates = [(x,y)]

        # Record ending (x,y) coordintes on left mouse bottom release
        elif event == cv2.EVENT_LBUTTONUP:
            self.image_coordinates.append((x,y))
            print('Starting: {}, Ending: {}'.format(self.image_coordinates[0], self.image_coordinates[1]))

            # Draw line
            cv2.rectangle(self.clone, self.image_coordinates[0], self.image_coordinates[1], (36,255,12), 2)
            cv2.imshow("image", self.clone) 

        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.original_image.copy()

    def show_image(self):
        return self.clone
    

if __name__ == '__main__':

    # Open the video file
    video_path = "data/inspection_day.mp4"
    cap = cv2.VideoCapture(video_path)
    static_frame = None

    while cap.isOpened():
        success, frame = cap.read()
        if success:
            static_frame = frame
            break
    
    if static_frame is not None:
        draw_line_widget = DrawLineWidget(static_frame)
        while True:
            cv2.imshow('image', draw_line_widget.show_image())
            key = cv2.waitKey(1)

            # Close program with keyboard 'q'
            if key == ord('q'):
                cv2.destroyAllWindows()
                exit(1)
    